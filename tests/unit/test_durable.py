from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, cast

import pytest

from volcano_sdk import (
    ConflictError,
    NotFoundError,
    ServerError,
    Session,
    VolcanoClient,
)
from volcano_sdk._transport import DurableExecutionListRequest

if TYPE_CHECKING:
    from volcano_sdk._transport import Transport

EXECUTION_ID = "00000000-0000-4000-8000-0000000000e1"
PROJECT_ID = "00000000-0000-4000-8000-000000000001"


@dataclass(frozen=True)
class FakeResponse:
    status_code: int
    payload: Any
    headers: dict[str, str]
    content: bytes = b""


def running_execution(**overrides: Any) -> dict[str, Any]:
    execution = {
        "id": EXECUTION_ID,
        "function_id": "00000000-0000-4000-8000-000000000040",
        "name": "order-42",
        "status": "running",
        "region": "aws-us-east-1",
        "created_at": "2026-09-02T12:00:00Z",
    }
    execution.update(overrides)
    return execution


class FakeDurableTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.start_response = FakeResponse(202, running_execution(), {})
        self.get_response = FakeResponse(
            200,
            running_execution(
                status="succeeded",
                result={"charged": "ch_1", "items": [1, 2]},
                completed_at="2026-09-02T12:04:30Z",
            ),
            {},
        )
        self.list_response = FakeResponse(
            200,
            {
                "data": [running_execution(), running_execution(status="succeeded")],
                "page": 1,
                "limit": 10,
                "total": 2,
                "has_more": False,
            },
            {},
        )
        self.stop_response = FakeResponse(200, running_execution(), {})

    def start_durable_execution_from_application(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("startDurableExecutionFromApplication", kwargs))
        return self.start_response

    def get_durable_execution(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("getDurableExecution", kwargs))
        return self.get_response

    def list_durable_executions(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("listDurableExecutions", kwargs))
        return self.list_response

    def stop_durable_execution(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("stopDurableExecution", kwargs))
        return self.stop_response


def durable_client(
    transport: FakeDurableTransport,
    *,
    anon_key: str = "anon-key",
    service_key: str | None = "service-key",
    session: bool = True,
) -> VolcanoClient:
    client = VolcanoClient(
        anon_key=anon_key,
        service_key=service_key,
        _transport=cast("Transport", transport),
    )
    if session:
        client.auth.set_session(
            Session(
                access_token="access-token",
                refresh_token="refresh-token",
                user_id="user-1",
            )
        )
    return client


def test_start_returns_the_accepted_execution_handle() -> None:
    transport = FakeDurableTransport()

    execution = durable_client(transport, session=False).durable.start(
        "order-pipeline",
        {"order_id": "order-42"},
    )

    assert execution.id == EXECUTION_ID
    assert execution.status == "running"
    assert execution.region == "aws-us-east-1"
    assert execution.created_at == datetime(2026, 9, 2, 12, 0, tzinfo=UTC)
    assert execution.is_terminal is False
    assert transport.calls == [
        (
            "startDurableExecutionFromApplication",
            {
                "authorization": "service-key",
                "function_id": "order-pipeline",
                "payload": {"order_id": "order-42"},
                "execution_name": None,
            },
        )
    ]


def test_start_sends_the_execution_name_as_an_idempotency_key() -> None:
    transport = FakeDurableTransport()

    durable_client(transport, session=False).durable.start(
        "order-pipeline",
        {"order_id": "order-42"},
        execution_name="order-42",
    )

    assert transport.calls[0][1]["execution_name"] == "order-42"


def test_start_prefers_a_session_over_the_service_key() -> None:
    transport = FakeDurableTransport()

    durable_client(transport).durable.start("order-pipeline")

    assert transport.calls[0][1]["authorization"] == "access-token"
    assert transport.calls[0][1]["payload"] == {}


def test_start_falls_back_to_the_anon_key() -> None:
    transport = FakeDurableTransport()
    anon_key = "ak-0000000000000000000000000000000000000000"

    durable_client(
        transport,
        anon_key=anon_key,
        service_key=None,
        session=False,
    ).durable.start("order-pipeline")

    assert transport.calls[0][1]["authorization"] == anon_key


def test_get_returns_the_result_of_a_succeeded_execution() -> None:
    transport = FakeDurableTransport()

    execution = durable_client(transport).durable.get(
        PROJECT_ID, "order-pipeline", EXECUTION_ID
    )

    assert execution.status == "succeeded"
    assert execution.is_terminal is True
    assert execution.result == {"charged": "ch_1", "items": (1, 2)}
    assert isinstance(execution.result, MappingProxyType)
    assert execution.completed_at == datetime(2026, 9, 2, 12, 4, 30, tzinfo=UTC)
    assert transport.calls == [
        (
            "getDurableExecution",
            {
                "authorization": "service-key",
                "project_id": PROJECT_ID,
                "function_id": "order-pipeline",
                "execution_id": EXECUTION_ID,
            },
        )
    ]


