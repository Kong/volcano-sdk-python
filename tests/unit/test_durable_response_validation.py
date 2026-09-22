from __future__ import annotations

from datetime import UTC, datetime

import httpx
import pytest

from volcano_sdk import Session, VolcanoClient
from volcano_sdk._transport import GeneratedTransport
from volcano_sdk.durable import _datetime, _durable_execution, _durable_execution_page

PROJECT_ID = "00000000-0000-4000-8000-000000000001"
EXECUTION_ID = "00000000-0000-4000-8000-000000000002"


def execution_payload() -> dict[str, object]:
    return {
        "id": EXECUTION_ID,
        "function_id": "00000000-0000-4000-8000-000000000003",
        "name": "order-42",
        "status": "running",
        "region": "aws-us-east-1",
        "created_at": "2026-09-02T12:00:00Z",
    }


def client_for(payload: object) -> tuple[VolcanoClient, list[httpx.Request]]:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=payload)

    client = VolcanoClient(
        anon_key="anon",
        _transport=GeneratedTransport(
            api_url="https://api.volcano.test",
            httpx_transport=httpx.MockTransport(handle),
        ),
    )
    client.auth.set_session(Session("access", "refresh", "user"))
    return client, requests


@pytest.mark.parametrize("payload", [None, [], True, 42, "invalid"])
def test_execution_rejects_non_object_responses(payload: object) -> None:
    with pytest.raises(TypeError, match="complete durable execution"):
        _durable_execution(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("error", []),
        ("error", True),
        ("error", "failed"),
        ("created_at", "invalid"),
        ("created_at", "2026-13-01"),
        ("created_at", " "),
        ("completed_at", ""),
        ("completed_at", []),
        ("completed_at", 123),
        ("completed_at", "invalid"),
    ],
)
def test_execution_rejects_malformed_failure_and_timestamps(
    field: str, value: object
) -> None:
    payload = execution_payload()
    payload[field] = value
    with pytest.raises(TypeError, match="complete durable execution"):
        _durable_execution(payload)


@pytest.mark.parametrize(
    "payload",
    [
        None,
        [],
        True,
        {"data": {}},
        {"data": "invalid"},
        {"has_more": 1},
        {"has_more": "true"},
        {"page": True},
        {"limit": "10"},
        {"total": 2.5},
    ],
)
def test_pages_reject_malformed_collections_and_metadata(payload: object) -> None:
    with pytest.raises(TypeError, match="complete durable execution page"):
        _durable_execution_page(payload)


@pytest.mark.parametrize("payload", [{}, {"data": None}])
def test_empty_pages_default_missing_metadata(payload: dict[str, object]) -> None:
    page = _durable_execution_page(payload)

    assert page.executions == ()
    assert page.page == 0
    assert page.limit == 0
    assert page.total == 0
    assert page.has_more is False


@pytest.mark.parametrize(
    "timestamp", ["2026-09-02T12:00:00Z", "2026-09-02T14:00:00+02:00"]
)
def test_execution_retains_timestamp_offsets(timestamp: str) -> None:
    payload = execution_payload()
    payload["created_at"] = timestamp
    payload["completed_at"] = timestamp
    client, requests = client_for(payload)

    execution = client.durable.get(PROJECT_ID, "pipeline", EXECUTION_ID)

    expected = datetime.fromisoformat(timestamp)
    assert execution.created_at == expected
    assert execution.created_at.utcoffset() == expected.utcoffset()
    assert execution.completed_at == expected
    assert len(requests) == 1
    assert requests[0].headers["authorization"] == "Bearer access"


def test_timestamp_conversion_retains_transport_datetime_objects() -> None:
    timestamp = datetime(2026, 9, 2, 12, tzinfo=UTC)

    assert _datetime(timestamp) is timestamp
