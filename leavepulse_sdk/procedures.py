# Generated from the LeavePulse contract. Do not edit.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from leavepulse_sdk.client import ClientContext


class AdminDiscoveryNs:
    """admin.discovery procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def candidates(self, *, page: int | None = None, limit: int | None = None, status: str | None = None, search: str | None = None, source: str | None = None, edition: str | None = None, region: str | None = None, min_sources: int | None = None, min_mc_online: int | None = None, min_discord_members: int | None = None, sort: str | None = None) -> Any:
        """admin.discovery.candidates"""
        return await self._ctx.transport.request("GET", "/v1/admin/discovery/candidates", query={"page": page, "limit": limit, "status": status, "search": search, "source": source, "edition": edition, "region": region, "min_sources": min_sources, "min_mc_online": min_mc_online, "min_discord_members": min_discord_members, "sort": sort})

    async def edit(self, candidate_id: int, body: dict[str, Any]) -> Any:
        """admin.discovery.edit"""
        return await self._ctx.transport.request("PATCH", f"/v1/admin/discovery/candidates/{candidate_id}", body=body)

    async def approve(self, candidate_id: int, *, show_in_public: bool | None = None, server_id: int | None = None) -> Any:
        """admin.discovery.approve"""
        return await self._ctx.transport.request("POST", f"/v1/admin/discovery/candidates/{candidate_id}/actions/approve", query={"show_in_public": show_in_public, "server_id": server_id})

    async def ignore(self, candidate_id: int, *, reason: str | None = None) -> Any:
        """admin.discovery.ignore"""
        return await self._ctx.transport.request("POST", f"/v1/admin/discovery/candidates/{candidate_id}/actions/ignore", query={"reason": reason})

    async def observations(self, candidate_id: int, *, limit: int | None = None) -> Any:
        """admin.discovery.observations"""
        return await self._ctx.transport.request("GET", f"/v1/admin/discovery/candidates/{candidate_id}/observations", query={"limit": limit})

    async def preview(self, candidate_id: int) -> Any:
        """admin.discovery.preview"""
        return await self._ctx.transport.request("GET", f"/v1/admin/discovery/candidates/{candidate_id}/preview")

    async def sources(self) -> Any:
        """admin.discovery.sources"""
        return await self._ctx.transport.request("GET", "/v1/admin/discovery/sources")

class AdminOverridesNs:
    """admin.overrides procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def list(self, server_id: int, *, start: str | None = None, end: str | None = None) -> Any:
        """admin.overrides.list"""
        return await self._ctx.transport.request("GET", f"/v1/admin/servers/{server_id}/status-overrides", query={"start": start, "end": end})

    async def create(self, server_id: int, body: dict[str, Any]) -> Any:
        """admin.overrides.create"""
        return await self._ctx.transport.request("POST", f"/v1/admin/servers/{server_id}/status-overrides", body=body)

    async def delete(self, server_id: int, override_id: str) -> Any:
        """admin.overrides.delete"""
        return await self._ctx.transport.request("DELETE", f"/v1/admin/servers/{server_id}/status-overrides/{override_id}")

