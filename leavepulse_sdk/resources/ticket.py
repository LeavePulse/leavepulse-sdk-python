# Generated from the LeavePulse contract. Do not edit.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from leavepulse_sdk.resource import Resource

if TYPE_CHECKING:
    from leavepulse_sdk.client import ClientContext


class Ticket(Resource):
    """Ticket resource."""

    def __init__(self, data: dict[str, Any], ctx: "ClientContext") -> None:
        super().__init__(data)
        self._ctx = ctx

    @property
    def can_set_status(self) -> bool:
        """Whether the current user may set_status (RFC §4)."""
        return self._has_capability("ticket.set_status")

    @property
    def can_reply(self) -> bool:
        """Whether the current user may reply (RFC §4)."""
        return self._has_capability("ticket.reply")

    async def set_status(self, body: dict[str, Any]) -> "Ticket":
        """ticket.set_status"""
        data = await self._ctx.transport.request("PATCH", f"/v1/community/tickets/{self.id}", body=body)
        self._ctx.hydrate("Ticket", data)
        return self

    async def reply(self, body: dict[str, Any]) -> Any:
        """ticket.reply"""
        return await self._ctx.transport.request("POST", f"/v1/community/tickets/{self.id}/messages", body=body)
