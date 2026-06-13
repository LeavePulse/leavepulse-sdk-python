# Generated from the LeavePulse contract. Do not edit.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from leavepulse_sdk.resource import Resource

if TYPE_CHECKING:
    from leavepulse_sdk.client import ClientContext


class Comment(Resource):
    """Comment resource."""

    def __init__(self, data: dict[str, Any], ctx: "ClientContext") -> None:
        super().__init__(data)
        self._ctx = ctx

    @property
    def can_delete(self) -> bool:
        """Whether the current user may delete (RFC §4)."""
        return self._has_capability("comment.delete")

    @property
    def can_like(self) -> bool:
        """Whether the current user may like (RFC §4)."""
        return self._has_capability("comment.like")

    async def delete(self) -> Any:
        """comment.delete"""
        return await self._ctx.transport.request("DELETE", f"/v1/community/projects/{self.id}/comments/{self.id}")

    async def like(self) -> Any:
        """comment.like"""
        return await self._ctx.transport.request("POST", f"/v1/community/projects/{self.id}/comments/{self.id}/like")

    async def reply(self, body: dict[str, Any], *, target_locale: str | None = None) -> "Comment":
        """comment.reply"""
        data = await self._ctx.transport.request("POST", f"/v1/community/projects/{self.id}/comments/{self.id}/replies", body=body, query={"target_locale": target_locale})
        self._ctx.hydrate("Comment", data)
        return self