class AdminPlayersNs:
    """admin.players procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def search(self, *, q: str | None = None, page: int | None = None, per_page: int | None = None) -> Any:
        """admin.players.search"""
        return await self._ctx.transport.request("GET", "/v1/admin/players", query={"q": q, "page": page, "per_page": per_page})

class AdminProjectsNs:
    """admin.projects procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def list(self, *, q: str | None = None, page: int | None = None, per_page: int | None = None) -> Any:
        """admin.projects.list"""
        return await self._ctx.transport.request("GET", "/v1/admin/projects", query={"q": q, "page": page, "per_page": per_page})

    async def delete(self, project_id: int) -> Any:
        """admin.projects.delete"""
        return await self._ctx.transport.request("DELETE", f"/v1/admin/projects/{project_id}")

    async def change_slug(self, project_id: int, body: dict[str, Any]) -> Any:
        """admin.projects.change_slug"""
        return await self._ctx.transport.request("POST", f"/v1/admin/projects/{project_id}/actions/change-slug", body=body)

    async def rename(self, project_id: int, body: dict[str, Any]) -> Any:
        """admin.projects.rename"""
        return await self._ctx.transport.request("POST", f"/v1/admin/projects/{project_id}/actions/rename", body=body)

    async def set_online_strategy(self, project_id: int, body: dict[str, Any]) -> Any:
        """admin.projects.set_online_strategy"""
        return await self._ctx.transport.request("POST", f"/v1/admin/projects/{project_id}/actions/set-online-strategy", body=body)

    async def set_rollout_mode(self, project_id: int, body: dict[str, Any]) -> Any:
        """admin.projects.set_rollout_mode"""
        return await self._ctx.transport.request("POST", f"/v1/admin/projects/{project_id}/actions/set-rollout-mode", body=body)

    async def transfer_ownership(self, project_id: int, body: dict[str, Any]) -> Any:
        """admin.projects.transfer_ownership"""
        return await self._ctx.transport.request("POST", f"/v1/admin/projects/{project_id}/actions/transfer-ownership", body=body)

class AdminRolesNs:
    """admin.roles procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def list(self) -> Any:
        """admin.roles.list"""
        return await self._ctx.transport.request("GET", "/v1/admin/roles")

    async def create(self, body: dict[str, Any]) -> Any:
        """admin.roles.create"""
        return await self._ctx.transport.request("POST", "/v1/admin/roles", body=body)

    async def delete(self, role_id: int) -> Any:
        """admin.roles.delete"""
        return await self._ctx.transport.request("DELETE", f"/v1/admin/roles/{role_id}")

    async def update(self, role_id: int, body: dict[str, Any]) -> Any:
        """admin.roles.update"""
        return await self._ctx.transport.request("PATCH", f"/v1/admin/roles/{role_id}", body=body)

class AdminServersNs:
    """admin.servers procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def list(self, *, page: int | None = None, per_page: int | None = None, q: str | None = None) -> Any:
        """admin.servers.list"""
        return await self._ctx.transport.request("GET", "/v1/admin/servers", query={"page": page, "per_page": per_page, "q": q})

    async def create(self, body: dict[str, Any]) -> Any:
        """admin.servers.create"""
        return await self._ctx.transport.request("POST", "/v1/admin/servers", body=body)

    async def stats(self) -> Any:
        """admin.servers.stats"""
        return await self._ctx.transport.request("GET", "/v1/admin/servers/stats")

    async def delete(self, server_id: int) -> Any:
        """admin.servers.delete"""
        return await self._ctx.transport.request("DELETE", f"/v1/admin/servers/{server_id}")

    async def update(self, server_id: int, body: dict[str, Any]) -> Any:
        """admin.servers.update"""
        return await self._ctx.transport.request("PATCH", f"/v1/admin/servers/{server_id}", body=body)

class AdminSessionsNs:
    """admin.sessions procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def revoke(self, session_id: int) -> Any:
        """admin.sessions.revoke"""
        return await self._ctx.transport.request("POST", f"/v1/admin/sessions/{session_id}/actions/revoke")

class AdminSystemNs:
    """admin.system procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def health(self) -> Any:
        """admin.system.health"""
        return await self._ctx.transport.request("GET", "/v1/admin/system/services-health")

