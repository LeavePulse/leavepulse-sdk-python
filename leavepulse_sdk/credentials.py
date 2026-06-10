"""LeavePulse SDK — credential providers.

A :class:`CredentialProvider` is the seam between *acquiring* a token (PAT,
device flow, OAuth2, service token) and *sending* it: ``AuthenticatedTransport``
asks the provider for a bearer before each request and, on a ``401``, for a
refresh. Providers are transport-agnostic — anything that performs a network
call (e.g. a token refresh) is injected, never hardcoded — so the same provider
works from a CLI, a service, or the launcher.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class TokenPair:
    """The token pair a refresh call yields (wire shape: snake_case)."""

    access_token: str
    refresh_token: str | None = None
    #: Access-token lifetime in seconds, used to compute the local expiry.
    expires_in: float | None = None


#: Performs the actual refresh exchange. Injected so the credential stays
#: transport-agnostic (no hardcoded httpx/URL): the caller decides whether it
#: hits the transport, a raw client, or a mock.
RefreshFn = Callable[[str], Awaitable[TokenPair]]


@runtime_checkable
class CredentialProvider(Protocol):
    """Supplies the bearer token a transport sends, and optionally rotates it.

    - ``token()`` returns the **current** access token to send.
    - ``refresh()`` (optional) exchanges a refresh token for a new pair; the
      transport calls it once on a ``401`` and retries. Providers without a
      meaningful refresh (PAT, service token) may omit it — the transport
      checks for the attribute before calling.
    """

    async def token(self) -> str:
        """The current bearer token to send on the next request."""
        ...


class StaticCredential:
    """A fixed, non-rotating credential: ``token()`` always returns the same
    value and there is no ``refresh``. Use for Personal Access Tokens and
    out-of-band service tokens — ``BearerTransport`` is exactly this."""

    def __init__(self, token: str) -> None:
        self._token = token

    async def token(self) -> str:
        return self._token


class RefreshingCredential:
    """Holds an access + refresh token locally and rotates them on demand.

    ``token()`` returns the access token, transparently refreshing first if it
    is known to be (nearly) expired; ``refresh()`` forces an exchange (called
    by the transport on a ``401``). The network exchange is delegated to the
    injected ``refresh_fn``, so this works for the launcher (refresh-in-body),
    device flow, and any other rotating credential without knowing the URL or
    transport. Concurrent refreshes are coalesced into one in-flight exchange.
    """

    def __init__(
        self,
        access_token: str,
        refresh_token: str,
        refresh_fn: RefreshFn,
        *,
        expires_in: float | None = None,
        leeway_seconds: float = 30.0,
    ) -> None:
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._refresh_fn = refresh_fn
        self._leeway = leeway_seconds
        #: Monotonic deadline when the access token expires, or ``None`` if
        #: unknown.
        self._expires_at = _expiry_from_seconds(expires_in)
        self._lock = asyncio.Lock()
        #: Coalesces concurrent refreshes into one in-flight exchange.
        self._inflight: asyncio.Task[None] | None = None

    @property
    def current_refresh_token(self) -> str:
        """The current refresh token (for persisting to a local store)."""
        return self._refresh_token

    async def token(self) -> str:
        # Refresh ``leeway`` seconds early so the token is still valid for the
        # request it's fetched for.
        if self._expires_at is not None and time.monotonic() >= self._expires_at - self._leeway:
            await self.refresh()
        return self._access_token

    async def refresh(self) -> None:
        # Coalesce concurrent callers (e.g. a 401 retry racing an expiry check)
        # into a single in-flight exchange shared by all awaiters.
        async with self._lock:
            if self._inflight is None or self._inflight.done():
                self._inflight = asyncio.create_task(self._do_refresh())
            task = self._inflight
        await task

    async def _do_refresh(self) -> None:
        pair = await self._refresh_fn(self._refresh_token)
        self._apply_token_pair(pair)

    def _apply_token_pair(self, pair: TokenPair) -> None:
        """Adopt a freshly-issued token pair (keeps the old refresh token if the
        server rotated only the access token)."""
        self._access_token = pair.access_token
        if pair.refresh_token:
            self._refresh_token = pair.refresh_token
        self._expires_at = _expiry_from_seconds(pair.expires_in)


class OAuth2Credential(RefreshingCredential):
    """A credential seeded from an OAuth2 authorization-code token exchange that
    auto-refreshes via the same ``/auth/oauth/token`` endpoint. Behaviour is
    identical to :class:`RefreshingCredential`; it exists as a named type so
    ``oauth2.exchange_code`` can return a self-describing credential."""


def _expiry_from_seconds(expires_in: float | None) -> float | None:
    """Convert a seconds-from-now lifetime into an absolute monotonic deadline."""
    if expires_in is None:
        return None
    return time.monotonic() + expires_in
