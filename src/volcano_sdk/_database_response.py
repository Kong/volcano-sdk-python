"""Validate database response envelopes shared by queries and realtime fetch."""

from collections.abc import Mapping
from typing import TypeGuard, cast

_INVALID_DATABASE_ROWS = "Expected a list of database rows with string keys"


def _is_database_row(value: object) -> TypeGuard[dict[str, object]]:
    if not isinstance(value, dict):
        return False
    row = cast("dict[object, object]", value)
    return all(isinstance(key, str) for key in row)


def database_rows(payload: object) -> list[dict[str, object]]:
    """Validate the server database envelope and preserve row objects.

    Returns:
        Rows with string keys.

    Raises:
        TypeError: The payload is not a valid database envelope.

    """
    if not isinstance(payload, Mapping):
        raise TypeError(_INVALID_DATABASE_ROWS)
    values = cast("Mapping[object, object]", payload)
    raw_rows = values.get("data")
    if not isinstance(raw_rows, list):
        raise TypeError(_INVALID_DATABASE_ROWS)
    rows: list[dict[str, object]] = []
    for row in cast("list[object]", raw_rows):
        if not _is_database_row(row):
            raise TypeError(_INVALID_DATABASE_ROWS)
        rows.append(row)
    return rows
