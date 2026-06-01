# Generated from the LeavePulse contract. Do not edit.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from leavepulse_sdk.client import ClientContext


class Order:
    """Order — a scope namespace (no instance identity)."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def get(self, order_id: str) -> Any:
        """order.get"""
        return await self._ctx.transport.request("GET", f"/v1/billing/orders/{order_id}")
