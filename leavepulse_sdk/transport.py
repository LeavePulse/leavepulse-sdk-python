"""LeavePulse SDK — transport abstraction.

The SDK never knows how requests are authenticated or sent; it only calls
``await transport.request(...)``. Adapters supply the mechanism:
  - ``BearerTransport``: ``Authorization: Bearer`` over httpx, for external use.
  - custom adapters: cookie/session auth, mocks for tests.

HTTP failures raise the typed :mod:`leavepulse_sdk.errors` hierarchy (chosen by
status code); ``BearerTransport`` additionally retries 429 (honouring
``Retry-After``) and 5xx (exponential backoff) up to ``retry.max_retries``.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from email.utils import parsedate_to_datetime
from typing import Any, Literal, Protocol, runtime_checkable

import httpx

from .errors import RateLimited, ServerError, http_error_for

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


class BearerTransport:
    """Bearer-token transport for external consumers (no cookies).

    Automatically retries 429 (honouring ``Retry-After``) and 5xx (exponential
    backoff) up to ``retry.max_retries``, then raises a typed ``HTTPException``.
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
        self._base_url = base_url.rstrip("/")
        #: Auth-service base URL for the ``auth`` channel; defaults to the
        #: platform base when the auth core is co-hosted.
        self._auth_base_url = (auth_base_url or base_url).rstrip("/")
        self._token = token
        self._client = client or httpx.AsyncClient()
        self._retry = retry or RetryOptions()

    async def request(
        self,
        method: HttpMethod,
        path: str,
        *,
        channel: Channel = "platform",
        query: dict[str, Any] | None = None,
        body: Any | None = None,
    ) -> Any:
        req = TransportRequest(
            method=method, path=path, channel=channel, query=query, body=body
        )
        base = self._auth_base_url if channel == "auth" else self._base_url
        url = base + build_path(path, query)
        headers = {"Authorization": f"Bearer {self._token}"}

        attempt = 0
        while True:
            response = await self._client.request(
                method, url, json=body, headers=headers
            )
            if response.status_code < 400:
                if response.status_code == 204 or not response.content:
                    return None
                return response.json()

            retry_after = _parse_retry_after(response.headers.get("retry-after"))
            error = http_error_for(
                response.status_code, req, response.text, retry_after
            )

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
