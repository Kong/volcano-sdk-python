from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest
from test_database_refresh import make_client, rows_response

from volcano_sdk.database import FilterBuilder

if TYPE_CHECKING:
    import httpx

    from volcano_sdk.models import JSONValue


@pytest.mark.parametrize("operation", ["select", "update", "delete"])
def test_filter_snapshots_nested_mappings_lists_and_tuples(operation: str) -> None:
    requests: list[httpx.Request] = []
    tags: list[JSONValue] = ["original"]
    item: dict[str, JSONValue] = {"tags": tags}
    value: dict[str, JSONValue] = {"items": (item,)}

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return rows_response()

    original = make_client(handle).database("db").from_("items")
    filtered = original.eq("metadata", value)
    tags.append("changed")
    item["extra"] = True
    value["items"] = []
    operations = {
        "select": filtered.execute,
        "update": filtered.update({"title": "updated"}).execute,
        "delete": filtered.delete().execute,
    }

    assert operations[operation]() == [{"id": 1}]
    assert original.execute() == [{"id": 1}]
    assert len(requests) == 2
    assert requests[0].url.path.endswith(f"/{operation}")
    assert json.loads(requests[0].content)["filters"] == [
        {
            "column": "metadata",
            "operator": "eq",
            "value": {"items": [{"tags": ["original"]}]},
        }
    ]
    assert json.loads(requests[1].content) == {"table": "items"}


def test_filter_base_requires_a_concrete_builder() -> None:
    with pytest.raises(NotImplementedError):
        _ = FilterBuilder()._with_filters(())
