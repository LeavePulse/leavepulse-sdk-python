"""LeavePulse SDK — base resource.

Generated resource classes extend this. It holds the backing data, supports
in-place hydration for the identity map, and computes runtime capabilities
(RFC 0001 §4): a static capability is "usable" only if the user's permissions
carry it. Properties here never touch the network.

Wrapped responses (RFC §3.1 x-sdk-data-root) are normalized by the client
before a resource is constructed, so a resource always sees a flat dict with
``id`` at the top level.
"""

from __future__ import annotations

from typing import Any


def extract_id(data: dict[str, Any]) -> str | int:
    """Extract an instance id from a payload. Resources key on different
    fields: most use ``id``, some a domain id (``user_id``). Falls back to the
    first ``*_id`` field so identity-mapping works regardless of schema."""
    direct = data.get("id")
    if isinstance(direct, (str, int)):
        return direct
    for key, value in data.items():
        if key.endswith("_id") and isinstance(value, (str, int)):
            return value
    return ""


class Resource:
    """Base class for all id-bearing resources."""

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    @property
    def id(self) -> str | int:
        return extract_id(self._data)

    def _hydrate(self, data: Any) -> None:
        self._data = data

    def to_dict(self) -> dict[str, Any]:
        """Snapshot of the backing data (always from memory)."""
        return self._data

    def _has_capability(self, permission_code: str) -> bool:
        perms = self._data.get("user_permissions")
        return isinstance(perms, list) and permission_code in perms
