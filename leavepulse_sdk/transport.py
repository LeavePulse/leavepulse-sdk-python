"""LeavePulse SDK — transport abstraction.

The SDK never knows how requests are authenticated or sent; it only calls
``await transport.request(...)``. Adapters supply the mechanism:
  - ``AuthenticatedTransport``: ``Authorization: Bearer`` over httpx, driven by
    a :class:`~leavepulse_sdk.credentials.CredentialProvider` (PAT, device flow,
    OAuth2, launcher) — refreshes once on a ``401`` when the provider can.
  - ``BearerTransport``: a thin specialization over a fixed token (a static
    credential), kept for back-compat with a pre-acquired bearer.
  - custom adapters: cookie/session auth, mocks for tests.

HTTP failures raise the typed :mod:`leavepulse_sdk.errors` hierarchy (chosen by
status code); the transport additionally retries 429 (honouring ``Retry-After``)
and 5xx (exponential backoff) up to ``retry.max_retries``.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from email.utils import parsedate_to_datetime
from typing import Any, Literal, Protocol, runtime_checkable
from urllib.parse import urlencode

import httpx

from .credentials import CredentialProvider, StaticCredential
from .errors import RateLimited, ServerError, Unauthorized, http_error_for

HttpMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]

#: Which backend a request targets. ``platform`` is the BFF (``/v1``); ``auth``
#: is the auth-service core (``/auth``) carrying login/refresh/oauth. The adapter
#: maps each channel to a base URL and to its own auth mechanism; the SDK never
#: learns *how* a channel authenticates, only which one to hit.
Channel = Literal["platform", "auth"]


@dataclass(frozen=True)
class TransportRequest:
    """A request the SDK asks a transport to dispatch."""

    method: HttpMethod
    #: Path relative to the channel root, e.g. ``/v1/projects/1``.
    path: str
    #: Backend channel; defaults to ``platform``.
    channel: Channel = "platform"
    #: Query parameters; ``None`` values are dropped.
    query: dict[str, Any] | None = None
    #: JSON request body.
    body: Any | None = None
    #: ``application/x-www-form-urlencoded`` body; mutually exclusive with
    #: ``body``. Required by the OAuth2 ``/auth/oauth/token`` endpoint, which
    #: consumes form-encoded (not JSON) grant requests.
    form: dict[str, str] | None = None


@runtime_checkable
class Transport(Protocol):
    """Anything that can dispatch a request and return decoded JSON."""

    async def request(
        self,
        method: HttpMethod,
        path: str,
        *,
        channel: Channel = "platform",
        query: dict[str, Any] | None = None,
        body: Any | None = None,
        form: dict[str, str] | None = None,
    ) -> Any: ...


def build_path(path: str, query: dict[str, Any] | None) -> str:
    """Append an encoded query string, dropping ``None`` values."""
    if not query:
        return path
    params = {k: v for k, v in query.items() if v is not None}
    if not params:
        return path
    return f"{path}?{httpx.QueryParams(params)}"


@dataclass
class RetryOptions:
    """Tuning for a transport's automatic retry behaviour."""

    #: Max automatic retries on 429 / 5xx. Set 0 to disable.
    max_retries: int = 2
    #: Base backoff in seconds for 5xx exponential backoff.
    backoff_base: float = 0.25
    #: Cap on any single backoff wait, seconds.
    backoff_max: float = 10.0


def _parse_retry_after(value: str | None) -> float | None:
    """Parse a ``Retry-After`` header (seconds or HTTP-date) into seconds."""
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        pass
    try:
        when = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if when is None:
        return None
    import datetime as _dt

    now = _dt.datetime.now(when.tzinfo)
    return max(0.0, (when - now).total_seconds())