class AdminUsersNs:
    """admin.users procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def list(self, *, page: int | None = None, per_page: int | None = None, q: str | None = None) -> Any:
        """admin.users.list"""
        return await self._ctx.transport.request("GET", "/v1/admin/users", query={"page": page, "per_page": per_page, "q": q})

    async def by_minecraft(self, uuid: str) -> Any:
        """admin.users.by_minecraft"""
        return await self._ctx.transport.request("GET", f"/v1/admin/users/by-minecraft-uuid/{uuid}")

    async def search(self, *, q: str | None = None, limit: int | None = None) -> Any:
        """admin.users.search"""
        return await self._ctx.transport.request("GET", "/v1/admin/users/search", query={"q": q, "limit": limit})

    async def get(self, user_id: int) -> Any:
        """admin.users.get"""
        return await self._ctx.transport.request("GET", f"/v1/admin/users/{user_id}")

    async def update(self, user_id: int, body: dict[str, Any]) -> Any:
        """admin.users.update"""
        return await self._ctx.transport.request("PATCH", f"/v1/admin/users/{user_id}", body=body)

    async def set_discord(self, user_id: int, body: dict[str, Any]) -> Any:
        """admin.users.set_discord"""
        return await self._ctx.transport.request("PATCH", f"/v1/admin/users/{user_id}/discord", body=body)

    async def create_offline_minecraft(self, user_id: int, body: dict[str, Any]) -> Any:
        """admin.users.create_offline_minecraft"""
        return await self._ctx.transport.request("POST", f"/v1/admin/users/{user_id}/minecraft-accounts/offline", body=body)

    async def delete_minecraft(self, user_id: int, account_id: int) -> Any:
        """admin.users.delete_minecraft"""
        return await self._ctx.transport.request("DELETE", f"/v1/admin/users/{user_id}/minecraft-accounts/{account_id}")

    async def update_minecraft(self, user_id: int, account_id: int, body: dict[str, Any]) -> Any:
        """admin.users.update_minecraft"""
        return await self._ctx.transport.request("PATCH", f"/v1/admin/users/{user_id}/minecraft-accounts/{account_id}", body=body)

    async def roles(self, user_id: int) -> Any:
        """admin.users.roles"""
        return await self._ctx.transport.request("GET", f"/v1/admin/users/{user_id}/roles")

    async def remove_role(self, user_id: int, role_slug: str) -> Any:
        """admin.users.remove_role"""
        return await self._ctx.transport.request("DELETE", f"/v1/admin/users/{user_id}/roles/{role_slug}")

    async def assign_role(self, user_id: int, role_slug: str) -> Any:
        """admin.users.assign_role"""
        return await self._ctx.transport.request("POST", f"/v1/admin/users/{user_id}/roles/{role_slug}")

    async def sessions(self, user_id: int) -> Any:
        """admin.users.sessions"""
        return await self._ctx.transport.request("GET", f"/v1/admin/users/{user_id}/sessions")

class AdminNs:
    """admin.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx
        self.discovery = AdminDiscoveryNs(ctx)
        self.overrides = AdminOverridesNs(ctx)
        self.players = AdminPlayersNs(ctx)
        self.projects = AdminProjectsNs(ctx)
        self.roles = AdminRolesNs(ctx)
        self.servers = AdminServersNs(ctx)
        self.sessions = AdminSessionsNs(ctx)
        self.system = AdminSystemNs(ctx)
        self.users = AdminUsersNs(ctx)

class AuthDeviceNs:
    """auth.device procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def approve(self, body: dict[str, Any]) -> Any:
        """auth.device.approve"""
        return await self._ctx.transport.request("POST", "/v1/auth/device/approve", body=body)

    async def start(self, body: dict[str, Any]) -> Any:
        """auth.device.start"""
        return await self._ctx.transport.request("POST", "/v1/auth/device/start", body=body)

    async def token(self, body: dict[str, Any]) -> Any:
        """auth.device.token"""
        return await self._ctx.transport.request("POST", "/v1/auth/device/token", body=body)

class AuthOauthNs:
    """auth.oauth procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def captcha_confirm(self, body: dict[str, Any]) -> Any:
        """auth.oauth.captcha_confirm"""
        return await self._ctx.transport.request("POST", "/auth/oauth/captcha/confirm", body=body, channel="auth")

    async def totp_confirm(self, body: dict[str, Any]) -> Any:
        """auth.oauth.totp_confirm"""
        return await self._ctx.transport.request("POST", "/auth/oauth/totp/confirm", body=body, channel="auth")

    async def callback(self, provider: str, body: dict[str, Any]) -> Any:
        """auth.oauth.callback"""
        return await self._ctx.transport.request("POST", f"/auth/oauth/{provider}/callback", body=body, channel="auth")

    async def start(self, provider: str) -> Any:
        """auth.oauth.start"""
        return await self._ctx.transport.request("GET", f"/auth/oauth/{provider}/start", channel="auth")

