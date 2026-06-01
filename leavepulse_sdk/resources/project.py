# Generated from the LeavePulse contract. Do not edit.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from leavepulse_sdk.resource import Resource

if TYPE_CHECKING:
    from leavepulse_sdk.client import ClientContext
    from leavepulse_sdk.resources.server import Server


class Project(Resource):
    """Project resource."""

    def __init__(self, data: dict[str, Any], ctx: "ClientContext") -> None:
        super().__init__(data)
        self._ctx = ctx

    async def refresh(self) -> "Project":
        """Re-fetch this Project and hydrate in place."""
        data = await self._ctx.transport.request("GET", f"/v1/projects/{self.id}")
        self._ctx.hydrate("Project", data, "project")
        return self

    @property
    def can_heart(self) -> bool:
        """Whether the current user may heart (RFC §4)."""
        return self._has_capability("project.heart")

    @property
    def can_thumb(self) -> bool:
        """Whether the current user may thumb (RFC §4)."""
        return self._has_capability("project.thumb")

    @property
    def can_manage_bridge(self) -> bool:
        """Whether the current user may manage_bridge (RFC §4)."""
        return self._has_capability("project.manage_bridge")

    @property
    def can_change_slug(self) -> bool:
        """Whether the current user may change_slug (RFC §4)."""
        return self._has_capability("project.change_slug")

    @property
    def can_rename(self) -> bool:
        """Whether the current user may rename (RFC §4)."""
        return self._has_capability("project.rename")

    @property
    def can_set_online_strategy(self) -> bool:
        """Whether the current user may set_online_strategy (RFC §4)."""
        return self._has_capability("project.set_online_strategy")

    @property
    def can_set_rollout_mode(self) -> bool:
        """Whether the current user may set_rollout_mode (RFC §4)."""
        return self._has_capability("project.set_rollout_mode")

    @property
    def servers(self) -> List["Server"]:
        """Related Server from cache (no network)."""
        return self._ctx.hydrate_many("Server", self._data.get("servers"))

    async def get_servers(self) -> List["Server"]:
        """Fetch related Server from the server."""
        await self.refresh()
        return self.servers

    async def comments_create(self, body: dict[str, Any], *, target_locale: str | None = None) -> "Project":
        """project.comments.create"""
        data = await self._ctx.transport.request("POST", f"/v1/community/projects/{self.id}/comments", body=body, query={"target_locale": target_locale})
        self._ctx.hydrate("Project", data)
        return self

    async def heart(self) -> "Project":
        """project.heart"""
        data = await self._ctx.transport.request("POST", f"/v1/community/projects/{self.id}/heart")
        self._ctx.hydrate("Project", data)
        return self

    async def thumb(self) -> "Project":
        """project.thumb"""
        data = await self._ctx.transport.request("POST", f"/v1/community/projects/{self.id}/thumb")
        self._ctx.hydrate("Project", data)
        return self

    async def bridge_update(self, body: dict[str, Any]) -> "Project":
        """project.bridge.update"""
        data = await self._ctx.transport.request("PATCH", f"/v1/discord/servers/{self.id}/bridge", body=body)
        self._ctx.hydrate("Project", data)
        return self

    async def bridge_import(self, body: dict[str, Any]) -> "Project":
        """project.bridge.import"""
        data = await self._ctx.transport.request("POST", f"/v1/discord/servers/{self.id}/import-pull", body=body)
        self._ctx.hydrate("Project", data)
        return self

    async def change_slug(self, body: dict[str, Any]) -> "Project":
        """project.change_slug"""
        data = await self._ctx.transport.request("POST", f"/v1/me/projects/{self.id}/actions/change-slug", body=body)
        self._ctx.hydrate("Project", data, "workspace")
        return self

    async def rename(self, body: dict[str, Any]) -> "Project":
        """project.rename"""
        data = await self._ctx.transport.request("POST", f"/v1/me/projects/{self.id}/actions/rename", body=body)
        self._ctx.hydrate("Project", data, "workspace")
        return self

    async def set_online_strategy(self, body: dict[str, Any]) -> "Project":
        """project.set_online_strategy"""
        data = await self._ctx.transport.request("POST", f"/v1/me/projects/{self.id}/actions/set-online-strategy", body=body)
        self._ctx.hydrate("Project", data, "workspace")
        return self

    async def set_rollout_mode(self, body: dict[str, Any]) -> "Project":
        """project.set_rollout_mode"""
        data = await self._ctx.transport.request("POST", f"/v1/me/projects/{self.id}/actions/set-rollout-mode", body=body)
        self._ctx.hydrate("Project", data, "workspace")
        return self

    async def policies_create(self, body: dict[str, Any]) -> "Project":
        """project.policies.create"""
        data = await self._ctx.transport.request("POST", f"/v1/projects/{self.id}/whitelist/policies", body=body)
        self._ctx.hydrate("Project", data)
        return self

    async def policies_delete(self) -> "Project":
        """project.policies.delete"""
        data = await self._ctx.transport.request("DELETE", f"/v1/projects/{self.id}/whitelist/policies/{self.id}")
        self._ctx.hydrate("Project", data)
        return self

    async def policies_update(self, body: dict[str, Any]) -> "Project":
        """project.policies.update"""
        data = await self._ctx.transport.request("PATCH", f"/v1/projects/{self.id}/whitelist/policies/{self.id}", body=body)
        self._ctx.hydrate("Project", data)
        return self

    async def policies_test(self, *, audience: str | None = None) -> "Project":
        """project.policies.test"""
        data = await self._ctx.transport.request("POST", f"/v1/projects/{self.id}/whitelist/policies/{self.id}/actions/test-notifications", query={"audience": audience})
        self._ctx.hydrate("Project", data)
        return self