def test_get_reports_a_failed_execution_error() -> None:
    transport = FakeDurableTransport()
    transport.get_response = FakeResponse(
        200,
        running_execution(
            status="failed",
            error={"type": "CardDeclined", "message": "card was declined"},
            completed_at="2026-09-02T12:01:00Z",
        ),
        {},
    )

    execution = durable_client(transport).durable.get(
        PROJECT_ID, "order-pipeline", EXECUTION_ID
    )

    assert execution.status == "failed"
    assert execution.is_terminal is True
    assert execution.error is not None
    assert execution.error.type == "CardDeclined"
    assert execution.error.message == "card was declined"


def test_get_distinguishes_an_expired_result_from_an_empty_one() -> None:
    transport = FakeDurableTransport()
    transport.get_response = FakeResponse(
        200,
        running_execution(status="succeeded", result_expired=True),
        {},
    )

    execution = durable_client(transport).durable.get(
        PROJECT_ID, "order-pipeline", EXECUTION_ID
    )

    assert execution.result is None
    assert execution.result_expired is True


def test_unknown_is_a_terminal_status() -> None:
    transport = FakeDurableTransport()
    transport.get_response = FakeResponse(200, running_execution(status="unknown"), {})

    execution = durable_client(transport).durable.get(
        PROJECT_ID, "order-pipeline", EXECUTION_ID
    )

    assert execution.status == "unknown"
    assert execution.is_terminal is True


def test_list_returns_an_immutable_page() -> None:
    transport = FakeDurableTransport()

    page = durable_client(transport).durable.list(
        PROJECT_ID, "order-pipeline", status="running", page=1, limit=10
    )

    assert page.total == 2
    assert page.has_more is False
    assert len(page.executions) == 2
    assert isinstance(page.executions, tuple)
    assert page.executions[1].status == "succeeded"
    assert transport.calls == [
        (
            "listDurableExecutions",
            {
                "authorization": "service-key",
                "project_id": PROJECT_ID,
                "function_id": "order-pipeline",
                "request": DurableExecutionListRequest(
                    status="running", page=1, limit=10
                ),
            },
        )
    ]


def test_list_omits_filters_it_was_not_given() -> None:
    transport = FakeDurableTransport()

    durable_client(transport).durable.list(PROJECT_ID, "order-pipeline")

    assert transport.calls[0][1]["request"] == DurableExecutionListRequest()


def test_list_tolerates_an_empty_page() -> None:
    transport = FakeDurableTransport()
    transport.list_response = FakeResponse(
        200,
        {"data": [], "page": 1, "limit": 10, "total": 0, "has_more": False},
        {},
    )

    page = durable_client(transport).durable.list(PROJECT_ID, "order-pipeline")

    assert page.executions == ()
    assert page.total == 0


def test_stop_returns_the_execution_read_back_after_asking() -> None:
    transport = FakeDurableTransport()

    execution = durable_client(transport).durable.stop(
        PROJECT_ID, "order-pipeline", EXECUTION_ID
    )

    # Stopping is accepted rather than awaited, so the execution it answers
    # with commonly still reports running.
    assert execution.status == "running"
    assert transport.calls == [
        (
            "stopDurableExecution",
            {
                "authorization": "service-key",
                "project_id": PROJECT_ID,
                "function_id": "order-pipeline",
                "execution_id": EXECUTION_ID,
            },
        )
    ]


def test_stop_is_safe_to_repeat_on_a_finished_execution() -> None:
    transport = FakeDurableTransport()
    transport.stop_response = FakeResponse(
        200, running_execution(status="succeeded"), {}
    )

    execution = durable_client(transport).durable.stop(
        PROJECT_ID, "order-pipeline", EXECUTION_ID
    )

    assert execution.status == "succeeded"


@pytest.mark.parametrize("function_name", ["", "   "])
def test_start_rejects_an_empty_function_name_before_transport(
    function_name: str,
) -> None:
    transport = FakeDurableTransport()

    with pytest.raises(ValueError, match="function_name"):
        durable_client(transport).durable.start(function_name)

    assert transport.calls == []