class AuthOauth2Ns:
    """auth.oauth2 procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def authorize(self, *, response_type: str | None = None, client_id: str | None = None, code_challenge: str | None = None, redirect_uri: str | None = None, scope: str | None = None, state: str | None = None, code_challenge_method: str | None = None) -> Any:
        """auth.oauth2.authorize"""
        return await self._ctx.transport.request("GET", "/auth/oauth/authorize", query={"response_type": response_type, "client_id": client_id, "code_challenge": code_challenge, "redirect_uri": redirect_uri, "scope": scope, "state": state, "code_challenge_method": code_challenge_method}, channel="auth")

    async def token(self) -> Any:
        """auth.oauth2.token"""
        return await self._ctx.transport.request("POST", "/auth/oauth/token", channel="auth")

class AuthTokensNs:
    """auth.tokens procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def list(self) -> Any:
        """auth.tokens.list"""
        return await self._ctx.transport.request("GET", "/auth/pat-tokens", channel="auth")

    async def create(self, body: dict[str, Any]) -> Any:
        """auth.tokens.create"""
        return await self._ctx.transport.request("POST", "/auth/pat-tokens", body=body, channel="auth")

    async def revoke(self, token_id: int) -> Any:
        """auth.tokens.revoke"""
        return await self._ctx.transport.request("DELETE", f"/auth/pat-tokens/{token_id}", channel="auth")

class AuthNs:
    """auth.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx
        self.device = AuthDeviceNs(ctx)
        self.oauth = AuthOauthNs(ctx)
        self.oauth2 = AuthOauth2Ns(ctx)
        self.tokens = AuthTokensNs(ctx)

    async def login(self, body: dict[str, Any]) -> Any:
        """auth.login"""
        return await self._ctx.transport.request("POST", "/auth/login", body=body, channel="auth")

    async def logout(self) -> Any:
        """auth.logout"""
        return await self._ctx.transport.request("POST", "/auth/logout", channel="auth")

    async def refresh(self, body: dict[str, Any]) -> Any:
        """auth.refresh"""
        return await self._ctx.transport.request("POST", "/auth/refresh", body=body, channel="auth")

    async def register(self, body: dict[str, Any]) -> Any:
        """auth.register"""
        return await self._ctx.transport.request("POST", "/auth/register", body=body, channel="auth")

    async def session(self) -> Any:
        """auth.session"""
        return await self._ctx.transport.request("POST", "/auth/session", channel="auth")

class BillingOrdersNs:
    """billing.orders procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def list(self, *, page: int | None = None, limit: int | None = None) -> List[Any]:
        """billing.orders.list"""
        data = await self._ctx.transport.request("GET", "/v1/billing/orders", query={"page": page, "limit": limit})
        items = data.get("items", []) if isinstance(data, dict) else []
        return self._ctx.hydrate_many("Order", items)

class BillingProductsNs:
    """billing.products procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def list(self) -> List[Any]:
        """billing.products.list"""
        data = await self._ctx.transport.request("GET", "/v1/billing/products")
        items = data.get("items", []) if isinstance(data, dict) else []
        return self._ctx.hydrate_many("Product", items)

class BillingSubscriptionsNs:
    """billing.subscriptions procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def list(self, *, page: int | None = None, limit: int | None = None) -> List[Any]:
        """billing.subscriptions.list"""
        data = await self._ctx.transport.request("GET", "/v1/billing/subscriptions", query={"page": page, "limit": limit})
        items = data.get("items", []) if isinstance(data, dict) else []
        return self._ctx.hydrate_many("Subscription", items)