class AuthenticatedTransport:
    """Bearer transport driven by a ``CredentialProvider`` rather than a fixed
    token.

    Before every request it asks ``provider.token()`` for the current bearer;
    on a ``401``, if the provider exposes ``refresh`` it refreshes **once** and
    retries the request **once** — covering device-flow / OAuth2 / launcher
    tokens that rotate. Automatically retries 429 (honouring ``Retry-After``)
    and 5xx (exponential backoff) up to ``retry.max_retries``, then raises a
    typed ``HTTPException``.
    """

    def __init__(
        self,
        base_url: str,
        provider: CredentialProvider,
        *,
        client: httpx.AsyncClient | None = None,
        auth_base_url: str | None = None,
        retry: RetryOptions | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        #: Auth-service base URL for the ``auth`` channel; defaults to the
        #: platform base when the auth core is co-hosted.
        self._auth_base_url = (auth_base_url or base_url).rstrip("/")
        self._provider = provider
        self._client = client or httpx.AsyncClient()
        self._retry = retry or RetryOptions()

    @staticmethod
    def _build_body(
        body: Any | None, form: dict[str, str] | None
    ) -> tuple[Any | None, str | None, str | None]:
        """Return ``(json_body, content, content_type)`` for one attempt.

        ``form`` (URL-encoded) and ``body`` (JSON) are mutually exclusive; the
        form variant supplies a raw ``content`` string and content type."""
        if form is not None:
            return None, urlencode(form), "application/x-www-form-urlencoded"
        return body, None, None

    async def request(
        self,
        method: HttpMethod,
        path: str,
        *,
        channel: Channel = "platform",
        query: dict[str, Any] | None = None,
        body: Any | None = None,
        form: dict[str, str] | None = None,
    ) -> Any:
        req = TransportRequest(
            method=method,
            path=path,
            channel=channel,
            query=query,
            body=body,
            form=form,
        )
        base = self._auth_base_url if channel == "auth" else self._base_url
        url = base + build_path(path, query)
        json_body, content, content_type = self._build_body(body, form)

        attempt = 0
        refreshed = False
        while True:
            token = await self._provider.token()
            headers = {"Authorization": f"Bearer {token}"}
            if content_type is not None:
                headers["Content-Type"] = content_type
            response = await self._client.request(
                method, url, json=json_body, content=content, headers=headers
            )
            if response.status_code < 400:
                if response.status_code == 204 or not response.content:
                    return None
                return response.json()

            retry_after = _parse_retry_after(response.headers.get("retry-after"))
            error = http_error_for(
                response.status_code, req, response.text, retry_after
            )

            # On 401, refresh the credential once and retry once before raising.
            refresh = getattr(self._provider, "refresh", None)
            if isinstance(error, Unauthorized) and not refreshed and callable(refresh):
                refreshed = True
                await refresh()
                continue

            retriable = isinstance(error, (RateLimited, ServerError))
            if retriable and attempt < self._retry.max_retries:
                if isinstance(error, RateLimited) and error.retry_after is not None:
                    wait = error.retry_after
                else:
                    wait = min(
                        self._retry.backoff_base * (2**attempt),
                        self._retry.backoff_max,
                    )
                attempt += 1
                await asyncio.sleep(wait)
                continue
            raise error

    async def aclose(self) -> None:
        await self._client.aclose()


class BearerTransport(AuthenticatedTransport):
    """Bearer-token transport for external consumers (no cookies) holding a
    single pre-acquired token.

    A thin specialization of :class:`AuthenticatedTransport` over a
    :class:`~leavepulse_sdk.credentials.StaticCredential`, kept for back-compat:
    the constructor signature ``(base_url, token, *, client?, auth_base_url?,
    retry?)`` is unchanged. For tokens that rotate (device flow, OAuth2,
    launcher) use ``AuthenticatedTransport`` with a refreshing credential.
    """

    def __init__(
        self,
        base_url: str,
        token: str,
        *,
        client: httpx.AsyncClient | None = None,
        auth_base_url: str | None = None,
        retry: RetryOptions | None = None,
    ) -> None:
        super().__init__(
            base_url,
            StaticCredential(token),
            client=client,
            auth_base_url=auth_base_url,
            retry=retry,
        )
