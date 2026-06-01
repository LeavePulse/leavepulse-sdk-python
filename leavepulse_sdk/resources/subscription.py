# Generated from the LeavePulse contract. Do not edit.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from leavepulse_sdk.resource import Resource

if TYPE_CHECKING:
    from leavepulse_sdk.client import ClientContext


class Subscription(Resource):
    """Subscription resource."""

    def __init__(self, data: dict[str, Any], ctx: "ClientContext") -> None:
        super().__init__(data)
        self._ctx = ctx

    @property
    def can_cancel(self) -> bool:
        """Whether the current user may cancel (RFC §4)."""
        return self._has_capability("subscription.cancel")

    async def cancel(self) -> "Subscription":
        """subscription.cancel"""
        data = await self._ctx.transport.request("PATCH", f"/v1/billing/subscriptions/{self.id}/cancel")
        self._ctx.hydrate("Subscription", data)
        return self
