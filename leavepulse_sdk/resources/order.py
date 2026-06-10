# Generated from the LeavePulse contract. Do not edit.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from leavepulse_sdk.resource import Resource

if TYPE_CHECKING:
    from leavepulse_sdk.client import ClientContext


class Order(Resource):
    """Order resource."""

    def __init__(self, data: dict[str, Any], ctx: "ClientContext") -> None:
        super().__init__(data)
        self._ctx = ctx

    async def refresh(self) -> "Order":
        """Re-fetch this Order and hydrate in place."""
        data = await self._ctx.transport.request("GET", f"/v1/billing/orders/{self.id}")
        self._ctx.hydrate("Order", data)
        return self
