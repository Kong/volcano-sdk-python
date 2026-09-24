"""Recursive JSON values and immutable response snapshots."""

from collections.abc import Mapping
from types import MappingProxyType
from typing import TypeAlias

JSONValue: TypeAlias = (
    str
    | int
    | float
    | bool
    | list["JSONValue"]
    | tuple["JSONValue", ...]
    | dict[str, "JSONValue"]
    | Mapping[str, "JSONValue"]
    | None
)


def freeze_json(value: JSONValue) -> JSONValue:
    """Recursively freeze JSON values exposed by immutable SDK models.

    Returns:
        The same scalar or an immutable container snapshot.

    """
    if isinstance(value, Mapping):
        return MappingProxyType({key: freeze_json(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(freeze_json(item) for item in value)
    return value
