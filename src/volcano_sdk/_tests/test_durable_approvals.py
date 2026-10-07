from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta, timezone
from types import MappingProxyType
from typing import TYPE_CHECKING

import httpx
import pytest

from volcano_sdk import (
    AuthenticationError,
    ConflictError,
    DurableApproval,
    DurableApprovalCounts,
    DurableApprovalDecider,
    DurableApprovalPage,
    DurableApprovalStats,
    NotFoundError,
    PermissionDeniedError,
    Session,
    VolcanoClient,
)
from volcano_sdk._durable_approval_response import (
    durable_approval,
    durable_approval_page,
    durable_approval_stats,
)
from volcano_sdk._transport import (
    DurableApprovalListRequest,
    DurableApprovalStatsRequest,
    GeneratedTransport,
)

from .fixtures.invalid_arguments import (
    assign_snapshot_value,
    non_string_approval_comment,
    unknown_approval_option,
    unknown_approval_status,
)
from .transport_fixtures import RejectingTransport

if TYPE_CHECKING:
    from collections.abc import Callable

    from volcano_sdk.durable import DurableApprovals

NAIVE = datetime(2026, 10, 1, tzinfo=UTC).replace(tzinfo=None)
PROJECT_ID = "00000000-0000-4000-8000-000000000001"
APPROVAL_ID = "00000000-0000-4000-8000-0000000000a1"
EXECUTION_ID = "00000000-0000-4000-8000-0000000000e1"
FUNCTION_ID = "00000000-0000-4000-8000-000000000040"
API_URL = "https://api.volcano.test"


@dataclass(frozen=True)
class FakeResponse:
    status_code: int
    payload: object
    headers: dict[str, str]
    content: bytes = b""


def pending_approval(**overrides: object) -> dict[str, object]:
    approval: dict[str, object] = {
        "id": APPROVAL_ID,
        "status": "pending",
        "name": "ship-order",
        "title": "Ship order 1234?",
        "description": "Customer asked for express shipping.",
        "details": {"order_id": "1234", "items": [1, 2]},
        "function": {"id": FUNCTION_ID, "name": "order-pipeline"},
        "execution": {"id": EXECUTION_ID, "name": "order-1234", "status": "running"},
        "requested_at": "2026-10-06T12:00:00Z",
        "expires_at": "2026-10-07T12:00:00Z",
        "decision": None,
    }
    approval.update(overrides)
    return approval


def approved_approval() -> dict[str, object]:
    return pending_approval(
        status="approved",
        decision={
            "comment": "Looks good",
            "decided_by": {"id": "user-7", "email": "ops@example.com"},
            "decided_at": "2026-10-06T12:05:00Z",
        },
    )


def counts(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "requested": 4,
        "pending": 1,
        "approved": 2,
        "denied": 1,
        "expired": 0,
        "cancelled": 0,
    }
    values.update(overrides)
    return values


def stats_payload() -> dict[str, object]:
    return {
        "from": "2026-09-06T00:00:00Z",
        "to": "2026-10-06T00:00:00Z",
        "counts": counts(),
        "approval_rate": 0.6667,
        "median_seconds_to_decision": 12.5,
        "p90_seconds_to_decision": 30,
        "functions": [
            {
                "function": {"id": FUNCTION_ID, "name": "order-pipeline"},
                "counts": counts(),
            },
            {"function": {"id": None, "name": "deleted-fn"}, "counts": counts()},
        ],
        "other_functions": counts(requested=0, pending=0, approved=0, denied=0),
        "daily": [{"date": "2026-10-05", "counts": counts()}],
    }


