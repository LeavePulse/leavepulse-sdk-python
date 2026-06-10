"""LeavePulse SDK — OAuth device-flow (RFC 8628) polling helper.

``auth.device.start`` / ``approve`` / ``token`` are the raw generated calls.
This wraps the token poll loop: call ``token`` every ``interval`` seconds, back
off on ``slow_down``, and resolve once the user approves (or reject on
expiry/denial). Framework-agnostic — the caller passes the poll function.

``begin_device_flow`` is the higher-level headless facade: it runs ``start``,
surfaces the user-facing URL + code, and exposes ``.poll()`` which honours the
returned interval and maps the approved grant into a ``RefreshingCredential``.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Literal

from .credentials import RefreshFn, RefreshingCredential, TokenPair

#: The poll status the token endpoint returns (RFC 8628 §3.5).
DevicePollStatus = Literal["approved", "pending", "slow_down", "expired", "denied"]


@dataclass(frozen=True)
class DeviceTokenResponse:
    """Minimal shape of an ``auth.device.token`` response the poller needs."""

    status: DevicePollStatus
    access_token: str | None = None
    token_type: str | None = None
    expires_in: float | None = None
    refresh_token: str | None = None
    refresh_token_expires_in: float | None = None


@dataclass(frozen=True)
class DeviceStartResponse:
    """Shape of an ``auth.device.start`` response (RFC 8628 §3.2, snake_case)."""

    #: Opaque code the client polls ``token`` with.
    device_code: str
    #: Short code the user enters in the frontend (``device.vue``).
    user_code: str
    #: URL the user opens to approve.
    verification_uri: str
    #: Seconds until the device code expires.
    expires_in: float
    #: ``verification_uri`` with the ``user_code`` pre-filled, when provided.
    verification_uri_complete: str | None = None
    #: Recommended seconds between polls.
    interval: float | None = None


class DeviceFlowError(Exception):
    """Raised when a device authorization can't complete."""

    def __init__(self, status: Literal["expired", "denied", "aborted"]) -> None:
        super().__init__(f"device authorization {status}")
        self.status = status


async def poll_device_token(
    token: Callable[[], Awaitable[DeviceTokenResponse]],
    *,
    interval_seconds: float = 5.0,
    slow_down_step_seconds: float = 5.0,
) -> DeviceTokenResponse:
    """Poll ``token`` until the user approves the device.

    Resolves with the approved token response, or raises :class:`DeviceFlowError`
    on expiry/denial. Cancellation of the awaiting task aborts the loop.

    :param token: a coroutine performing one ``auth.device.token`` call.
    """
    interval = interval_seconds
    while True:
        response = await token()
        status = response.status
        if status == "approved":
            return response
        if status == "expired":
            raise DeviceFlowError("expired")
        if status == "denied":
            raise DeviceFlowError("denied")
        if status == "slow_down":
            interval += slow_down_step_seconds
        # "pending" and "slow_down" both fall through to the wait.
        await asyncio.sleep(interval)


@dataclass(frozen=True)
class DeviceFlowHandle:
    """A started device authorization: user-facing fields plus a ``poll()``
    that blocks until approval and yields a refreshing credential."""

    #: Short code the user confirms in the frontend.
    user_code: str
    #: URL the user opens to approve the device.
    verification_uri: str
    #: Seconds until the device code expires.
    expires_in: float
    #: The ``device_code`` to poll with (exposed for advanced callers).
    device_code: str
    #: ``verification_uri`` with the code pre-filled, when the server gave it.
    verification_uri_complete: str | None = None
    #: Poll runner, bound to the started device code. Use :meth:`poll`.
    _poll: Callable[[], Awaitable[RefreshingCredential]] | None = None

    async def poll(self) -> RefreshingCredential:
        """Poll ``token`` (honouring ``interval``/``slow_down``/``expires_in``)
        until the user approves, then resolve with a
        :class:`~leavepulse_sdk.credentials.RefreshingCredential` seeded from the
        grant. Raises :class:`DeviceFlowError` on expiry/denial/abort."""
        if self._poll is None:  # pragma: no cover - constructed by facade
            raise RuntimeError("device flow handle has no bound poll runner")
        return await self._poll()


async def begin_device_flow(
    start: Callable[[], Awaitable[DeviceStartResponse]],
    poll: Callable[[str], Awaitable[DeviceTokenResponse]],
    *,
    refresh_fn: RefreshFn | None = None,
    leeway_seconds: float = 30.0,
    slow_down_step_seconds: float = 5.0,
) -> DeviceFlowHandle:
    """Begin RFC 8628 device authorization headlessly.

    Calls ``start()``, returns the user-facing URL + code immediately, and
    exposes ``.poll()`` which runs :func:`poll_device_token` with the
    server-advised ``interval`` and maps the approved grant into a
    :class:`~leavepulse_sdk.credentials.RefreshingCredential`.

    :param start: a coroutine performing one ``auth.device.start`` call.
    :param poll:  a coroutine performing one ``auth.device.token`` call for a
                  given ``device_code``.
    """
    started = await start()

    async def run_poll() -> RefreshingCredential:
        approved = await poll_device_token(
            lambda: poll(started.device_code),
            interval_seconds=started.interval if started.interval is not None else 5.0,
            slow_down_step_seconds=slow_down_step_seconds,
        )
        if not approved.access_token or not approved.refresh_token:
            raise DeviceFlowError("denied")
        if refresh_fn is None:

            async def _no_refresh(_token: str) -> TokenPair:
                raise RuntimeError(
                    "device-flow credential has no refresh_fn; provide one in "
                    "begin_device_flow options"
                )

            effective_refresh: RefreshFn = _no_refresh
        else:
            effective_refresh = refresh_fn
        return RefreshingCredential(
            access_token=approved.access_token,
            refresh_token=approved.refresh_token,
            refresh_fn=effective_refresh,
            expires_in=approved.expires_in,
            leeway_seconds=leeway_seconds,
        )

    return DeviceFlowHandle(
        user_code=started.user_code,
        verification_uri=started.verification_uri,
        verification_uri_complete=started.verification_uri_complete,
        expires_in=started.expires_in,
        device_code=started.device_code,
        _poll=run_poll,
    )
