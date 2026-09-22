from __future__ import annotations

import httpx
import pytest
from test_logs import FakeLogsTransport, FakeResponse, logs_client
from test_logs_refresh import make_client


@pytest.mark.parametrize("operation", ["search", "activity"])
@pytest.mark.parametrize("payload", [None, [], "invalid", 1, True])
def test_logs_reject_non_object_responses(operation: str, payload: object) -> None:
    transport = FakeLogsTransport()
    transport.search_response = FakeResponse(200, payload, {})
    transport.activity_response = FakeResponse(200, payload, {})
    logs = logs_client(transport).logs
    read = logs.search if operation == "search" else logs.activity

    with pytest.raises(TypeError, match="Expected a complete log response"):
        read("project-1", {})


@pytest.mark.parametrize("operation", ["search", "activity"])
@pytest.mark.parametrize("data", [None, {}, "invalid", [None], [1], [[], {}]])
def test_logs_reject_invalid_response_rows(operation: str, data: object) -> None:
    transport = FakeLogsTransport()
    payload = {"data": data, "limit": 25, "has_more": False, "total": 0}
    transport.search_response = FakeResponse(200, payload, {})
    transport.activity_response = FakeResponse(200, payload, {})
    logs = logs_client(transport).logs
    read = logs.search if operation == "search" else logs.activity

    with pytest.raises(TypeError, match="Expected a complete log response"):
        read("project-1", {})


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
    transport = FakeLogsTransport()
    transport.search_response = FakeResponse(200, payload, {})

    def handle(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    client = make_client(handle) if native_transport else logs_client(transport)
    with pytest.raises(TypeError, match="Expected a complete log response"):
        client.logs.search(
            "00000000-0000-4000-8000-000000000001",
            {"resource": {"type": "function"}},
        )


@pytest.mark.parametrize("total", [None, "0", 0.0, True])
def test_logs_activity_rejects_invalid_totals(total: object) -> None:
    transport = FakeLogsTransport()
    transport.activity_response = FakeResponse(200, {"data": [], "total": total}, {})

    with pytest.raises(TypeError, match="Expected a complete log response"):
        logs_client(transport).logs.activity("project-1", {})
