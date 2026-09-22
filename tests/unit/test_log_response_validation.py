from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import pytest
from test_logs import FakeLogsTransport, FakeResponse, logs_client
from test_logs_refresh import make_client

if TYPE_CHECKING:
    from volcano_sdk import VolcanoClient

PROJECT_ID = "00000000-0000-4000-8000-000000000001"
REQUEST = {"resource": {"type": "function"}}


def response_client(payload: object, *, native_transport: bool) -> VolcanoClient:
    def handle(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    if native_transport:
        return make_client(handle)
    transport = FakeLogsTransport()
    transport.search_response = FakeResponse(200, payload, {})
    transport.activity_response = FakeResponse(200, payload, {})
    return logs_client(transport)


@pytest.mark.parametrize("native_transport", [False, True])
@pytest.mark.parametrize("operation", ["search", "activity"])
@pytest.mark.parametrize("payload", [None, [], "invalid", 1, True])
def test_logs_reject_non_object_responses(
    operation: str, payload: object, *, native_transport: bool
) -> None:
    logs = response_client(payload, native_transport=native_transport).logs
    read = logs.search if operation == "search" else logs.activity

    with pytest.raises(TypeError, match="Expected a complete log response"):
        read(PROJECT_ID, REQUEST)


@pytest.mark.parametrize("native_transport", [False, True])
@pytest.mark.parametrize("operation", ["search", "activity"])
@pytest.mark.parametrize("data", [None, {}, "invalid", [None], [1], [[], {}]])
def test_logs_reject_invalid_response_rows(
    operation: str, data: object, *, native_transport: bool
) -> None:
    payload = {"data": data, "limit": 25, "has_more": False, "total": 0}
    logs = response_client(payload, native_transport=native_transport).logs
    read = logs.search if operation == "search" else logs.activity

    with pytest.raises(TypeError, match="Expected a complete log response"):
        read(PROJECT_ID, REQUEST)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("limit", None),
        ("limit", "25"),
        ("limit", 25.0),
        ("limit", True),
        ("has_more", None),
        ("has_more", "false"),
        ("has_more", 0),
        ("next_cursor", 1),
        ("next_cursor", []),
    ],
)
@pytest.mark.parametrize("native_transport", [False, True])
def test_logs_search_rejects_invalid_page_metadata(
    field: str, value: object, *, native_transport: bool
) -> None:
    payload: dict[str, object] = {"data": [], "limit": 25, "has_more": False}
    payload[field] = value
    client = response_client(payload, native_transport=native_transport)
    with pytest.raises(TypeError, match="Expected a complete log response"):
        client.logs.search(PROJECT_ID, REQUEST)


@pytest.mark.parametrize("native_transport", [False, True])
@pytest.mark.parametrize("total", [None, "0", 0.0, True])
def test_logs_activity_rejects_invalid_totals(
    total: object, *, native_transport: bool
) -> None:
    client = response_client(
        {"data": [], "total": total}, native_transport=native_transport
    )
    with pytest.raises(TypeError, match="Expected a complete log response"):
        client.logs.activity(PROJECT_ID, REQUEST)
