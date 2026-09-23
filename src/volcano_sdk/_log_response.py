"""Validate log response containers before generated model normalization."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from .models import JSONValue

INVALID_LOG_RESPONSE = "Expected a complete log response"


def response_values(payload: object) -> Mapping[str, object]:
    """Require a JSON object for the response envelope.

    Returns:
        The response fields without normalizing their values.

    Raises:
        TypeError: The response envelope is not an object.

    """
    if not isinstance(payload, Mapping):
        raise TypeError(INVALID_LOG_RESPONSE)
    return cast("Mapping[str, object]", payload)


def response_data(values: Mapping[str, object]) -> tuple[Mapping[str, JSONValue], ...]:
    """Require a list of objects without coercing empty mappings into lists.

    Returns:
        The validated rows in their original order.

    Raises:
        TypeError: The rows are not a list of objects.

    """
    raw_data = values.get("data")
    if not isinstance(raw_data, list):
        raise TypeError(INVALID_LOG_RESPONSE)
    data = cast("list[object]", raw_data)
    if any(not isinstance(item, Mapping) for item in data):
        raise TypeError(INVALID_LOG_RESPONSE)
    return tuple(cast("Mapping[str, JSONValue]", item) for item in data)


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
