# Generated from the LeavePulse contract. Do not edit.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from leavepulse_sdk.resource import Resource

if TYPE_CHECKING:
    from leavepulse_sdk.client import ClientContext


class Form(Resource):
    """Form resource."""

    def __init__(self, data: dict[str, Any], ctx: "ClientContext") -> None:
        super().__init__(data)
        self._ctx = ctx

    async def refresh(self) -> "Form":
        """Re-fetch this Form and hydrate in place."""
        data = await self._ctx.transport.request("GET", f"/v1/whitelist/forms/{self.id}")
        self._ctx.hydrate("Form", data)
        return self

    @property
    def can_delete(self) -> bool:
        """Whether the current user may delete (RFC §4)."""
        return self._has_capability("form.delete")

    @property
    def can_update(self) -> bool:
        """Whether the current user may update (RFC §4)."""
        return self._has_capability("form.update")

    async def delete(self) -> "Form":
        """form.delete"""
        data = await self._ctx.transport.request("DELETE", f"/v1/whitelist/forms/{self.id}")
        self._ctx.hydrate("Form", data)
        return self

    async def update(self, body: dict[str, Any]) -> "Form":
        """form.update"""
        data = await self._ctx.transport.request("PATCH", f"/v1/whitelist/forms/{self.id}", body=body)
        self._ctx.hydrate("Form", data)
        return self

    async def set_import_mapping(self, body: dict[str, Any]) -> "Form":
        """form.set_import_mapping"""
        data = await self._ctx.transport.request("PATCH", f"/v1/whitelist/forms/{self.id}/import-mapping", body=body)
        self._ctx.hydrate("Form", data)
        return self
