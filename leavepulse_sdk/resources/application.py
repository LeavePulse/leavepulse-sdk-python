# Generated from the LeavePulse contract. Do not edit.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from leavepulse_sdk.resource import Resource

if TYPE_CHECKING:
    from leavepulse_sdk.client import ClientContext


class Application(Resource):
    """Application resource."""

    def __init__(self, data: dict[str, Any], ctx: "ClientContext") -> None:
        super().__init__(data)
        self._ctx = ctx

    @property
    def can_apply(self) -> bool:
        """Whether the current user may apply (RFC §4)."""
        return self._has_capability("application.apply")

    @property
    def can_set_status(self) -> bool:
        """Whether the current user may set_status (RFC §4)."""
        return self._has_capability("application.set_status")

    @property
    def can_approve(self) -> bool:
        """Whether the current user may approve (RFC §4)."""
        return self._has_capability("application.approve")

    @property
    def can_deny(self) -> bool:
        """Whether the current user may deny (RFC §4)."""
        return self._has_capability("application.deny")

    @property
    def can_resubmit(self) -> bool:
        """Whether the current user may resubmit (RFC §4)."""
        return self._has_capability("application.resubmit")

    async def whitelist_apply(self, body: dict[str, Any]) -> Any:
        """server.whitelist.apply"""
        return await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/whitelist/applications", body=body)

    async def set_status(self, body: dict[str, Any]) -> Any:
        """application.set_status"""
        return await self._ctx.transport.request("PATCH", f"/v1/servers/{self.id}/whitelist/applications/{self.id}", body=body)

    async def approve(self, body: dict[str, Any]) -> Any:
        """application.approve"""
        return await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/whitelist/applications/{self.id}/approve", body=body)

    async def deny(self, body: dict[str, Any]) -> Any:
        """application.deny"""
        return await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/whitelist/applications/{self.id}/deny", body=body)

    async def resubmit(self, body: dict[str, Any]) -> Any:
        """application.resubmit"""
        return await self._ctx.transport.request("PATCH", f"/v1/servers/{self.id}/whitelist/applications/{self.id}/resubmit", body=body)
