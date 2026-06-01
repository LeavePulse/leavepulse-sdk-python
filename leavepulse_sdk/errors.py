"""LeavePulse SDK — error hierarchy (discord.py-style).

Every failure is a :class:`LeavePulseError`. HTTP failures are an
:class:`HTTPException` subclass chosen by status code, so callers can write
``except NotFound:``. The backend speaks RFC 7807 problem+json (service-toolkit
/ awesome_errors), so the parsed :class:`ProblemDetails` carries the
machine-readable ``code``, human ``detail``, validation ``fields``, and
``request_id`` for support.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .transport import TransportRequest


@dataclass(frozen=True)
class ProblemDetails:
    """RFC 7807 problem details as emitted by the LeavePulse backend."""

    type: str | None = None
    title: str | None = None
    status: int | None = None
    detail: str | None = None
    instance: str | None = None
    #: Stable machine-readable error code (e.g. ``whitelist.not_found``).
    code: str | None = None
    timestamp: str | None = None
    #: Correlation id for support / log lookup.
    request_id: str | None = None
    #: Originating service name.
    service: str | None = None
    #: Extra structured context, including per-field validation errors.
    details: dict[str, Any] | None = None


class LeavePulseError(Exception):
    """Base class for every error the SDK raises."""


class MalformedResponse(LeavePulseError):
    """The server returned a payload that doesn't match the expected shape.

    Distinct from an HTTP error: the request succeeded but the body is
    unusable (e.g. a resource with no id to identity-map on).
    """

    def __init__(self, message: str, payload: Any) -> None:
        super().__init__(message)
        self.payload = payload


class HTTPException(LeavePulseError):
    """Any non-2xx HTTP response. Subclasses narrow by status."""

    def __init__(
        self,
        status: int,
        request: TransportRequest,
        problem: ProblemDetails | None,
        raw: str,
    ) -> None:
        code = f" [{problem.code}]" if problem and problem.code else ""
        detail = (problem.detail or problem.title) if problem else None
        detail = detail or raw
        suffix = f": {detail}" if detail else ""
        super().__init__(
            f"{request.method} {request.path} -> {status}{code}{suffix}"
        )
        self.status = status
        self.request = request
        self.problem = problem
        #: Raw response body text when it wasn't valid problem+json.
        self.raw = raw

    @property
    def code(self) -> str | None:
        """Machine-readable error code, when the server supplied one."""
        return self.problem.code if self.problem else None

    @property
    def request_id(self) -> str | None:
        """Correlation id for support, when present."""
        return self.problem.request_id if self.problem else None


class BadRequest(HTTPException):
    """400 — malformed request / failed validation."""

    @property
    def fields(self) -> dict[str, Any] | None:
        """Per-field validation errors, when the backend reported them."""
        details = self.problem.details if self.problem else None
        if isinstance(details, dict):
            found = details.get("fields") or details.get("errors")
            if isinstance(found, dict):
                return found
        return None


class Unauthorized(HTTPException):
    """401 — authentication required or failed."""


class Forbidden(HTTPException):
    """403 — authenticated but not permitted."""


class NotFound(HTTPException):
    """404 — resource not found."""


class Conflict(HTTPException):
    """409 — state conflict (e.g. duplicate, already-exists)."""


class RateLimited(HTTPException):
    """429 — rate limited. ``retry_after`` is the server-advised wait (s)."""

    def __init__(
        self,
        status: int,
        request: TransportRequest,
        problem: ProblemDetails | None,
        raw: str,
        retry_after: float | None,
    ) -> None:
        super().__init__(status, request, problem, raw)
        self.retry_after = retry_after


class ServerError(HTTPException):
    """5xx — the server failed to fulfil a valid request."""


def parse_problem(raw: str) -> ProblemDetails | None:
    """Parse a response body as RFC 7807 problem+json; ``None`` if not JSON."""
    if not raw:
        return None
    try:
        obj = json.loads(raw)
    except (ValueError, TypeError):
        return None
    if not isinstance(obj, dict):
        return None
    # The wire uses snake_case (``request_id``), which already matches.
    return ProblemDetails(
        type=obj.get("type"),
        title=obj.get("title"),
        status=obj.get("status"),
        detail=obj.get("detail"),
        instance=obj.get("instance"),
        code=obj.get("code"),
        timestamp=obj.get("timestamp"),
        request_id=obj.get("request_id") or obj.get("requestId"),
        service=obj.get("service"),
        details=obj.get("details"),
    )


def http_error_for(
    status: int,
    request: TransportRequest,
    raw: str,
    retry_after: float | None = None,
) -> HTTPException:
    """Build the right :class:`HTTPException` subclass from a failed response."""
    problem = parse_problem(raw)
    if status == 400:
        return BadRequest(status, request, problem, raw)
    if status == 401:
        return Unauthorized(status, request, problem, raw)
    if status == 403:
        return Forbidden(status, request, problem, raw)
    if status == 404:
        return NotFound(status, request, problem, raw)
    if status == 409:
        return Conflict(status, request, problem, raw)
    if status == 429:
        return RateLimited(status, request, problem, raw, retry_after)
    if status >= 500:
        return ServerError(status, request, problem, raw)
    return HTTPException(status, request, problem, raw)
