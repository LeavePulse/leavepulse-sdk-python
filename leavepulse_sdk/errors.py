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
    #: Stable machine-readable error code, UPPER_SNAKE (e.g. ``RESOURCE_NOT_FOUND``).
    code: str | None = None
    timestamp: str | None = None
    #: Correlation id for support / log lookup.
    request_id: str | None = None
    #: Originating service name.
    service: str | None = None
    #: Extra structured context. For validation failures it holds
    #: ``{"errors": [{"key", "message", "source"}], "path"}``.
    details: dict[str, Any] | None = None


@dataclass(frozen=True)
class FieldError:
    """A single per-field validation failure, normalized from the backend's
    ``details.errors`` array (Litestar's ``{key, message, source}`` shape)."""

    #: The offending field path (e.g. ``email``, ``body.address.city``).
    field: str
    #: Human-readable validation message.
    message: str
    #: Where it came from: ``body`` | ``query`` | ``path`` | …
    source: str | None = None


def field_errors_of(problem: ProblemDetails | None) -> list[FieldError]:
    """Extract normalized per-field validation errors from a problem's
    ``details``. The backend reports them as
    ``details.errors = [{key, message, source}]``; legacy/other shapes
    (``details.fields`` mapping, pydantic ``{loc, msg}``) are tolerated."""
    details = problem.details if problem else None
    if not isinstance(details, dict):
        return []

    def from_entry(entry: Any) -> FieldError | None:
        if not isinstance(entry, dict):
            return None
        loc = (
            entry.get("key")
            or entry.get("field")
            or entry.get("path")
            or entry.get("loc")
        )
        field = ".".join(str(p) for p in loc) if isinstance(loc, list) else str(loc or "")
        message = str(entry.get("message") or entry.get("msg") or entry.get("detail") or "")
        source = entry.get("source")
        if not field and not message:
            return None
        return FieldError(field=field, message=message, source=str(source) if source else None)

    raw = details.get("errors")
    if isinstance(raw, list):
        return [fe for fe in (from_entry(e) for e in raw) if fe is not None]
    fields = details.get("fields")
    if isinstance(fields, dict):
        return [FieldError(field=k, message=str(v)) for k, v in fields.items()]
    return []


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
        """Machine-readable error code, when the server supplied one
        (UPPER_SNAKE, e.g. ``RESOURCE_NOT_FOUND``)."""
        return self.problem.code if self.problem else None

    def is_code(self, code: str) -> bool:
        """Whether the server's stable error code matches ``code`` — a
        transport-agnostic check (``err.is_code("SESSION_EXPIRED")``)."""
        return bool(self.problem and self.problem.code == code)

    @property
    def request_id(self) -> str | None:
        """Correlation id for support, when present."""
        return self.problem.request_id if self.problem else None

    @property
    def field_errors(self) -> list[FieldError]:
        """Normalized per-field validation errors, when the backend reported
        them (populated for 400/422 validation failures)."""
        return field_errors_of(self.problem)


class BadRequest(HTTPException):
    """400 — malformed request / failed validation."""


class UnprocessableEntity(HTTPException):
    """422 — semantic validation failure (the backend's primary validation
    status, carrying ``details.errors``). Shares ``field_errors`` with
    :class:`BadRequest`."""


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
    if status == 422:
        return UnprocessableEntity(status, request, problem, raw)
    if status == 429:
        return RateLimited(status, request, problem, raw, retry_after)
    if status >= 500:
        return ServerError(status, request, problem, raw)
    return HTTPException(status, request, problem, raw)
