"""Database response rows stay unknown until their shape is checked."""

from __future__ import annotations

import httpx
import pytest
from test_database_refresh import make_client

from volcano_sdk.database import _database_rows


@pytest.mark.parametrize(
    "payload",
    [
        None,
        {},
        {"data": {}},
        {"data": [42]},
        {"data": [{1: "value"}]},
    ],
)
def test_database_rows_rejects_malformed_responses(payload: object) -> None:
    with pytest.raises(TypeError, match="Expected a list of database rows"):
        _database_rows(payload)


def test_database_rows_preserves_valid_row_objects() -> None:
    row: dict[str, object] = {"id": 1, "metadata": {"flags": [True, None]}}

    result = _database_rows({"data": [row]})

    assert result == [row]
    assert result[0] is row


@pytest.mark.parametrize("operation", ["select", "insert", "update", "delete"])
def test_database_operations_reject_missing_rows(operation: str) -> None:
    def handle(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"count": 0})

    table = make_client(handle).database("db").from_("items")
    operations = {
        "select": table.execute,
        "insert": table.insert({"id": 1}).execute,
        "update": table.update({"id": 1}).execute,
        "delete": table.delete().execute,
    }

    with pytest.raises(TypeError, match="Expected a list of database rows"):
        operations[operation]()
