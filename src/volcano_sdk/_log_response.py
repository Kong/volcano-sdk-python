"""Validate log response containers before generated model normalization."""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import TYPE_CHECKING, TypeGuard

if TYPE_CHECKING:
    from .models import JSONValue

INVALID_LOG_RESPONSE = "Expected a complete log response"


def _is_object_mapping(value: object) -> TypeGuard[Mapping[object, object]]:
    return isinstance(value, Mapping)


def _is_object_list(value: object) -> TypeGuard[list[object]]:
    return isinstance(value, list)


def _is_object_tuple(value: object) -> TypeGuard[tuple[object, ...]]:
    return isinstance(value, tuple)


def _is_json_scalar(value: object) -> TypeGuard[str | int | float | bool | None]:
    if isinstance(value, float):
        return math.isfinite(value)
    return value is None or isinstance(value, (str, int, bool))


def is_json_value(value: object) -> TypeGuard[JSONValue]:
    if _is_json_scalar(value):
        return True
    if _is_object_list(value):
        return all(is_json_value(item) for item in value)
    if _is_object_tuple(value):
        return all(is_json_value(item) for item in value)
    if _is_object_mapping(value):
        return all(
            isinstance(key, str) and is_json_value(item) for key, item in value.items()
        )
    return False


def response_values(payload: object) -> Mapping[str, object]:
    """Require a JSON object for the response envelope.

    Returns:
        The response fields without normalizing their values.

    Raises:
        TypeError: The response envelope is not an object.

    """
    if not _is_object_mapping(payload):
        raise TypeError(INVALID_LOG_RESPONSE)
    values: dict[str, object] = {}
    for key, value in payload.items():
        if not isinstance(key, str):
            raise TypeError(INVALID_LOG_RESPONSE)
        values[key] = value
    return values


def _row_values(item: object) -> Mapping[str, JSONValue]:
    if not _is_object_mapping(item):
        raise TypeError(INVALID_LOG_RESPONSE)
    row: dict[str, JSONValue] = {}
    for key, value in item.items():
        if not isinstance(key, str) or not is_json_value(value):
            raise TypeError(INVALID_LOG_RESPONSE)
        row[key] = value
    return row


def response_data(values: Mapping[str, object]) -> tuple[Mapping[str, JSONValue], ...]:
    """Require a list of objects without coercing empty mappings into lists.

    Returns:
        The validated rows in their original order.

    Raises:
        TypeError: The rows are not a list of objects.

    """
    raw_data = values.get("data")
    if not _is_object_list(raw_data):
        raise TypeError(INVALID_LOG_RESPONSE)
    return tuple(_row_values(item) for item in raw_data)


def search_metadata(values: Mapping[str, object]) -> tuple[int, bool, str | None]:
    """Require search pagination fields without coercing their values.

    Returns:
        The page limit, continuation flag, and optional cursor.

    Raises:
        TypeError: Required metadata is missing or has an invalid type.

    """
    limit = values.get("limit")
    has_more = values.get("has_more")
    next_cursor = values.get("next_cursor")
    if (
        not isinstance(limit, int)
        or isinstance(limit, bool)
        or not isinstance(has_more, bool)
        or (next_cursor is not None and not isinstance(next_cursor, str))
    ):
        raise TypeError(INVALID_LOG_RESPONSE)
    return limit, has_more, next_cursor


def activity_total(values: Mapping[str, object]) -> int:
    """Require the activity total without treating booleans as integers.

    Returns:
        The total reported by the server.

    Raises:
        TypeError: The total is missing or is not an integer.

    """
    total = values.get("total")
    if not isinstance(total, int) or isinstance(total, bool):
        raise TypeError(INVALID_LOG_RESPONSE)
    return total