class FakeApprovalTransport(RejectingTransport):
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []
        self.list_response: FakeResponse = FakeResponse(
            200,
            {
                "data": [pending_approval(), approved_approval()],
                "page": 1,
                "limit": 10,
                "total": 2,
                "has_more": False,
            },
            {},
        )
        self.get_response: FakeResponse = FakeResponse(200, pending_approval(), {})
        self.stats_response: FakeResponse = FakeResponse(200, stats_payload(), {})
        self.decide_response: FakeResponse = FakeResponse(200, approved_approval(), {})

    def list_durable_approvals(self, **kwargs: object) -> FakeResponse:
        self.calls.append(("listDurableApprovals", kwargs))
        return self.list_response

    def get_durable_approval(self, **kwargs: object) -> FakeResponse:
        self.calls.append(("getDurableApproval", kwargs))
        return self.get_response

    def get_durable_approval_stats(self, **kwargs: object) -> FakeResponse:
        self.calls.append(("getDurableApprovalStats", kwargs))
        return self.stats_response

    def approve_durable_approval(self, **kwargs: object) -> FakeResponse:
        self.calls.append(("approveDurableApproval", kwargs))
        return self.decide_response

    def deny_durable_approval(self, **kwargs: object) -> FakeResponse:
        self.calls.append(("denyDurableApproval", kwargs))
        return self.decide_response


def approvals_client(
    transport: RejectingTransport | GeneratedTransport, *, session: bool = True
) -> VolcanoClient:
    client = VolcanoClient(
        anon_key="anon-key", service_key="service-key", _transport=transport
    )
    if session:
        _ = client.auth.set_session(
            Session(
                access_token="access-token",
                refresh_token="refresh-token",
                user_id="user-1",
            )
        )
    return client


def wire_client(
    respond: Callable[[httpx.Request], httpx.Response],
) -> tuple[VolcanoClient, list[httpx.Request]]:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return respond(request)

    client = approvals_client(
        GeneratedTransport(api_url=API_URL, httpx_transport=httpx.MockTransport(handle))
    )
    return client, requests


def test_approvals_require_a_transport_with_approval_methods() -> None:
    client = approvals_client(RejectingTransport())

    with pytest.raises(TypeError, match="Transport does not support durable approvals"):
        _ = client.durable.approvals.get(PROJECT_ID, APPROVAL_ID)


def test_get_returns_a_pending_approval() -> None:
    transport = FakeApprovalTransport()

    approval = approvals_client(transport).durable.approvals.get(
        f" {PROJECT_ID} ", APPROVAL_ID
    )

    assert approval == DurableApproval(
        id=APPROVAL_ID,
        status="pending",
        name="ship-order",
        title="Ship order 1234?",
        description="Customer asked for express shipping.",
        function=approval.function,
        execution=approval.execution,
        requested_at=datetime(2026, 10, 6, 12, tzinfo=UTC),
        expires_at=datetime(2026, 10, 7, 12, tzinfo=UTC),
        decision=None,
        details={"order_id": "1234", "items": (1, 2)},
    )
    assert approval.function.id == FUNCTION_ID
    assert approval.function.name == "order-pipeline"
    assert approval.execution.id == EXECUTION_ID
    assert approval.execution.name == "order-1234"
    assert approval.execution.status == "running"
    assert approval.is_pending is True
    assert transport.calls == [
        (
            "getDurableApproval",
            {
                "authorization": "access-token",
                "project_id": PROJECT_ID,
                "approval_id": APPROVAL_ID,
            },
        )
    ]


def test_get_freezes_the_details_the_workflow_attached() -> None:
    approval = approvals_client(FakeApprovalTransport()).durable.approvals.get(
        PROJECT_ID, APPROVAL_ID
    )

    assert isinstance(approval.details, MappingProxyType)
    with pytest.raises(TypeError):
        assign_snapshot_value(approval.details)


def test_get_reports_who_decided_and_when() -> None:
    transport = FakeApprovalTransport()
    transport.get_response = FakeResponse(200, approved_approval(), {})

    approval = approvals_client(transport).durable.approvals.get(
        PROJECT_ID, APPROVAL_ID
    )

    assert approval.status == "approved"
    assert approval.is_pending is False
    assert approval.decision is not None
    assert approval.decision.comment == "Looks good"
    assert approval.decision.decided_by == DurableApprovalDecider(
        id="user-7", email="ops@example.com"
    )
    assert approval.decision.decided_at == datetime(2026, 10, 6, 12, 5, tzinfo=UTC)


