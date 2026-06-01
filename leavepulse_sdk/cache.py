"""LeavePulse SDK — identity map.

Guarantees one live object per (resource, id): ``await client.project(1)``
always returns the same instance, so ``p1 is p2``. The cache hands back the
existing instance and refreshes its data in place rather than minting a new
object. Per RFC 0001 §5 it is NOT a TTL auto-refetcher — properties never hit
the network; data changes only on an explicit ``refresh()`` / ``invalidate()``.
"""

from __future__ import annotations

from typing import Any, Callable, Protocol, runtime_checkable


@runtime_checkable
class Identified(Protocol):
    """A resource with a stable identity within its type."""

    @property
    def id(self) -> str | int: ...

    def _hydrate(self, data: Any) -> None: ...


class IdentityMap:
    """One instance per (type, id), hydrated in place on refresh."""

    def __init__(self) -> None:
        self._by_type: dict[str, dict[str, Identified]] = {}

    def upsert(
        self,
        type_: str,
        id_: str | int,
        data: Any,
        factory: Callable[[], Identified],
    ) -> Identified:
        bucket = self._by_type.setdefault(type_, {})
        key = str(id_)
        existing = bucket.get(key)
        if existing is not None:
            existing._hydrate(data)
            return existing
        created = factory()
        bucket[key] = created
        return created

    def get(self, type_: str, id_: str | int) -> Identified | None:
        return self._by_type.get(type_, {}).get(str(id_))

    def invalidate(self, type_: str, id_: str | int | None = None) -> None:
        if id_ is None:
            self._by_type.pop(type_, None)
            return
        self._by_type.get(type_, {}).pop(str(id_), None)

    def clear(self) -> None:
        self._by_type.clear()