class BillingNs:
    """billing.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx
        self.orders = BillingOrdersNs(ctx)
        self.products = BillingProductsNs(ctx)
        self.subscriptions = BillingSubscriptionsNs(ctx)

    async def checkout(self, body: dict[str, Any]) -> Any:
        """billing.checkout"""
        return await self._ctx.transport.request("POST", "/v1/billing/checkout", body=body)

class BuildsNs:
    """builds.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def create(self, body: dict[str, Any]) -> List[Any]:
        """builds.create"""
        data = await self._ctx.transport.request("POST", "/v1/builds", body=body)
        items = data.get("items", []) if isinstance(data, dict) else []
        return self._ctx.hydrate_many("Build", items)

    async def import_(self, body: dict[str, Any]) -> List[Any]:
        """builds.import"""
        data = await self._ctx.transport.request("POST", "/v1/builds/import", body=body)
        items = data.get("items", []) if isinstance(data, dict) else []
        return self._ctx.hydrate_many("Build", items)

    async def preview(self, share_token: str) -> List[Any]:
        """builds.preview"""
        data = await self._ctx.transport.request("GET", f"/v1/builds/preview/{share_token}")
        items = data.get("items", []) if isinstance(data, dict) else []
        return self._ctx.hydrate_many("Build", items)

    async def shared_with_me(self) -> List[Any]:
        """builds.shared_with_me"""
        data = await self._ctx.transport.request("GET", "/v1/builds/shared-with-me")
        items = data.get("items", []) if isinstance(data, dict) else []
        return self._ctx.hydrate_many("Build", items)

class DiscordLinkNs:
    """discord.link procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def complete(self, body: dict[str, Any]) -> Any:
        """discord.link.complete"""
        return await self._ctx.transport.request("POST", "/v1/discord/link/complete", body=body)

    async def session(self, *, state: str | None = None) -> Any:
        """discord.link.session"""
        return await self._ctx.transport.request("GET", "/v1/discord/link/session", query={"state": state})

    async def token(self, body: dict[str, Any]) -> Any:
        """discord.link.token"""
        return await self._ctx.transport.request("POST", "/v1/discord/link/token", body=body)

class DiscordNs:
    """discord.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx
        self.link = DiscordLinkNs(ctx)

class MonitoringMeNs:
    """monitoring.me procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def stats(self) -> Any:
        """monitoring.me.stats"""
        return await self._ctx.transport.request("GET", "/v1/monitoring/me/stats")

class MonitoringMeStatsNs:
    """monitoring.me.stats procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def unverified(self) -> Any:
        """monitoring.me.stats.unverified"""
        return await self._ctx.transport.request("GET", "/v1/monitoring/me/stats/unverified")

class MonitoringNs:
    """monitoring.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx
        self.me = MonitoringMeNs(ctx)
        self.me_stats = MonitoringMeStatsNs(ctx)

    async def landing(self) -> Any:
        """monitoring.landing"""
        return await self._ctx.transport.request("GET", "/v1/monitoring/landing")

class PasswordNs:
    """password.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def reset_confirm(self, body: dict[str, Any]) -> Any:
        """password.reset_confirm"""
        return await self._ctx.transport.request("POST", "/v1/password/reset/confirm", body=body)

    async def reset_request(self, body: dict[str, Any]) -> Any:
        """password.reset_request"""
        return await self._ctx.transport.request("POST", "/v1/password/reset/request", body=body)

