# Generated from the LeavePulse contract. Do not edit.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from leavepulse_sdk.resource import Resource

if TYPE_CHECKING:
    from leavepulse_sdk.client import ClientContext


class Server(Resource):
    """Server resource."""

    def __init__(self, data: dict[str, Any], ctx: "ClientContext") -> None:
        super().__init__(data)
        self._ctx = ctx

    async def refresh(self) -> "Server":
        """Re-fetch this Server and hydrate in place."""
        data = await self._ctx.transport.request("GET", f"/v1/servers/{self.id}")
        self._ctx.hydrate("Server", data)
        return self

    @property
    def can_change_address(self) -> bool:
        """Whether the current user may change_address (RFC §4)."""
        return self._has_capability("server.change_address")

    @property
    def can_change_slug(self) -> bool:
        """Whether the current user may change_slug (RFC §4)."""
        return self._has_capability("server.change_slug")

    @property
    def can_force_ping(self) -> bool:
        """Whether the current user may force_ping (RFC §4)."""
        return self._has_capability("server.force_ping")

    @property
    def can_rename(self) -> bool:
        """Whether the current user may rename (RFC §4)."""
        return self._has_capability("server.rename")

    @property
    def can_set_bedrock_port(self) -> bool:
        """Whether the current user may set_bedrock_port (RFC §4)."""
        return self._has_capability("server.set_bedrock_port")

    @property
    def can_set_description(self) -> bool:
        """Whether the current user may set_description (RFC §4)."""
        return self._has_capability("server.set_description")

    @property
    def can_set_parent(self) -> bool:
        """Whether the current user may set_parent (RFC §4)."""
        return self._has_capability("server.set_parent")

    @property
    def can_set_ping_port(self) -> bool:
        """Whether the current user may set_ping_port (RFC §4)."""
        return self._has_capability("server.set_ping_port")

    @property
    def can_set_regions(self) -> bool:
        """Whether the current user may set_regions (RFC §4)."""
        return self._has_capability("server.set_regions")

    @property
    def can_set_role(self) -> bool:
        """Whether the current user may set_role (RFC §4)."""
        return self._has_capability("server.set_role")

    @property
    def can_set_show_description(self) -> bool:
        """Whether the current user may set_show_description (RFC §4)."""
        return self._has_capability("server.set_show_description")

    @property
    def can_set_show_in_public(self) -> bool:
        """Whether the current user may set_show_in_public (RFC §4)."""
        return self._has_capability("server.set_show_in_public")

    @property
    def can_set_team_enabled(self) -> bool:
        """Whether the current user may set_team_enabled (RFC §4)."""
        return self._has_capability("server.set_team_enabled")

    @property
    def can_set_version_override(self) -> bool:
        """Whether the current user may set_version_override (RFC §4)."""
        return self._has_capability("server.set_version_override")

    @property
    def can_manage_bot(self) -> bool:
        """Whether the current user may manage_bot (RFC §4)."""
        return self._has_capability("server.manage_bot")

    @property
    def can_manage_voting(self) -> bool:
        """Whether the current user may manage_voting (RFC §4)."""
        return self._has_capability("server.manage_voting")

    @property
    def can_set_maintenance(self) -> bool:
        """Whether the current user may set_maintenance (RFC §4)."""
        return self._has_capability("server.set_maintenance")

    @property
    def can_set_motd(self) -> bool:
        """Whether the current user may set_motd (RFC §4)."""
        return self._has_capability("server.set_motd")

    @property
    def can_manage_social(self) -> bool:
        """Whether the current user may manage_social (RFC §4)."""
        return self._has_capability("server.manage_social")

    @property
    def can_import(self) -> bool:
        """Whether the current user may import (RFC §4)."""
        return self._has_capability("server.import")

    async def change_address(self, body: dict[str, Any]) -> "Server":
        """server.change_address"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/actions/change-address", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def change_slug(self, body: dict[str, Any]) -> "Server":
        """server.change_slug"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/actions/change-slug", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def force_ping(self) -> "Server":
        """server.force_ping"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/actions/force-ping")
        self._ctx.hydrate("Server", data)
        return self

    async def rename(self, body: dict[str, Any]) -> "Server":
        """server.rename"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/actions/rename", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def set_bedrock_port(self, body: dict[str, Any]) -> "Server":
        """server.set_bedrock_port"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/actions/set-bedrock-port", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def set_description(self, body: dict[str, Any]) -> "Server":
        """server.set_description"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/actions/set-description", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def set_parent(self, body: dict[str, Any]) -> "Server":
        """server.set_parent"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/actions/set-parent", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def set_ping_port(self, body: dict[str, Any]) -> "Server":
        """server.set_ping_port"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/actions/set-ping-port", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def set_regions(self, body: dict[str, Any]) -> "Server":
        """server.set_regions"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/actions/set-regions", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def set_role(self, body: dict[str, Any]) -> "Server":
        """server.set_role"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/actions/set-role", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def set_show_description(self, body: dict[str, Any]) -> "Server":
        """server.set_show_description"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/actions/set-show-description", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def set_show_in_public(self, body: dict[str, Any]) -> "Server":
        """server.set_show_in_public"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/actions/set-show-in-public", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def set_team_enabled(self, body: dict[str, Any]) -> "Server":
        """server.set_team_enabled"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/actions/set-team-enabled", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def set_version_override(self, body: dict[str, Any]) -> "Server":
        """server.set_version_override"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/actions/set-version-override", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def bot_update(self, body: dict[str, Any]) -> "Server":
        """server.bot.update"""
        data = await self._ctx.transport.request("PATCH", f"/v1/servers/{self.id}/bot", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def issue_gateway_token(self, body: dict[str, Any]) -> "Server":
        """server.issue_gateway_token"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/gateway-token", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def icons_upload(self) -> "Server":
        """server.icons.upload"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/icon")
        self._ctx.hydrate("Server", data)
        return self

    async def icons_select(self, body: dict[str, Any]) -> "Server":
        """server.icons.select"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/icon/select", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def voting_update(self, body: dict[str, Any]) -> "Server":
        """server.voting.update"""
        data = await self._ctx.transport.request("PATCH", f"/v1/servers/{self.id}/integrations/voting", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def maintenance_update(self, body: dict[str, Any]) -> "Server":
        """server.maintenance.update"""
        data = await self._ctx.transport.request("PATCH", f"/v1/servers/{self.id}/maintenance", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def motd_update(self, body: dict[str, Any]) -> "Server":
        """server.motd.update"""
        data = await self._ctx.transport.request("PATCH", f"/v1/servers/{self.id}/motd", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def discord_unlink(self) -> "Server":
        """server.discord.unlink"""
        data = await self._ctx.transport.request("DELETE", f"/v1/servers/{self.id}/social/discord")
        self._ctx.hydrate("Server", data)
        return self

    async def discord_update(self, body: dict[str, Any]) -> "Server":
        """server.discord.update"""
        data = await self._ctx.transport.request("PATCH", f"/v1/servers/{self.id}/social/discord", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def discord_verify(self, body: dict[str, Any]) -> "Server":
        """server.discord.verify"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/social/discord/verify", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def social_update(self, body: dict[str, Any]) -> "Server":
        """server.social.update"""
        data = await self._ctx.transport.request("PATCH", f"/v1/servers/{self.id}/social/links", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def social_verify(self, body: dict[str, Any]) -> "Server":
        """server.social.verify"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/social/verify", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def subservers_issue_link_code(self) -> "Server":
        """server.subservers.issue_link_code"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/subservers/auto-link-code")
        self._ctx.hydrate("Server", data)
        return self

    async def members_create(self, body: dict[str, Any]) -> "Server":
        """server.members.create"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/team/members", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def members_delete(self) -> "Server":
        """server.members.delete"""
        data = await self._ctx.transport.request("DELETE", f"/v1/servers/{self.id}/team/members/{self.id}")
        self._ctx.hydrate("Server", data)
        return self

    async def members_update(self, body: dict[str, Any]) -> "Server":
        """server.members.update"""
        data = await self._ctx.transport.request("PATCH", f"/v1/servers/{self.id}/team/members/{self.id}", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def roles_create(self, body: dict[str, Any]) -> "Server":
        """server.roles.create"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/team/roles", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def roles_delete(self) -> "Server":
        """server.roles.delete"""
        data = await self._ctx.transport.request("DELETE", f"/v1/servers/{self.id}/team/roles/{self.id}")
        self._ctx.hydrate("Server", data)
        return self

    async def roles_update(self, body: dict[str, Any]) -> "Server":
        """server.roles.update"""
        data = await self._ctx.transport.request("PATCH", f"/v1/servers/{self.id}/team/roles/{self.id}", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def translations_delete(self) -> "Server":
        """server.translations.delete"""
        data = await self._ctx.transport.request("DELETE", f"/v1/servers/{self.id}/translations/{self.id}/{self.id}")
        self._ctx.hydrate("Server", data)
        return self

    async def translations_set(self, body: dict[str, Any]) -> "Server":
        """server.translations.set"""
        data = await self._ctx.transport.request("PATCH", f"/v1/servers/{self.id}/translations/{self.id}/{self.id}", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def whitelist_add_direct(self, body: dict[str, Any]) -> "Server":
        """server.whitelist.add_direct"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/whitelist/direct", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def whitelist_remove_direct(self) -> "Server":
        """server.whitelist.remove_direct"""
        data = await self._ctx.transport.request("DELETE", f"/v1/servers/{self.id}/whitelist/direct/{self.id}")
        self._ctx.hydrate("Server", data)
        return self

    async def whitelist_create_import(self, body: dict[str, Any]) -> "Server":
        """server.whitelist.create_import"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/whitelist/imports", body=body)
        self._ctx.hydrate("Server", data)
        return self

    async def whitelist_pull_minecraft_import(self, body: dict[str, Any]) -> "Server":
        """server.whitelist.pull_minecraft_import"""
        data = await self._ctx.transport.request("POST", f"/v1/servers/{self.id}/whitelist/imports/pull-minecraft", body=body)
        self._ctx.hydrate("Server", data)
        return self