def test_get_keeps_an_approval_whose_function_and_execution_are_gone() -> None:
    transport = FakeApprovalTransport()
    payload = pending_approval(
        status="cancelled",
        function={"id": None, "name": "order-pipeline"},
        execution={"id": None, "name": "order-1234", "status": None},
        expires_at=None,
        decision={
            "comment": "",
            "decided_by": None,
            "decided_at": "2026-10-06T13:00:00Z",
        },
    )
    del payload["details"]
    transport.get_response = FakeResponse(200, payload, {})

    approval = approvals_client(transport).durable.approvals.get(
        PROJECT_ID, APPROVAL_ID
    )

    assert approval.function.id is None
    assert approval.execution.id is None
    assert approval.execution.status is None
    assert approval.expires_at is None
    assert approval.details is None
    assert approval.decision is not None
    assert approval.decision.decided_by is None


def test_list_returns_an_immutable_page_and_omits_unset_filters() -> None:
    transport = FakeApprovalTransport()

    page = approvals_client(transport).durable.approvals.list(PROJECT_ID)

    assert isinstance(page, DurableApprovalPage)
    assert [approval.status for approval in page.approvals] == ["pending", "approved"]
    assert isinstance(page.approvals, tuple)
    assert (page.page, page.limit, page.total, page.has_more) == (1, 10, 2, False)
    assert transport.calls == [
        (
            "listDurableApprovals",
            {
                "authorization": "access-token",
                "project_id": PROJECT_ID,
                "request": DurableApprovalListRequest(),
            },
        )
    ]


def test_list_forwards_every_filter() -> None:
    transport = FakeApprovalTransport()
    start = datetime(2026, 10, 1, tzinfo=UTC)
    end = datetime(2026, 10, 6, tzinfo=UTC)

    _ = approvals_client(transport).durable.approvals.list(
        PROJECT_ID,
        status="pending",
        function=" order-pipeline ",
        execution_id=EXECUTION_ID,
        from_=start,
        to=end,
        page=2,
        limit=50,
    )

    assert transport.calls[0][1]["request"] == DurableApprovalListRequest(
        status="pending",
        function="order-pipeline",
        execution_id=EXECUTION_ID,
        from_=start,
        to=end,
        page=2,
        limit=50,
    )


def test_stats_returns_counts_rates_and_breakdowns() -> None:
    transport = FakeApprovalTransport()

    stats = approvals_client(transport).durable.approvals.stats(
        PROJECT_ID, function="order-pipeline"
    )

    assert isinstance(stats, DurableApprovalStats)
    assert stats.from_ == datetime(2026, 9, 6, tzinfo=UTC)
    assert stats.to == datetime(2026, 10, 6, tzinfo=UTC)
    assert stats.counts == DurableApprovalCounts(
        requested=4, pending=1, approved=2, denied=1, expired=0, cancelled=0
    )
    assert stats.approval_rate == pytest.approx(0.6667)
    assert stats.median_seconds_to_decision == pytest.approx(12.5)
    assert stats.p90_seconds_to_decision == pytest.approx(30.0)
    assert isinstance(stats.p90_seconds_to_decision, float)
    assert [entry.function.name for entry in stats.functions] == [
        "order-pipeline",
        "deleted-fn",
    ]
    assert stats.functions[1].function.id is None
    assert stats.functions[0].counts.requested == 4
    assert stats.other_functions.requested == 0
    assert stats.daily[0].day == date(2026, 10, 5)
    assert stats.daily[0].counts.approved == 2
    assert transport.calls == [
        (
            "getDurableApprovalStats",
            {
                "authorization": "access-token",
                "project_id": PROJECT_ID,
                "request": DurableApprovalStatsRequest(function="order-pipeline"),
            },
        )
    ]


def test_stats_keeps_absent_rates_absent() -> None:
    transport = FakeApprovalTransport()
    payload = stats_payload()
    payload.update(
        approval_rate=None,
        median_seconds_to_decision=None,
        p90_seconds_to_decision=None,
        functions=[],
        daily=[],
    )
    transport.stats_response = FakeResponse(200, payload, {})

    stats = approvals_client(transport).durable.approvals.stats(PROJECT_ID)

    assert stats.approval_rate is None
    assert stats.median_seconds_to_decision is None
    assert stats.p90_seconds_to_decision is None
    assert stats.functions == ()
    assert stats.daily == ()
    assert transport.calls[0][1]["request"] == DurableApprovalStatsRequest()


