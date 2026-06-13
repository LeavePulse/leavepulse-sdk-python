"""LeavePulse SDK — pagination.

``list``-style operations (``x-sdk-paginated``) return a :class:`Page` that is
both a snapshot of one page and an async iterator over all pages. Callers can do
``async for item in client.billing.orders.list(): ...`` without juggling
page/limit by hand, while still reading ``total``/``page``/``per_page`` off the
returned page — metadata a bare ``list`` would drop.
"""

from __future__ import annotations

from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Generic,
    Iterator,
    List,
    TypeVar,
)

T = TypeVar("T")

# A fetcher takes (page, per_page) and returns the next Page snapshot.
PageFetcher = Callable[[int, int], Awaitable["Page[Any]"]]


def _num(body: Any, key: str, fallback: int) -> int:
    """Read an integer envelope field, falling back when absent or non-numeric.
    Mirrors the TS ``pageDataFrom`` ``num`` helper."""
    if isinstance(body, dict):
        value = body.get(key)
        if isinstance(value, bool):
            return fallback
        if isinstance(value, (int, float)):
            return int(value)
    return fallback


def page_data_from(
    body: Any,
    hydrate: Callable[[List[Any]], List[T]],
    fetcher: PageFetcher,
    requested_page: int,
    requested_per_page: int,
) -> "Page[T]":
    """Coerce an arbitrary list-envelope body into a :class:`Page`, hydrating its
    ``items`` via ``hydrate`` and reading the canonical ``{total, page,
    per_page}`` fields (with sensible fallbacks). Generated list methods build
    the per-endpoint ``hydrate`` closure and pass the same ``fetcher`` they were
    called through, so ``Page.next()``/iteration advance correctly. The field
    plumbing lives here so it stays identical across every paginated method,
    mirroring the TS ``pageDataFrom``."""
    if isinstance(body, dict):
        raw_items = body.get("items")
    elif isinstance(body, list):
        raw_items = body
    else:
        raw_items = None
    raw_items = raw_items if isinstance(raw_items, list) else []
    items = hydrate(raw_items)
    return Page(
        items=items,
        total=_num(body, "total", len(items)),
        page=_num(body, "page", requested_page),
        per_page=_num(body, "per_page", requested_per_page),
        fetcher=fetcher,
    )


class Page(Generic[T]):
    """A single page of a paginated list, plus the envelope's pagination
    metadata, that is also an async iterator over the remaining pages."""

    def __init__(
        self,
        items: List[T],
        page: int,
        per_page: int,
        total: int,
        fetcher: PageFetcher,
    ) -> None:
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = total
        self._fetcher = fetcher

    @property
    def has_next(self) -> bool:
        """Whether a further page exists after this one."""
        return self.page * self.per_page < self.total

    async def next(self) -> "Page[T] | None":
        """Fetch the page after this one, or ``None`` when this is the last."""
        if not self.has_next:
            return None
        return await self._fetcher(self.page + 1, self.per_page)

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self) -> Iterator[T]:
        """Iterate this page's items only (no network)."""
        return iter(self.items)

    async def __aiter__(self) -> AsyncIterator[T]:
        """Iterate every item across all pages, fetching lazily."""
        current: "Page[T] | None" = self
        while current is not None:
            for item in current.items:
                yield item
            current = await current.next()
