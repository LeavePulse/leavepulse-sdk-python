# Generated from the LeavePulse contract. Do not edit.
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, List

from leavepulse_sdk.cache import Identified, IdentityMap
from leavepulse_sdk.errors import MalformedResponse
from leavepulse_sdk.resource import extract_id
from leavepulse_sdk.transport import Transport
from leavepulse_sdk.resources.application import Application
from leavepulse_sdk.resources.binding import Binding
from leavepulse_sdk.resources.build import Build
from leavepulse_sdk.resources.comment import Comment
from leavepulse_sdk.resources.form import Form
from leavepulse_sdk.resources.me import Me
from leavepulse_sdk.resources.order import Order
from leavepulse_sdk.resources.product import Product
from leavepulse_sdk.resources.project import Project
from leavepulse_sdk.resources.server import Server
from leavepulse_sdk.resources.session import Session
from leavepulse_sdk.resources.subscription import Subscription
from leavepulse_sdk.resources.ticket import Ticket
from leavepulse_sdk.resources.user import User
from leavepulse_sdk.procedures import AdminNs
from leavepulse_sdk.procedures import AuthNs
from leavepulse_sdk.procedures import BillingNs
from leavepulse_sdk.procedures import BuildsNs
from leavepulse_sdk.procedures import DiscordNs
from leavepulse_sdk.procedures import MonitoringNs
from leavepulse_sdk.procedures import PasswordNs
from leavepulse_sdk.procedures import ProjectsNs
from leavepulse_sdk.procedures import RbacNs
from leavepulse_sdk.procedures import ServersNs
from leavepulse_sdk.procedures import StatsNs
from leavepulse_sdk.procedures import TicketsNs
from leavepulse_sdk.procedures import UpdatesNs
from leavepulse_sdk.procedures import UsersNs
from leavepulse_sdk.procedures import VerificationNs
from leavepulse_sdk.procedures import WhitelistNs


@dataclass
class ClientContext:
    transport: Transport
    cache: IdentityMap
    hydrate: Callable[..., Any]
    hydrate_many: Callable[[str, Any], List[Any]]


class LeavePulse:
    """The LeavePulse SDK client."""

    def __init__(self, transport: Transport) -> None:
        cache = IdentityMap()
        self._ctx = ClientContext(
            transport=transport,
            cache=cache,
            hydrate=self._hydrate,
            hydrate_many=self._hydrate_many,
        )
        self.admin = AdminNs(self._ctx)
        self.auth = AuthNs(self._ctx)
        self.billing = BillingNs(self._ctx)
        self.builds = BuildsNs(self._ctx)
        self.discord = DiscordNs(self._ctx)
        self.monitoring = MonitoringNs(self._ctx)
        self.password = PasswordNs(self._ctx)
        self.projects = ProjectsNs(self._ctx)
        self.rbac = RbacNs(self._ctx)
        self.servers = ServersNs(self._ctx)
        self.stats = StatsNs(self._ctx)
        self.tickets = TicketsNs(self._ctx)
        self.updates = UpdatesNs(self._ctx)
        self.users = UsersNs(self._ctx)
        self.verification = VerificationNs(self._ctx)
        self.whitelist = WhitelistNs(self._ctx)

    async def build(self, id: int) -> Build:
        data = await self._ctx.transport.request("GET", f"/v1/builds/{id}")
        return self._hydrate("Build", data)

    async def form(self, id: int) -> Form:
        data = await self._ctx.transport.request("GET", f"/v1/whitelist/forms/{id}")
        return self._hydrate("Form", data)

    async def me(self, id: int) -> Me:
        data = await self._ctx.transport.request("GET", "/v1/me")
        return self._hydrate("Me", data)

    async def order(self, id: int) -> Order:
        data = await self._ctx.transport.request("GET", f"/v1/billing/orders/{id}")
        return self._hydrate("Order", data)

    async def project(self, id: int) -> Project:
        data = await self._ctx.transport.request("GET", f"/v1/projects/{id}")
        return self._hydrate("Project", data, "project")

    async def server(self, id: int) -> Server:
        data = await self._ctx.transport.request("GET", f"/v1/servers/{id}")
        return self._hydrate("Server", data)

    async def user(self, id: int) -> User:
        data = await self._ctx.transport.request("GET", f"/v1/users/{id}/public-profile")
        return self._hydrate("User", data)

    def _hydrate(self, type_: str, payload: Any, data_root: str | None = None) -> Any:
        factories: dict[str, Callable[[dict[str, Any]], Identified]] = {
            "Application": lambda d: Application(d, self._ctx),
            "Binding": lambda d: Binding(d, self._ctx),
            "Build": lambda d: Build(d, self._ctx),
            "Comment": lambda d: Comment(d, self._ctx),
            "Form": lambda d: Form(d, self._ctx),
            "Me": lambda d: Me(d, self._ctx),
            "Order": lambda d: Order(d, self._ctx),
            "Product": lambda d: Product(d, self._ctx),
            "Project": lambda d: Project(d, self._ctx),
            "Server": lambda d: Server(d, self._ctx),
            "Session": lambda d: Session(d, self._ctx),
            "Subscription": lambda d: Subscription(d, self._ctx),
            "Ticket": lambda d: Ticket(d, self._ctx),
            "User": lambda d: User(d, self._ctx),
        }
        factory = factories.get(type_)
        if factory is None:
            return payload
        data = payload
        if data_root and isinstance(payload, dict):
            core = payload.get(data_root, {})
            siblings = {k: v for k, v in payload.items() if k != data_root}
            data = {**core, **siblings}
        ident = extract_id(data)
        if ident == "":
            raise MalformedResponse(f"{type_} payload has no id field to identity-map on", payload)
        return self._ctx.cache.upsert(type_, ident, data, lambda: factory(data))

    def _hydrate_many(self, type_: str, raw: Any) -> List[Any]:
        if not isinstance(raw, list):
            return []
        return [self._hydrate(type_, item) for item in raw]