@pytest.mark.parametrize("decide", ["approve", "deny"])
def test_a_decision_sends_its_comment(decide: str) -> None:
    transport = FakeApprovalTransport()
    approvals = approvals_client(transport).durable.approvals
    method = approvals.approve if decide == "approve" else approvals.deny

    approval = method(PROJECT_ID, APPROVAL_ID, comment="Ship it")

    assert approval.status == "approved"
    assert transport.calls == [
        (
            f"{decide}DurableApproval",
            {
                "authorization": "access-token",
                "project_id": PROJECT_ID,
                "approval_id": APPROVAL_ID,
                "comment": "Ship it",
            },
        )
    ]


@pytest.mark.parametrize("decide", ["approve", "deny"])
def test_a_decision_without_a_comment_sends_none(decide: str) -> None:
    transport = FakeApprovalTransport()
    approvals = approvals_client(transport).durable.approvals
    method = approvals.approve if decide == "approve" else approvals.deny

    _ = method(PROJECT_ID, APPROVAL_ID)

    assert transport.calls[0][1]["comment"] is None


def test_a_comment_at_the_limit_is_accepted() -> None:
    transport = FakeApprovalTransport()

    _ = approvals_client(transport).durable.approvals.approve(
        PROJECT_ID, APPROVAL_ID, comment="x" * 2000
    )

    assert transport.calls[0][1]["comment"] == "x" * 2000


@pytest.mark.parametrize("decide", ["approve", "deny"])
def test_a_comment_over_the_limit_is_refused_before_transport(decide: str) -> None:
    transport = FakeApprovalTransport()
    approvals = approvals_client(transport).durable.approvals
    method = approvals.approve if decide == "approve" else approvals.deny

    with pytest.raises(ValueError, match="comment must be at most 2000 characters"):
        _ = method(PROJECT_ID, APPROVAL_ID, comment="x" * 2001)
    assert transport.calls == []


def test_a_comment_that_is_not_a_string_is_refused_before_transport() -> None:
    transport = FakeApprovalTransport()

    with pytest.raises(TypeError) as caught:
        non_string_approval_comment(
            approvals_client(transport).durable.approvals, APPROVAL_ID
        )
    assert str(caught.value) == "comment must be a string"
    assert transport.calls == []


INVALID_ARGUMENTS: dict[str, tuple[Callable[[DurableApprovals], object], str]] = {
    "empty project": (
        lambda a: a.get("", APPROVAL_ID),
        "project_id must be a non-empty string",
    ),
    "get project": (
        lambda a: a.get("project", APPROVAL_ID),
        "project_id must be a UUID",
    ),
    "empty approval": (
        lambda a: a.get(PROJECT_ID, " "),
        "approval_id must be a non-empty string",
    ),
    "get approval": (
        lambda a: a.get(PROJECT_ID, "approval"),
        "approval_id must be a UUID",
    ),
    "approve approval": (
        lambda a: a.approve(PROJECT_ID, "approval"),
        "approval_id must be a UUID",
    ),
    "deny project": (
        lambda a: a.deny("project", APPROVAL_ID),
        "project_id must be a UUID",
    ),
    "list project": (lambda a: a.list("project"), "project_id must be a UUID"),
    "stats project": (lambda a: a.stats("project"), "project_id must be a UUID"),
    "list execution": (
        lambda a: a.list(PROJECT_ID, execution_id="execution"),
        "execution_id must be a UUID",
    ),
    "blank function": (
        lambda a: a.list(PROJECT_ID, function=" "),
        "function must be a non-empty string",
    ),
    "long function": (
        lambda a: a.stats(PROJECT_ID, function="f" * 256),
        "function must be at most 255 characters",
    ),
    "naive list from": (
        lambda a: a.list(PROJECT_ID, from_=NAIVE),
        "from_ must be a timezone-aware datetime",
    ),
    "naive list to": (
        lambda a: a.list(PROJECT_ID, to=NAIVE),
        "to must be a timezone-aware datetime",
    ),
    "naive stats from": (
        lambda a: a.stats(PROJECT_ID, from_=NAIVE),
        "from_ must be a timezone-aware datetime",
    ),
    "naive stats to": (
        lambda a: a.stats(PROJECT_ID, to=NAIVE),
        "to must be a timezone-aware datetime",
    ),
}