class ProjectsNs:
    """projects.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def stats(self, *, q: str | None = None, edition: str | None = None, access: str | None = None, features: str | None = None, region: str | None = None, hosting: str | None = None, verified: bool | None = None) -> Any:
        """projects.stats"""
        return await self._ctx.transport.request("GET", "/v1/projects/stats", query={"q": q, "edition": edition, "access": access, "features": features, "region": region, "hosting": hosting, "verified": verified})

    async def bridge(self, server_id: int) -> Any:
        """projects.bridge"""
        return await self._ctx.transport.request("GET", f"/v1/discord/servers/{server_id}/bridge")

    async def bridge_update(self, server_id: int, body: dict[str, Any]) -> Any:
        """projects.bridge_update"""
        return await self._ctx.transport.request("PATCH", f"/v1/discord/servers/{server_id}/bridge", body=body)

    async def bridge_import(self, server_id: int, body: dict[str, Any]) -> Any:
        """projects.bridge_import"""
        return await self._ctx.transport.request("POST", f"/v1/discord/servers/{server_id}/import-pull", body=body)

    async def bridge_roles(self, server_id: int) -> Any:
        """projects.bridge_roles"""
        return await self._ctx.transport.request("GET", f"/v1/discord/servers/{server_id}/roles-catalog")

    async def projects_list(self, *, page: int | None = None, per_page: int | None = None) -> Any:
        """projects.projects_list"""
        return await self._ctx.transport.request("GET", "/v1/me/projects", query={"page": page, "per_page": per_page})

    async def projects_resolve(self, project_ref: str) -> Any:
        """projects.projects_resolve"""
        return await self._ctx.transport.request("GET", f"/v1/me/projects/resolve/{project_ref}")

    async def list(self, *, q: str | None = None, edition: str | None = None, access: str | None = None, features: str | None = None, region: str | None = None, hosting: str | None = None, verified: bool | None = None, has_build: bool | None = None, page: int | None = None, per_page: int | None = None, sort: str | None = None) -> Any:
        """projects.list"""
        return await self._ctx.transport.request("GET", "/v1/projects", query={"q": q, "edition": edition, "access": access, "features": features, "region": region, "hosting": hosting, "verified": verified, "has_build": has_build, "page": page, "per_page": per_page, "sort": sort})

    async def create(self, body: dict[str, Any]) -> Any:
        """projects.create"""
        return await self._ctx.transport.request("POST", "/v1/projects", body=body)

    async def resolve(self, project_ref: str) -> Any:
        """projects.resolve"""
        return await self._ctx.transport.request("GET", f"/v1/projects/resolve/{project_ref}")

class RbacNs:
    """rbac.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def batch_resolve(self, body: dict[str, Any]) -> Any:
        """rbac.batch_resolve"""
        return await self._ctx.transport.request("POST", "/v1/rbac/batch-resolve", body=body)

class ServersNs:
    """servers.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def resolve(self, server_ref: str) -> List[Any]:
        """servers.resolve"""
        data = await self._ctx.transport.request("GET", f"/v1/servers/resolve/{server_ref}")
        items = data.get("items", []) if isinstance(data, dict) else []
        return self._ctx.hydrate_many("Server", items)

class StatsNs:
    """stats.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def filter(self, *, q: str | None = None, edition: str | None = None, access: str | None = None, features: str | None = None, region: str | None = None, hosting: str | None = None, verified: bool | None = None, role: str | None = None) -> Any:
        """stats.filter"""
        return await self._ctx.transport.request("GET", "/v1/stats/filter", query={"q": q, "edition": edition, "access": access, "features": features, "region": region, "hosting": hosting, "verified": verified, "role": role})

    async def live(self) -> Any:
        """stats.live"""
        return await self._ctx.transport.request("GET", "/v1/stats/live")

class TicketsNs:
    """tickets.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def create(self, body: dict[str, Any]) -> List[Any]:
        """tickets.create"""
        data = await self._ctx.transport.request("POST", "/v1/community/tickets", body=body)
        items = data.get("items", []) if isinstance(data, dict) else []
        return self._ctx.hydrate_many("Ticket", items)

    async def mine(self, *, page: int | None = None, limit: int | None = None) -> List[Any]:
        """tickets.mine"""
        data = await self._ctx.transport.request("GET", "/v1/community/tickets/my", query={"page": page, "limit": limit})
        items = data.get("items", []) if isinstance(data, dict) else []
        return self._ctx.hydrate_many("Ticket", items)

class UpdatesNs:
    """updates.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def manifest(self, *, channel: str | None = None, platform: str | None = None, server_id: int | None = None) -> Any:
        """updates.manifest"""
        return await self._ctx.transport.request("GET", "/v1/launcher/updates/manifest", query={"channel": channel, "platform": platform, "server_id": server_id})

    async def manifest_upsert(self, channel: str, platform: str, body: dict[str, Any]) -> Any:
        """updates.manifest_upsert"""
        return await self._ctx.transport.request("PUT", f"/v1/launcher/updates/manifests/{channel}/{platform}", body=body)

    async def manifest_delete(self, channel: str, platform: str) -> Any:
        """updates.manifest_delete"""
        return await self._ctx.transport.request("POST", f"/v1/launcher/updates/manifests/{channel}/{platform}/delete")

    async def report(self, body: dict[str, Any]) -> Any:
        """updates.report"""
        return await self._ctx.transport.request("POST", "/v1/launcher/updates/report", body=body)

