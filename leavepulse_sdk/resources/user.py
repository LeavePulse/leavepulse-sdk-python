# Generated from the LeavePulse contract. Do not edit.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from leavepulse_sdk.resource import Resource

if TYPE_CHECKING:
    from leavepulse_sdk.client import ClientContext


class User(Resource):
    """User resource."""

    def __init__(self, data: dict[str, Any], ctx: "ClientContext") -> None:
        super().__init__(data)
        self._ctx = ctx

    async def refresh(self) -> "User":
        """Re-fetch this User and hydrate in place."""
        data = await self._ctx.transport.request("GET", f"/v1/users/{self.id}/public-profile")
        self._ctx.hydrate("User", data)
        return self

    @property
    def can_report(self) -> bool:
        """Whether the current user may report (RFC §4)."""
        return self._has_capability("user.report")

    async def report(self, body: dict[str, Any]) -> Any:
        """user.report"""
        return await self._ctx.transport.request("POST", f"/v1/community/users/{self.id}/report", body=body)