@pytest.mark.parametrize(
    ("call", "message"),
    [pytest.param(*case, id=name) for name, case in INVALID_ARGUMENTS.items()],
)
def test_invalid_arguments_are_refused_before_transport(
    call: Callable[[DurableApprovals], object], message: str
) -> None:
    transport = FakeApprovalTransport()
    approvals = approvals_client(transport).durable.approvals

    with pytest.raises(ValueError, match=f"^{re.escape(message)}$"):
        _ = call(approvals)
    assert transport.calls == []


def test_list_refuses_an_unknown_status_before_transport() -> None:
    transport = FakeApprovalTransport()

    with pytest.raises(
        ValueError,
        match=r"^status must be one of pending, approved, denied, expired, cancelled$",
    ):
        unknown_approval_status(approvals_client(transport).durable.approvals)
    assert transport.calls == []


def test_an_unknown_option_is_refused_before_transport() -> None:
    transport = FakeApprovalTransport()

    with pytest.raises(TypeError) as caught:
        unknown_approval_option(approvals_client(transport).durable.approvals)
    assert str(caught.value) == "unexpected option: sort, state"
    assert transport.calls == []


def test_a_function_at_the_name_limit_is_accepted() -> None:
    transport = FakeApprovalTransport()

    _ = approvals_client(transport).durable.approvals.list(
        PROJECT_ID, function="f" * 255
    )

    assert transport.calls[0][1]["request"] == DurableApprovalListRequest(
        function="f" * 255
    )


def test_approvals_refuse_a_service_key_alone() -> None:
    transport = FakeApprovalTransport()
    client = approvals_client(transport, session=False)

    with pytest.raises(RuntimeError, match="No active session"):
        _ = client.durable.approvals.get(PROJECT_ID, APPROVAL_ID)
    assert transport.calls == []


@pytest.mark.parametrize(
    ("status", "code", "expected"),
    [
        (403, None, PermissionDeniedError),
        (404, None, NotFoundError),
        (409, "approval_decided", ConflictError),
        (409, "approval_expired", ConflictError),
        (409, "approval_cancelled", ConflictError),
    ],
)
def test_decision_failures_raise_typed_errors(
    status: int, code: str | None, expected: type[Exception]
) -> None:
    transport = FakeApprovalTransport()
    body: dict[str, object] = {"error": "cannot decide"}
    if code is not None:
        body["code"] = code
    transport.decide_response = FakeResponse(status, body, {})

    with pytest.raises(expected, match="cannot decide") as caught:
        _ = approvals_client(transport).durable.approvals.deny(PROJECT_ID, APPROVAL_ID)

    assert type(caught.value) is expected
    assert getattr(caught.value, "code", None) == code


def test_permission_denied_is_an_authentication_error() -> None:
    error = PermissionDeniedError("denied", status=403)

    assert isinstance(error, AuthenticationError)


def test_get_raises_not_found_for_another_project_s_approval() -> None:
    transport = FakeApprovalTransport()
    transport.get_response = FakeResponse(404, {"error": "approval not found"}, {})

    with pytest.raises(NotFoundError, match="approval not found"):
        _ = approvals_client(transport).durable.approvals.get(PROJECT_ID, APPROVAL_ID)


def test_get_sends_the_owner_request_over_the_wire() -> None:
    client, requests = wire_client(
        lambda _r: httpx.Response(200, json=pending_approval())
    )

    approval = client.durable.approvals.get(PROJECT_ID, APPROVAL_ID)

    assert approval.id == APPROVAL_ID
    assert len(requests) == 1
    assert requests[0].method == "GET"
    assert str(requests[0].url) == (
        f"{API_URL}/projects/{PROJECT_ID}/durable-approvals/{APPROVAL_ID}"
    )
    assert requests[0].headers["authorization"] == "Bearer access-token"


