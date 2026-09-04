from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, cast

import pytest

from volcano_sdk import ServerError, Session, VolcanoClient

if TYPE_CHECKING:
    from collections.abc import Mapping

    from volcano_sdk._transport import Transport
    from volcano_sdk.models import JSONValue


@dataclass(frozen=True)
class FakeResponse:
    status_code: int
    payload: Any
    headers: dict[str, str]
    content: bytes = b""


class FakeLogsTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.search_response = FakeResponse(
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
        self.activity_response = FakeResponse(
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

    def search_project_logs(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("searchProjectLogs", kwargs))
        return self.search_response

    def get_project_log_activity(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("getProjectLogActivity", kwargs))
        return self.activity_response


def logs_client(transport: FakeLogsTransport) -> VolcanoClient:
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=cast("Transport", transport),
    )
    client.auth.set_session(
        Session(
            access_token="access-token", refresh_token="refresh-token", user_id="user-1"
        )
    )
    return client


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
        logs_client(transport).logs.search(
            project_id,
            {"resource": {"type": "function"}},
        )

    assert transport.calls == []


def test_logs_rejects_a_non_mapping_request() -> None:
    transport = FakeLogsTransport()

    with pytest.raises(TypeError, match="mapping"):
        logs_client(transport).logs.activity("project-1", cast("Any", []))

    assert transport.calls == []


def test_logs_maps_platform_errors() -> None:
    transport = FakeLogsTransport()
    transport.search_response = FakeResponse(
        503,
        {"error": "logs unavailable", "code": "logs_unavailable"},
        {},
    )

    with pytest.raises(ServerError, match="logs unavailable") as raised:
        logs_client(transport).logs.search(
            "project-1",
            {"resource": {"type": "function"}},
        )

    assert raised.value.code == "logs_unavailable"
