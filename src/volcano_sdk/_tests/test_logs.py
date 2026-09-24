from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

import pytest

from volcano_sdk import ServerError, Session, VolcanoClient
from volcano_sdk.logs import Logs, LogsTransport

from .fixtures.invalid_arguments import non_json_log_request, non_mapping_log_request
from .transport_fixtures import RejectingTransport
from .typing import TYPE_CHECKING, cast, get_origin, get_type_hints

if TYPE_CHECKING:
    from volcano_sdk.models import JSONValue


@dataclass(frozen=True)
class FakeResponse:
    status_code: int
    payload: object
    headers: dict[str, str]
    content: bytes = b""


class FakeLogsTransport(RejectingTransport):
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []
        self.search_response: FakeResponse = FakeResponse(
            200,
            {
                "data": [
                    {
                        "id": "event-1",
                        "timestamp": "2026-09-02T12:00:00Z",
                        "body": {"message": "ready"},
                        "resource": {"type": "function", "id": "function-1"},
                    }
                ],
                "limit": 25,
                "has_more": True,
                "next_cursor": "cursor-2",
            },
            {},
        )
        self.activity_response: FakeResponse = FakeResponse(
            200,
            {
                "data": [
                    {
                        "start_time": "2026-09-02T12:00:00Z",
                        "end_time": "2026-09-02T12:05:00Z",
                        "counts": {
                            "levels": {"info": 2},
                            "regions": {"us-east-1": 2},
                            "resource_ids": {"function-1": 2},
                        },
                        "total": 2,
                    }
                ],
                "total": 2,
            },
            {},
        )

    def search_project_logs(self, **kwargs: object) -> FakeResponse:
        self.calls.append(("searchProjectLogs", kwargs))
        return self.search_response

    def get_project_log_activity(self, **kwargs: object) -> FakeResponse:
        self.calls.append(("getProjectLogActivity", kwargs))
        return self.activity_response


def logs_client(transport: FakeLogsTransport) -> VolcanoClient:
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
    )
    _ = client.auth.set_session(
        Session(
            access_token="access-token", refresh_token="refresh-token", user_id="user-1"
        )
    )
    return client


def test_log_public_request_annotations_resolve_at_runtime() -> None:
    methods = (
        Logs.search,
        Logs.activity,
        LogsTransport.search_project_logs,
        LogsTransport.get_project_log_activity,
    )
    for method in methods:
        annotation = cast("object", get_type_hints(method)["request"])
        assert get_origin(annotation) is Mapping


def test_logs_requires_a_transport_with_log_methods() -> None:
    client = VolcanoClient(anon_key="anon-key", _transport=RejectingTransport())
    _ = client.auth.set_session(
        Session(
            access_token="access-token", refresh_token="refresh-token", user_id="user-1"
        )
    )

    with pytest.raises(TypeError, match="Transport does not support project logs"):
        _ = client.logs.search("project-1", {"resource": {"type": "function"}})


def test_logs_search_returns_an_immutable_page() -> None:
    transport = FakeLogsTransport()
    request: Mapping[str, JSONValue] = {
        "resource": {"type": "function"},
        "limit": 25,
    }

    result = logs_client(transport).logs.search("project-1", request)

    assert result.limit == 25
    assert result.has_more is True
    assert result.next_cursor == "cursor-2"
    assert result.data[0]["body"] == {"message": "ready"}
    assert isinstance(result.data[0], MappingProxyType)
    assert isinstance(result.data[0]["body"], MappingProxyType)
    assert transport.calls == [
        (
            "searchProjectLogs",
            {
                "authorization": "access-token",
                "project_id": "project-1",
                "request": request,
            },
        )
    ]


def test_logs_activity_returns_immutable_buckets() -> None:
    transport = FakeLogsTransport()
    request: Mapping[str, JSONValue] = {
        "resource": {"type": "function"},
        "bucket_count": 12,
    }

    result = logs_client(transport).logs.activity("project-1", request)

    assert result.total == 2
    assert result.data[0]["counts"] == {
        "levels": {"info": 2},
        "regions": {"us-east-1": 2},
        "resource_ids": {"function-1": 2},
    }
    assert isinstance(result.data[0]["counts"], MappingProxyType)
    assert transport.calls[0] == (
        "getProjectLogActivity",
        {
            "authorization": "access-token",
            "project_id": "project-1",
            "request": request,
        },
    )


@pytest.mark.parametrize("project_id", ["", "   "])
def test_logs_rejects_an_empty_project_id(project_id: str) -> None:
    transport = FakeLogsTransport()

    with pytest.raises(ValueError, match="project_id"):
        _ = logs_client(transport).logs.search(
            project_id,
            {"resource": {"type": "function"}},
        )

    assert transport.calls == []


def test_logs_rejects_a_non_mapping_request() -> None:
    transport = FakeLogsTransport()

    with pytest.raises(TypeError, match="mapping"):
        non_mapping_log_request(logs_client(transport).logs)

    assert transport.calls == []


@pytest.mark.parametrize(
    "invalid_request",
    [
        {1: "invalid"},
        {"resource": object()},
        {"resource": {1: "invalid"}},
        *({"resource": value} for value in (math.nan, math.inf, -math.inf)),
    ],
)
def test_logs_rejects_non_json_requests(invalid_request: object) -> None:
    transport = FakeLogsTransport()

    with pytest.raises(TypeError, match="Log request must be a mapping"):
        non_json_log_request(logs_client(transport).logs, invalid_request)

    assert transport.calls == []


def test_logs_snapshots_nested_request_values() -> None:
    transport = FakeLogsTransport()
    nested: list[JSONValue] = ["first"]
    request: Mapping[str, JSONValue] = {
        "resource": {"ids": nested, "kinds": ("function",)}
    }

    _ = logs_client(transport).logs.search("project-1", request)
    nested.append("second")

    sent = transport.calls[0][1]["request"]
    assert sent == {"resource": {"ids": ("first",), "kinds": ("function",)}}


def test_logs_maps_platform_errors() -> None:
    transport = FakeLogsTransport()
    transport.search_response = FakeResponse(
        503,
        {"error": "logs unavailable", "code": "logs_unavailable"},
        {},
    )

    with pytest.raises(ServerError, match="logs unavailable") as raised:
        _ = logs_client(transport).logs.search(
            "project-1",
            {"resource": {"type": "function"}},
        )

    assert raised.value.code == "logs_unavailable"