def test_list_sends_filters_as_query_parameters() -> None:
    page = {
        "data": [pending_approval()],
        "page": 2,
        "limit": 5,
        "total": 6,
        "has_more": True,
    }
    client, requests = wire_client(lambda _r: httpx.Response(200, json=page))
    plus_two = timezone(timedelta(hours=2))

    result = client.durable.approvals.list(
        PROJECT_ID,
        status="approved",
        function="order-pipeline",
        execution_id=EXECUTION_ID,
        from_=datetime(2026, 10, 1, 8, tzinfo=plus_two),
        to=datetime(2026, 10, 6, tzinfo=UTC),
        page=2,
        limit=5,
    )

    assert result.page == 2
    assert result.has_more is True
    assert requests[0].method == "GET"
    assert requests[0].url.path == f"/projects/{PROJECT_ID}/durable-approvals"
    assert dict(requests[0].url.params) == {
        "status": "approved",
        "function": "order-pipeline",
        "execution_id": EXECUTION_ID,
        "from": "2026-10-01T08:00:00+02:00",
        "to": "2026-10-06T00:00:00+00:00",
        "page": "2",
        "limit": "5",
    }


def test_list_sends_no_filters_it_was_not_given() -> None:
    page: dict[str, object] = {
        "data": [],
        "page": 1,
        "limit": 10,
        "total": 0,
        "has_more": False,
    }
    client, requests = wire_client(lambda _r: httpx.Response(200, json=page))

    result = client.durable.approvals.list(PROJECT_ID)

    assert result.approvals == ()
    assert dict(requests[0].url.params) == {}


def test_stats_sends_its_window_as_query_parameters() -> None:
    client, requests = wire_client(lambda _r: httpx.Response(200, json=stats_payload()))

    stats = client.durable.approvals.stats(
        PROJECT_ID,
        function=FUNCTION_ID,
        from_=datetime(2026, 9, 6, tzinfo=UTC),
        to=datetime(2026, 10, 6, tzinfo=UTC),
    )

    assert stats.counts.requested == 4
    assert stats.daily[0].day == date(2026, 10, 5)
    assert requests[0].url.path == f"/projects/{PROJECT_ID}/durable-approvals/stats"
    assert dict(requests[0].url.params) == {
        "function": FUNCTION_ID,
        "from": "2026-09-06T00:00:00+00:00",
        "to": "2026-10-06T00:00:00+00:00",
    }


def test_stats_sends_no_window_it_was_not_given() -> None:
    client, requests = wire_client(lambda _r: httpx.Response(200, json=stats_payload()))

    _ = client.durable.approvals.stats(PROJECT_ID)

    assert dict(requests[0].url.params) == {}


@pytest.mark.parametrize(
    ("decide", "comment", "body"),
    [
        ("approve", "Ship it", {"comment": "Ship it"}),
        ("approve", None, {}),
        ("deny", "Out of stock", {"comment": "Out of stock"}),
        ("deny", None, {}),
    ],
)
def test_a_decision_posts_its_body_over_the_wire(
    decide: str, comment: str | None, body: dict[str, str]
) -> None:
    client, requests = wire_client(
        lambda _r: httpx.Response(200, json=approved_approval())
    )
    approvals = client.durable.approvals
    method = approvals.approve if decide == "approve" else approvals.deny

    approval = method(PROJECT_ID, APPROVAL_ID, comment=comment)

    assert approval.decision is not None
    assert requests[0].method == "POST"
    assert str(requests[0].url) == (
        f"{API_URL}/projects/{PROJECT_ID}/durable-approvals/{APPROVAL_ID}/{decide}"
    )
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert json.loads(requests[0].content) == body


@pytest.mark.parametrize(
    ("status", "expected"),
    [(403, PermissionDeniedError), (404, NotFoundError), (409, ConflictError)],
)
def test_wire_failures_map_to_typed_errors(
    status: int, expected: type[Exception]
) -> None:
    message = "approvals are decided by a person; use a platform token or the dashboard"
    client, _requests = wire_client(
        lambda _r: httpx.Response(status, json={"error": message, "code": "c"})
    )

    with pytest.raises(expected) as caught:
        _ = client.durable.approvals.approve(PROJECT_ID, APPROVAL_ID)

    assert type(caught.value) is expected
    assert str(caught.value) == message


