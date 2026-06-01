# Generated from the LeavePulse contract. Do not edit.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from leavepulse_sdk.resource import Resource

if TYPE_CHECKING:
    from leavepulse_sdk.client import ClientContext


class Binding(Resource):
    """Binding resource."""

    def __init__(self, data: dict[str, Any], ctx: "ClientContext") -> None:
        super().__init__(data)
        self._ctx = ctx

    @property
    def can_delete(self) -> bool:
        """Whether the current user may delete (RFC §4)."""
        return self._has_capability("binding.delete")

    @property
    def can_update(self) -> bool:
        """Whether the current user may update (RFC §4)."""
        return self._has_capability("binding.update")

    @property
    def can_test(self) -> bool:
        """Whether the current user may test (RFC §4)."""
        return self._has_capability("binding.test")

    async def delete(self) -> "Binding":
        """binding.delete"""
        data = await self._ctx.transport.request("DELETE", f"/v1/whitelist/bindings/{self.id}")
        self._ctx.hydrate("Binding", data)
        return self

    async def update(self, body: dict[str, Any]) -> "Binding":
        """binding.update"""
        data = await self._ctx.transport.request("PATCH", f"/v1/whitelist/bindings/{self.id}", body=body)
        self._ctx.hydrate("Binding", data)
        return self

    async def test(self, *, audience: str | None = None) -> "Binding":
        """binding.test"""
        data = await self._ctx.transport.request("POST", f"/v1/whitelist/bindings/{self.id}/actions/test-notifications", query={"audience": audience})
        self._ctx.hydrate("Binding", data)
        return self

    async def entries_add(self, body: dict[str, Any]) -> "Binding":
        """binding.entries.add"""
        data = await self._ctx.transport.request("POST", f"/v1/whitelist/bindings/{self.id}/direct/entries", body=body)
        self._ctx.hydrate("Binding", data)
        return self

    async def entries_remove(self) -> "Binding":
        """binding.entries.remove"""
        data = await self._ctx.transport.request("DELETE", f"/v1/whitelist/bindings/{self.id}/direct/entries/{self.id}")
        self._ctx.hydrate("Binding", data)
        return self
