"""Validate log response containers before generated model normalization."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from .models import JSONValue

INVALID_LOG_RESPONSE = "Expected a complete log response"


def response_values(payload: object) -> Mapping[str, object]:
    """Require a JSON object for the response envelope.

    Raises:
        TypeError: The response envelope is not an object.

    Returns:
        The response fields without normalizing their values.

    """
    if not isinstance(payload, Mapping):
        raise TypeError(INVALID_LOG_RESPONSE)
    return cast("Mapping[str, object]", payload)


def response_data(values: Mapping[str, object]) -> tuple[Mapping[str, JSONValue], ...]:
    """Require a list of objects without coercing empty mappings into lists.

    Raises:
        TypeError: The rows are not a list of objects.

    Returns:
        The validated rows in their original order.

    """
    raw_data = values.get("data")
    if not isinstance(raw_data, list):
        raise TypeError(INVALID_LOG_RESPONSE)
    data = cast("list[object]", raw_data)
    if any(not isinstance(item, Mapping) for item in data):
        raise TypeError(INVALID_LOG_RESPONSE)
    return tuple(cast("Mapping[str, JSONValue]", item) for item in data)