@pytest.mark.parametrize("payload", [None, [], "approval", 1])
def test_an_approval_must_be_an_object(payload: object) -> None:
    with pytest.raises(TypeError, match="Expected a complete durable approval"):
        _ = durable_approval(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", ""),
        ("id", None),
        ("status", "waiting"),
        ("name", 3),
        ("title", None),
        ("description", None),
        ("function", None),
        ("function", {"id": FUNCTION_ID}),
        ("function", {"id": 3, "name": "f"}),
        ("execution", "e"),
        ("execution", {"id": None, "name": "e", "status": "waiting"}),
        ("execution", {"id": None, "name": None, "status": None}),
        ("requested_at", "yesterday"),
        ("requested_at", None),
        ("expires_at", "tomorrow"),
        ("decision", "approved"),
        ("decision", {"comment": None, "decided_by": None, "decided_at": "2026"}),
        ("decision", {"comment": "", "decided_by": "ops", "decided_at": "2026"}),
        (
            "decision",
            {"comment": "", "decided_by": {"id": "u"}, "decided_at": "2026-10-06"},
        ),
        ("decision", {"comment": "", "decided_by": None, "decided_at": None}),
        ("details", {1: "x"}),
    ],
)
def test_an_approval_with_a_malformed_field_is_refused(
    field: str, value: object
) -> None:
    payload = pending_approval()
    payload[field] = value

    with pytest.raises(TypeError, match="Expected a complete durable approval"):
        _ = durable_approval(payload)


@pytest.mark.parametrize("field", ["id", "function", "execution", "requested_at"])
def test_an_approval_missing_a_field_is_refused(field: str) -> None:
    payload = pending_approval()
    del payload[field]

    with pytest.raises(TypeError, match="Expected a complete durable approval"):
        _ = durable_approval(payload)


def test_an_approval_with_non_string_keys_is_refused() -> None:
    payload: dict[object, object] = {1: "x"}
    payload.update(pending_approval())

    with pytest.raises(TypeError, match="Expected a complete durable approval"):
        _ = durable_approval(payload)


@pytest.mark.parametrize(
    "payload",
    [
        None,
        [],
        {"data": "x"},
        {"data": [], "has_more": "no"},
        {"data": [], "page": True},
        {"data": [], "total": 1.5},
    ],
)
def test_a_malformed_approval_page_is_refused(payload: object) -> None:
    with pytest.raises(TypeError, match="Expected a complete durable approval page"):
        _ = durable_approval_page(payload)


def test_an_approval_page_defaults_missing_metadata() -> None:
    page = durable_approval_page({})

    assert page == DurableApprovalPage(
        approvals=(), page=0, limit=0, total=0, has_more=False
    )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("from", None),
        ("to", "later"),
        ("counts", None),
        ("counts", {"requested": 1}),
        ("counts", counts(pending=True)),
        ("counts", counts(approved=1.5)),
        ("approval_rate", "half"),
        ("approval_rate", True),
        ("median_seconds_to_decision", "fast"),
        ("p90_seconds_to_decision", float("nan")),
        ("functions", None),
        ("functions", [{"function": None, "counts": counts()}]),
        ("functions", [{"function": {"id": None, "name": "f"}, "counts": None}]),
        ("other_functions", []),
        ("daily", "today"),
        ("daily", [{"date": "yesterday", "counts": counts()}]),
        ("daily", [{"date": None, "counts": counts()}]),
        ("daily", ["2026-10-05"]),
    ],
)
def test_malformed_stats_are_refused(field: str, value: object) -> None:
    payload = stats_payload()
    payload[field] = value

    with pytest.raises(TypeError, match="Expected complete durable approval stats"):
        _ = durable_approval_stats(payload)


@pytest.mark.parametrize("payload", [None, [], {1: "x"}])
def test_stats_must_be_an_object(payload: object) -> None:
    with pytest.raises(TypeError, match="Expected complete durable approval stats"):
        _ = durable_approval_stats(payload)
