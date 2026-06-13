# Generated from the LeavePulse contract. Do not edit.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from leavepulse_sdk.resource import Resource

if TYPE_CHECKING:
    from leavepulse_sdk.client import ClientContext


class Session(Resource):
    """Session resource."""

    def __init__(self, data: dict[str, Any], ctx: "ClientContext") -> None:
        super().__init__(data)
        self._ctx = ctx

    @property
    def can_revoke(self) -> bool:
        """Whether the current user may revoke (RFC §4)."""
        return self._has_capability("session.revoke")

    async def revoke(self) -> Any:
        """session.revoke"""
        return await self._ctx.transport.request("POST", f"/v1/me/sessions/{self.id}/actions/revoke")
