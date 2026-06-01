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

    async def whitelist_apply(self, body: dict[str, Any]) -> "Application":
        """server.whitelist.apply"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/whitelist/applications", body=body)
        self._ctx.hydrate("Application", data)
        return self

    async def set_status(self, body: dict[str, Any]) -> "Application":
        """application.set_status"""
        data = await self._ctx.transport.request("PATCH", f"/v1/servers/{self.id}/whitelist/applications/{self.id}", body=body)
        self._ctx.hydrate("Application", data)
        return self

    async def approve(self, body: dict[str, Any]) -> "Application":
        """application.approve"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/whitelist/applications/{self.id}/approve", body=body)
        self._ctx.hydrate("Application", data)
        return self

    async def deny(self, body: dict[str, Any]) -> "Application":
        """application.deny"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/whitelist/applications/{self.id}/deny", body=body)
        self._ctx.hydrate("Application", data)
        return self

    async def resubmit(self, body: dict[str, Any]) -> "Application":
        """application.resubmit"""
        data = await self._ctx.transport.request("PATCH", f"/v1/servers/{self.id}/whitelist/applications/{self.id}/resubmit", body=body)
        self._ctx.hydrate("Application", data)
        return self