class UsersNs:
    """users.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def batch(self, body: dict[str, Any]) -> List[Any]:
        """users.batch"""
        data = await self._ctx.transport.request("POST", "/v1/users/public-profiles", body=body)
        items = data.get("items", []) if isinstance(data, dict) else []
        return self._ctx.hydrate_many("User", items)

    async def search(self, *, q: str | None = None, limit: int | None = None) -> List[Any]:
        """users.search"""
        data = await self._ctx.transport.request("GET", "/v1/users/search", query={"q": q, "limit": limit})
        items = data.get("items", []) if isinstance(data, dict) else []
        return self._ctx.hydrate_many("User", items)

    async def engagement(self, user_id: int) -> Any:
        """users.engagement"""
        return await self._ctx.transport.request("GET", f"/v1/community/users/{user_id}/engagement")

    async def activity_list(self, user_id: int, *, limit: int | None = None) -> Any:
        """users.activity_list"""
        return await self._ctx.transport.request("GET", f"/v1/community/users/{user_id}/recent-activity", query={"limit": limit})

class VerificationNs:
    """verification.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def start_dns(self, body: dict[str, Any]) -> Any:
        """verification.start_dns"""
        return await self._ctx.transport.request("POST", "/v1/servers/verification/dns", body=body)

    async def check_dns(self, body: dict[str, Any]) -> Any:
        """verification.check_dns"""
        return await self._ctx.transport.request("POST", "/v1/servers/verification/dns/check", body=body)

    async def start_motd(self, body: dict[str, Any]) -> Any:
        """verification.start_motd"""
        return await self._ctx.transport.request("POST", "/v1/servers/verification/motd", body=body)

    async def check_motd(self, body: dict[str, Any]) -> Any:
        """verification.check_motd"""
        return await self._ctx.transport.request("POST", "/v1/servers/verification/motd/check", body=body)

    async def start_plugin(self, body: dict[str, Any]) -> Any:
        """verification.start_plugin"""
        return await self._ctx.transport.request("POST", "/v1/servers/verification/plugin", body=body)

    async def check_plugin(self, server_id: int) -> Any:
        """verification.check_plugin"""
        return await self._ctx.transport.request("GET", f"/v1/servers/verification/plugin/{server_id}")

class WhitelistBindingsNs:
    """whitelist.bindings procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def create(self, body: dict[str, Any]) -> List[Any]:
        """whitelist.bindings.create"""
        data = await self._ctx.transport.request("POST", "/v1/whitelist/bindings", body=body)
        items = data.get("items", []) if isinstance(data, dict) else []
        return self._ctx.hydrate_many("Binding", items)

class WhitelistFormsNs:
    """whitelist.forms procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx

    async def list(self, *, project_id: int | None = None, search: str | None = None, page: int | None = None, per_page: int | None = None) -> List[Any]:
        """whitelist.forms.list"""
        data = await self._ctx.transport.request("GET", "/v1/whitelist/forms", query={"project_id": project_id, "search": search, "page": page, "per_page": per_page})
        items = data.get("items", []) if isinstance(data, dict) else []
        return self._ctx.hydrate_many("Form", items)

    async def create(self, body: dict[str, Any]) -> List[Any]:
        """whitelist.forms.create"""
        data = await self._ctx.transport.request("POST", "/v1/whitelist/forms", body=body)
        items = data.get("items", []) if isinstance(data, dict) else []
        return self._ctx.hydrate_many("Form", items)

class WhitelistNs:
    """whitelist.* procedures."""

    def __init__(self, ctx: "ClientContext") -> None:
        self._ctx = ctx
        self.bindings = WhitelistBindingsNs(ctx)
        self.forms = WhitelistFormsNs(ctx)
