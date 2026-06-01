# Generated from the LeavePulse contract. Do not edit.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from leavepulse_sdk.resource import Resource

if TYPE_CHECKING:
    from leavepulse_sdk.client import ClientContext


class Build(Resource):
    """Build resource."""

    def __init__(self, data: dict[str, Any], ctx: "ClientContext") -> None:
        super().__init__(data)
        self._ctx = ctx

    async def refresh(self) -> "Build":
        """Re-fetch this Build and hydrate in place."""
        data = await self._ctx.transport.request("GET", f"/v1/builds/{self.id}")
        self._ctx.hydrate("Build", data)
        return self

    @property
    def can_delete(self) -> bool:
        """Whether the current user may delete (RFC §4)."""
        return self._has_capability("build.delete")

    @property
    def can_update(self) -> bool:
        """Whether the current user may update (RFC §4)."""
        return self._has_capability("build.update")

    @property
    def can_add_collaborator(self) -> bool:
        """Whether the current user may add_collaborator (RFC §4)."""
        return self._has_capability("build.add_collaborator")

    @property
    def can_remove_collaborator(self) -> bool:
        """Whether the current user may remove_collaborator (RFC §4)."""
        return self._has_capability("build.remove_collaborator")

    @property
    def can_confirm_config(self) -> bool:
        """Whether the current user may confirm_config (RFC §4)."""
        return self._has_capability("build.confirm_config")

    @property
    def can_upload_config(self) -> bool:
        """Whether the current user may upload_config (RFC §4)."""
        return self._has_capability("build.upload_config")

    @property
    def can_unshare(self) -> bool:
        """Whether the current user may unshare (RFC §4)."""
        return self._has_capability("build.unshare")

    @property
    def can_share(self) -> bool:
        """Whether the current user may share (RFC §4)."""
        return self._has_capability("build.share")

    async def delete(self) -> "Build":
        """build.delete"""
        data = await self._ctx.transport.request("DELETE", f"/v1/builds/{self.id}")
        self._ctx.hydrate("Build", data)
        return self

    async def update(self, body: dict[str, Any]) -> "Build":
        """build.update"""
        data = await self._ctx.transport.request("PATCH", f"/v1/builds/{self.id}", body=body)
        self._ctx.hydrate("Build", data)
        return self

    async def collaborators_add(self, body: dict[str, Any]) -> "Build":
        """build.collaborators.add"""
        data = await self._ctx.transport.request("POST", f"/v1/builds/{self.id}/collaborators", body=body)
        self._ctx.hydrate("Build", data)
        return self

    async def collaborators_remove(self) -> "Build":
        """build.collaborators.remove"""
        data = await self._ctx.transport.request("DELETE", f"/v1/builds/{self.id}/collaborators/{self.id}")
        self._ctx.hydrate("Build", data)
        return self

    async def config_confirm(self, body: dict[str, Any]) -> "Build":
        """build.config.confirm"""
        data = await self._ctx.transport.request("POST", f"/v1/builds/{self.id}/config/confirm", body=body)
        self._ctx.hydrate("Build", data)
        return self

    async def config_upload(self, body: dict[str, Any]) -> "Build":
        """build.config.upload"""
        data = await self._ctx.transport.request("POST", f"/v1/builds/{self.id}/config/upload", body=body)
        self._ctx.hydrate("Build", data)
        return self

    async def unshare(self) -> "Build":
        """build.unshare"""
        data = await self._ctx.transport.request("DELETE", f"/v1/builds/{self.id}/share")
        self._ctx.hydrate("Build", data)
        return self

    async def share(self) -> "Build":
        """build.share"""
        data = await self._ctx.transport.request("POST", f"/v1/builds/{self.id}/share")
        self._ctx.hydrate("Build", data)
        return self