@pytest.mark.parametrize("execution_name", ["", "   "])
def test_start_rejects_an_empty_execution_name_before_transport(
    execution_name: str,
) -> None:
    transport = FakeDurableTransport()

    with pytest.raises(ValueError, match="execution_name"):
        durable_client(transport).durable.start(
            "order-pipeline", execution_name=execution_name
        )

    assert transport.calls == []


@pytest.mark.parametrize(
    ("project_id", "function_name", "execution_id", "expected"),
    [
        ("", "order-pipeline", EXECUTION_ID, "project_id"),
        ("   ", "order-pipeline", EXECUTION_ID, "project_id"),
        (PROJECT_ID, "", EXECUTION_ID, "function_name"),
        (PROJECT_ID, "order-pipeline", "", "execution_id"),
        (PROJECT_ID, "order-pipeline", "   ", "execution_id"),
    ],
)
def test_owner_scoped_reads_reject_empty_path_segments(
    project_id: str, function_name: str, execution_id: str, expected: str
) -> None:
    # An empty segment would address the collection instead of the execution,
    # which is a different request rather than a failed one.
    transport = FakeDurableTransport()
    client = durable_client(transport)

    with pytest.raises(ValueError, match=expected):
        client.durable.get(project_id, function_name, execution_id)
    with pytest.raises(ValueError, match=expected):
        client.durable.stop(project_id, function_name, execution_id)

    assert transport.calls == []


def test_owner_scoped_reads_use_the_service_key_without_a_session() -> None:
    transport = FakeDurableTransport()
    client = durable_client(transport, session=False)

    client.durable.get(PROJECT_ID, "order-pipeline", EXECUTION_ID)

    assert transport.calls[0][1]["authorization"] == "service-key"


def test_owner_scoped_reads_refuse_without_a_platform_credential() -> None:
    transport = FakeDurableTransport()
    client = durable_client(transport, session=False, service_key=None)

    with pytest.raises(RuntimeError, match="No active session"):
        client.durable.get(PROJECT_ID, "order-pipeline", EXECUTION_ID)

    assert transport.calls == []


def test_get_raises_not_found_for_a_missing_execution() -> None:
    transport = FakeDurableTransport()
    transport.get_response = FakeResponse(
        404, {"error": "execution not found", "code": "not_found"}, {}
    )

    with pytest.raises(NotFoundError, match="execution not found") as raised:
        durable_client(transport).durable.get(
            PROJECT_ID, "order-pipeline", EXECUTION_ID
        )

    assert raised.value.status == 404
    assert raised.value.code == "not_found"


def test_start_raises_conflict_when_the_concurrency_cap_is_reached() -> None:
    transport = FakeDurableTransport()
    transport.start_response = FakeResponse(
        409,
        {"error": "too many running executions", "code": "durable_concurrency_cap"},
        {},
    )

    with pytest.raises(ConflictError, match="too many running executions") as raised:
        durable_client(transport, session=False).durable.start("order-pipeline")

    assert raised.value.status == 409
    assert raised.value.code == "durable_concurrency_cap"


def test_start_raises_for_a_platform_failure() -> None:
    transport = FakeDurableTransport()
    transport.start_response = FakeResponse(
        503,
        {"error": "durable execution is unavailable", "code": "durable_unavailable"},
        {},
    )

    with pytest.raises(ServerError, match="durable execution is unavailable") as raised:
        durable_client(transport, session=False).durable.start("order-pipeline")

    assert raised.value.status == 503
    assert raised.value.code == "durable_unavailable"


def test_a_malformed_execution_payload_is_refused() -> None:
    transport = FakeDurableTransport()
    transport.start_response = FakeResponse(202, {"id": EXECUTION_ID}, {})

    with pytest.raises(TypeError, match="complete durable execution"):
        durable_client(transport, session=False).durable.start("order-pipeline")


def test_owner_scoped_reads_reject_identifiers_that_are_not_uuids() -> None:
    """The transport sends the project and execution ids as UUIDs.

    Unchecked, a malformed one raised `badly formed hexadecimal UUID string`
    from inside the transport -- outside this package's error hierarchy and
    outside the facade's own messages.
    """
    transport = FakeDurableTransport()
    client = durable_client(transport)

    with pytest.raises(ValueError, match="project_id must be a UUID"):
        client.durable.get("not-a-uuid", "order-pipeline", EXECUTION_ID)
    with pytest.raises(ValueError, match="execution_id must be a UUID"):
        client.durable.get(PROJECT_ID, "order-pipeline", "exec-abc")

    assert transport.calls == []


def test_an_execution_has_a_stable_hash() -> None:
    execution = durable_client(FakeDurableTransport()).durable.get(
        PROJECT_ID, "order-pipeline", EXECUTION_ID
    )

    assert hash(execution) == hash(execution)
