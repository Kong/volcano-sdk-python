from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from types import MappingProxyType
from typing import TYPE_CHECKING

import httpx
import pytest
from typing_extensions import override

from volcano_sdk import (
    ConflictError,
    DurableMessage,
    DurableMessagePage,
    DurableMessageSender,
    DurableMessageSubscription,
    NotFoundError,
    ServerError,
    Session,
    VolcanoClient,
)
from volcano_sdk._durable_message_response import (
    durable_message,
    durable_message_page,
)
from volcano_sdk._durable_message_stream import retry_delay
from volcano_sdk._realtime_durable import DurableChannels
from volcano_sdk._transport import (
    DurableMessageListRequest,
    DurableMessageSendRequest,
    DurableMessageTarget,
    GeneratedTransport,
)
from volcano_sdk.durable import Durable

from .fixtures.invalid_arguments import (
    assign_snapshot_value,
    durable_realtime_channel,
    non_callable_message_handler,
    non_string_sent_message_name,
    remove_durable_realtime_channel,
    unknown_listed_message_direction,
    unknown_sent_message_option,
    unknown_subscription_option,
)
from .realtime_probes import realtime_state
from .test_realtime import FakeCentrifugeClient, FakeCentrifugeFactory, FakeSubscription
from .transport_fixtures import RejectingTransport

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Callable, Mapping

    from volcano_sdk._durable_messages import DurableMessages

PROJECT_ID = "00000000-0000-4000-8000-000000000001"
EXECUTION_ID = "00000000-0000-4000-8000-0000000000e1"
USER_ID = "00000000-0000-4000-8000-0000000000a7"
API_URL = "https://api.volcano.test"
CHANNEL = f"durable:{EXECUTION_ID}"
APPLICATION_PATH = f"/durable-functions/checkout/executions/{EXECUTION_ID}/messages"
PROJECT_PATH = f"/projects/{PROJECT_ID}{APPLICATION_PATH}"


@dataclass(frozen=True)
class FakeResponse:
    status_code: int
    payload: object
    headers: dict[str, str]
    content: bytes = b""


def published(seq: int, **overrides: object) -> dict[str, object]:
    message: dict[str, object] = {
        "id": f"00000000-0000-4000-8000-{seq:012d}",
        "execution_id": EXECUTION_ID,
        "direction": "out",
        "seq": seq,
        "name": "progress",
        "data": {"step": seq},
        "sender": {"type": "execution", "user_id": None},
        "status": "published",
        "sent_at": "2026-10-12T09:00:00Z",
        "delivered_at": None,
    }
    message.update(overrides)
    return message


def sent(**overrides: object) -> dict[str, object]:
    return (
        published(
            4,
            direction="in",
            name="address-confirmed",
            data={"street": "Main St", "lines": [1, 2]},
            sender={"type": "user", "user_id": USER_ID},
            status="delivered",
            delivered_at="2026-10-12T09:00:05Z",
        )
        | overrides
    )


class FakeMessageTransport(RejectingTransport):
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []
        self.send_response: FakeResponse = FakeResponse(201, sent(), {})
        self.list_response: FakeResponse = FakeResponse(
            200, {"data": [published(1), sent()], "has_more": False}, {}
        )
        # Answers subscription reads from the execution's published messages,
        # after any canned answers. Each canned answer is given once, so a
        # read that goes on gets the published pages instead of spinning.
        self.published: list[int] = []
        self.page_size: int = 100
        self.read_answers: list[FakeResponse] = []
        self.next_read_gate: asyncio.Event | None = None
        self.read_arrivals: Arrivals = Arrivals()

    def send_durable_message(self, **kwargs: object) -> FakeResponse:
        self.calls.append(("sendDurableMessage", kwargs))
        return self.send_response

    def list_durable_messages(self, **kwargs: object) -> FakeResponse:
        self.calls.append(("listDurableMessages", kwargs))
        return self.list_response

    async def list_durable_messages_async(self, **kwargs: object) -> FakeResponse:
        self.calls.append(("listDurableMessagesAsync", kwargs))
        request = kwargs["request"]
        assert isinstance(request, DurableMessageListRequest)
        # A catch-up read without its cursor would page from the start forever.
        assert request.after is not None
        # Read before waiting, as a list racing a publish would.
        answer = (
            self.read_answers.pop(0)
            if self.read_answers
            else self.page_after(request.after)
        )
        self.read_arrivals.arrive()
        gate, self.next_read_gate = self.next_read_gate, None
        if gate is not None:
            _ = await asyncio.wait_for(gate.wait(), timeout=2)
        return answer

    def page_after(self, after: int) -> FakeResponse:
        newer = [seq for seq in self.published if seq > after]
        page = newer[: self.page_size]
        return FakeResponse(
            200,
            {"data": [published(seq) for seq in page], "has_more": page != newer},
            {},
        )

    def reads(self) -> list[DurableMessageListRequest]:
        requests: list[DurableMessageListRequest] = []
        for name, arguments in self.calls:
            request = arguments["request"]
            if name == "listDurableMessagesAsync":
                assert isinstance(request, DurableMessageListRequest)
                requests.append(request)
        return requests

    def read_after(self) -> list[int | None]:
        return [request.after for request in self.reads()]


class Arrivals:
    def __init__(self) -> None:
        self.count: int = 0
        self._arrived: asyncio.Event = asyncio.Event()

    def arrive(self) -> None:
        self.count += 1
        self._arrived.set()

    async def wait_for(self, count: int) -> None:
        async def reach() -> None:
            while self.count < count:
                self._arrived.clear()
                _ = await self._arrived.wait()

        await asyncio.wait_for(reach(), timeout=2)


class Received:
    def __init__(self) -> None:
        self.messages: list[DurableMessage] = []
        self.arrivals: Arrivals = Arrivals()

    def __call__(self, message: DurableMessage) -> None:
        self.messages.append(message)
        self.arrivals.arrive()

    @property
    def seqs(self) -> list[int]:
        return [message.seq for message in self.messages]

    async def until(self, count: int) -> list[int]:
        await self.arrivals.wait_for(count)
        return self.seqs


def messages_client(
    transport: RejectingTransport | GeneratedTransport, *, session: bool = False
) -> VolcanoClient:
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    if session:
        _ = client.auth.set_session(
            Session(
                access_token="access-token",
                refresh_token="refresh-token",
                user_id=USER_ID,
            )
        )
    return client


def wire_client(
    respond: Callable[[httpx.Request], httpx.Response], *, session: bool = False
) -> tuple[VolcanoClient, list[httpx.Request]]:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return respond(request)

    client = messages_client(
        GeneratedTransport(
            api_url=API_URL, httpx_transport=httpx.MockTransport(handle)
        ),
        session=session,
    )
    return client, requests


def subscriber(
    transport: FakeMessageTransport,
) -> tuple[VolcanoClient, FakeCentrifugeClient]:
    native = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(native),
    )
    return client, native


def subscription_of(native: FakeCentrifugeClient) -> FakeSubscription:
    return native.subscriptions[CHANNEL]


async def dispatched(client: VolcanoClient) -> None:
    """Wait until the channel has handed its queued publications on."""
    task = realtime_state(client.realtime).channels[CHANNEL].state.callback_task
    # Not wait_for: cancelling the dispatcher from a handler it is running
    # would leave both cancelling forever instead of failing the test.
    if task is not None:
        _ = await asyncio.wait({task}, timeout=2)


SEND_AND_LIST: dict[str, Callable[[DurableMessages], object]] = {
    "send": lambda m: m.send("checkout", EXECUTION_ID, "ping", project_id=PROJECT_ID),
    "list": lambda m: m.list("checkout", EXECUTION_ID, project_id=PROJECT_ID),
}


@pytest.mark.parametrize(
    "call", [pytest.param(call, id=name) for name, call in SEND_AND_LIST.items()]
)
def test_messages_require_a_transport_with_message_methods(
    call: Callable[[DurableMessages], object],
) -> None:
    messages = messages_client(RejectingTransport(), session=True).durable.messages

    with pytest.raises(TypeError, match="Transport does not support durable messages"):
        _ = call(messages)


def test_send_uses_the_application_route_with_the_client_credential() -> None:
    transport = FakeMessageTransport()

    message = messages_client(transport).durable.messages.send(
        " checkout ",
        f" {EXECUTION_ID} ",
        "address-confirmed",
        {"street": "Main St"},
        client_token="client-token",
        idempotency_key="confirm-1",
    )

    assert message == DurableMessage(
        id="00000000-0000-4000-8000-000000000004",
        execution_id=EXECUTION_ID,
        direction="in",
        seq=4,
        name="address-confirmed",
        data={"street": "Main St", "lines": (1, 2)},
        sender=DurableMessageSender(type="user", user_id=USER_ID),
        status="delivered",
        sent_at=datetime(2026, 10, 12, 9, tzinfo=UTC),
        delivered_at=datetime(2026, 10, 12, 9, 0, 5, tzinfo=UTC),
    )
    assert transport.calls == [
        (
            "sendDurableMessage",
            {
                "authorization": "anon-key",
                "target": DurableMessageTarget(
                    function_id="checkout",
                    execution_id=EXECUTION_ID,
                    client_token="client-token",
                ),
                "request": DurableMessageSendRequest(
                    name="address-confirmed",
                    data={"street": "Main St"},
                    idempotency_key="confirm-1",
                ),
            },
        )
    ]


def test_a_repeated_send_returns_the_message_the_first_one_stored() -> None:
    transport = FakeMessageTransport()
    transport.send_response = FakeResponse(200, sent(status="queued"), {})

    message = messages_client(transport).durable.messages.send(
        "checkout", EXECUTION_ID, "address-confirmed", idempotency_key="confirm-1"
    )

    assert message.status == "queued"
    assert message.delivered_at == datetime(2026, 10, 12, 9, 0, 5, tzinfo=UTC)


def test_send_on_the_project_route_uses_the_session() -> None:
    transport = FakeMessageTransport()

    _ = messages_client(transport, session=True).durable.messages.send(
        "checkout", EXECUTION_ID, "ping", project_id=f" {PROJECT_ID} "
    )

    assert transport.calls == [
        (
            "sendDurableMessage",
            {
                "authorization": "access-token",
                "target": DurableMessageTarget(
                    function_id="checkout",
                    execution_id=EXECUTION_ID,
                    project_id=PROJECT_ID,
                ),
                "request": DurableMessageSendRequest(name="ping"),
            },
        )
    ]


@pytest.mark.parametrize(
    "call", [pytest.param(call, id=name) for name, call in SEND_AND_LIST.items()]
)
def test_the_project_route_needs_a_session(
    call: Callable[[DurableMessages], object],
) -> None:
    transport = FakeMessageTransport()

    with pytest.raises(RuntimeError, match="No active session"):
        _ = call(messages_client(transport).durable.messages)
    assert transport.calls == []


@pytest.mark.parametrize(
    ("status", "code", "expected"),
    [
        (404, None, NotFoundError),
        (409, "execution_not_running", ConflictError),
        (500, None, ServerError),
    ],
)
def test_send_failures_raise_typed_errors(
    status: int, code: str | None, expected: type[Exception]
) -> None:
    transport = FakeMessageTransport()
    body: dict[str, object] = {"error": "cannot send"}
    if code is not None:
        body["code"] = code
    transport.send_response = FakeResponse(status, body, {})

    with pytest.raises(expected, match="cannot send") as caught:
        _ = messages_client(transport).durable.messages.send(
            "checkout", EXECUTION_ID, "ping"
        )

    assert type(caught.value) is expected
    assert getattr(caught.value, "code", None) == code


def test_list_forwards_every_filter_and_returns_a_page() -> None:
    transport = FakeMessageTransport()

    page = messages_client(transport).durable.messages.list(
        "checkout",
        EXECUTION_ID,
        client_token="client-token",
        direction="in",
        name="address-confirmed",
        after=3,
        limit=50,
    )

    assert page == DurableMessagePage(
        messages=(durable_message(published(1)), durable_message(sent())),
        has_more=False,
    )
    assert transport.calls == [
        (
            "listDurableMessages",
            {
                "authorization": "anon-key",
                "target": DurableMessageTarget(
                    function_id="checkout",
                    execution_id=EXECUTION_ID,
                    client_token="client-token",
                ),
                "request": DurableMessageListRequest(
                    direction="in", name="address-confirmed", after=3, limit=50
                ),
            },
        )
    ]


def test_list_omits_unset_filters() -> None:
    transport = FakeMessageTransport()

    _ = messages_client(transport, session=True).durable.messages.list(
        "checkout", EXECUTION_ID, project_id=PROJECT_ID, direction="out"
    )

    assert transport.calls == [
        (
            "listDurableMessages",
            {
                "authorization": "access-token",
                "target": DurableMessageTarget(
                    function_id="checkout",
                    execution_id=EXECUTION_ID,
                    project_id=PROJECT_ID,
                ),
                "request": DurableMessageListRequest(direction="out"),
            },
        )
    ]


def test_list_raises_not_found_for_an_execution_it_cannot_reach() -> None:
    transport = FakeMessageTransport()
    transport.list_response = FakeResponse(404, {"error": "execution not found"}, {})

    with pytest.raises(NotFoundError, match="execution not found"):
        _ = messages_client(transport).durable.messages.list("checkout", EXECUTION_ID)


INVALID_ARGUMENTS: dict[str, tuple[Callable[[DurableMessages], object], str]] = {
    "empty function": (
        lambda m: m.send("", EXECUTION_ID, "ping"),
        "function_name must be a non-empty string",
    ),
    "blank execution": (
        lambda m: m.send("checkout", " ", "ping"),
        "execution_id must be a non-empty string",
    ),
    "send execution": (
        lambda m: m.send("checkout", "execution-1", "ping"),
        "execution_id must be a UUID",
    ),
    "send project": (
        lambda m: m.send("checkout", EXECUTION_ID, "ping", project_id="project"),
        "project_id must be a UUID",
    ),
    "empty client token": (
        lambda m: m.send("checkout", EXECUTION_ID, "ping", client_token=""),
        "client_token must be a non-empty string",
    ),
    "empty name": (
        lambda m: m.send("checkout", EXECUTION_ID, ""),
        "name must be a non-empty string",
    ),
    "blank name": (
        lambda m: m.send("checkout", EXECUTION_ID, "  "),
        "name must be a non-empty string",
    ),
    "non-string name": (
        lambda m: non_string_sent_message_name(m, EXECUTION_ID),
        "name must be a non-empty string",
    ),
    "empty idempotency key": (
        lambda m: m.send("checkout", EXECUTION_ID, "ping", idempotency_key=""),
        "idempotency_key must be a non-empty string",
    ),
    "long idempotency key": (
        lambda m: m.send("checkout", EXECUTION_ID, "ping", idempotency_key="k" * 256),
        "idempotency_key must be at most 255 characters",
    ),
    "list function": (
        lambda m: m.list(" ", EXECUTION_ID),
        "function_name must be a non-empty string",
    ),
    "list execution": (
        lambda m: m.list("checkout", "execution-1"),
        "execution_id must be a UUID",
    ),
    "list project": (
        lambda m: m.list("checkout", EXECUTION_ID, project_id="project"),
        "project_id must be a UUID",
    ),
    "list client token": (
        lambda m: m.list("checkout", EXECUTION_ID, client_token=""),
        "client_token must be a non-empty string",
    ),
    "list direction": (
        lambda m: unknown_listed_message_direction(m, EXECUTION_ID),
        "direction must be 'in' or 'out'",
    ),
}


@pytest.mark.parametrize(
    ("call", "message"),
    [pytest.param(*case, id=name) for name, case in INVALID_ARGUMENTS.items()],
)
def test_invalid_arguments_are_refused_before_transport(
    call: Callable[[DurableMessages], object], message: str
) -> None:
    transport = FakeMessageTransport()
    messages = messages_client(transport).durable.messages

    with pytest.raises(ValueError, match=f"^{re.escape(message)}$"):
        _ = call(messages)
    assert transport.calls == []


def test_an_idempotency_key_may_use_the_whole_length() -> None:
    transport = FakeMessageTransport()
    key = "k" * 255

    _ = messages_client(transport).durable.messages.send(
        "checkout", EXECUTION_ID, "ping", idempotency_key=key
    )

    assert transport.calls[0][1]["request"] == DurableMessageSendRequest(
        name="ping", idempotency_key=key
    )


def test_unknown_options_are_refused() -> None:
    transport = FakeMessageTransport()

    with pytest.raises(TypeError, match="unexpected option: retries"):
        unknown_sent_message_option(
            messages_client(transport).durable.messages, EXECUTION_ID
        )
    assert transport.calls == []


def test_send_goes_over_the_application_route() -> None:
    client, requests = wire_client(lambda _r: httpx.Response(201, json=sent()))

    message = client.durable.messages.send(
        "checkout",
        EXECUTION_ID,
        "address-confirmed",
        {"street": "Main St"},
        client_token="client-token",
        idempotency_key="confirm-1",
    )

    assert message.seq == 4
    assert len(requests) == 1
    assert requests[0].method == "POST"
    assert str(requests[0].url) == f"{API_URL}{APPLICATION_PATH}"
    assert requests[0].headers["authorization"] == "Bearer anon-key"
    assert requests[0].headers["x-volcano-client-token"] == "client-token"
    assert requests[0].headers["idempotency-key"] == "confirm-1"
    assert json.loads(requests[0].content) == {
        "name": "address-confirmed",
        "data": {"street": "Main St"},
    }


def test_send_accepts_the_data_of_a_message_it_read() -> None:
    client, requests = wire_client(lambda _r: httpx.Response(201, json=sent()))
    received = durable_message(sent())

    _ = client.durable.messages.send(
        "checkout", EXECUTION_ID, "address-confirmed", received.data
    )

    assert json.loads(requests[0].content) == {
        "name": "address-confirmed",
        "data": {"street": "Main St", "lines": [1, 2]},
    }


def test_send_goes_over_the_project_route() -> None:
    client, requests = wire_client(
        lambda _r: httpx.Response(200, json=sent()), session=True
    )

    _ = client.durable.messages.send(
        "checkout", EXECUTION_ID, "ping", project_id=PROJECT_ID
    )

    assert str(requests[0].url) == f"{API_URL}{PROJECT_PATH}"
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert "x-volcano-client-token" not in requests[0].headers
    assert "idempotency-key" not in requests[0].headers
    assert json.loads(requests[0].content) == {"name": "ping", "data": None}


def test_send_on_the_project_route_forwards_the_idempotency_key() -> None:
    client, requests = wire_client(
        lambda _r: httpx.Response(201, json=sent()), session=True
    )

    _ = client.durable.messages.send(
        "checkout",
        EXECUTION_ID,
        "ping",
        project_id=PROJECT_ID,
        idempotency_key="ping-1",
    )

    assert requests[0].url.path == PROJECT_PATH
    assert requests[0].headers["idempotency-key"] == "ping-1"


def test_list_goes_over_the_application_route_with_every_filter() -> None:
    client, requests = wire_client(
        lambda _r: httpx.Response(200, json={"data": [sent()], "has_more": True})
    )

    page = client.durable.messages.list(
        "checkout",
        EXECUTION_ID,
        client_token="client-token",
        direction="out",
        name="progress",
        after=2,
        limit=50,
    )

    assert page.has_more is True
    assert requests[0].method == "GET"
    assert requests[0].url.path == APPLICATION_PATH
    assert dict(requests[0].url.params) == {
        "direction": "out",
        "name": "progress",
        "after": "2",
        "limit": "50",
    }
    assert requests[0].headers["authorization"] == "Bearer anon-key"
    assert requests[0].headers["x-volcano-client-token"] == "client-token"


def test_list_goes_over_the_project_route_without_filters() -> None:
    client, requests = wire_client(
        lambda _r: httpx.Response(200, json={"data": [], "has_more": False}),
        session=True,
    )

    page = client.durable.messages.list("checkout", EXECUTION_ID, project_id=PROJECT_ID)

    assert page == DurableMessagePage(messages=(), has_more=False)
    assert requests[0].url.path == PROJECT_PATH
    assert dict(requests[0].url.params) == {}
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert "x-volcano-client-token" not in requests[0].headers


def test_list_goes_over_the_project_route_with_every_filter() -> None:
    client, requests = wire_client(
        lambda _r: httpx.Response(200, json={"data": [], "has_more": False}),
        session=True,
    )

    _ = client.durable.messages.list(
        "checkout",
        EXECUTION_ID,
        project_id=PROJECT_ID,
        direction="in",
        name="address-confirmed",
        after=3,
        limit=10,
    )

    assert requests[0].url.path == PROJECT_PATH
    assert dict(requests[0].url.params) == {
        "direction": "in",
        "name": "address-confirmed",
        "after": "3",
        "limit": "10",
    }


@pytest.mark.parametrize(
    ("target", "path", "headers"),
    [
        (
            DurableMessageTarget(
                function_id="checkout",
                execution_id=EXECUTION_ID,
                client_token="client-token",
            ),
            APPLICATION_PATH,
            {"x-volcano-client-token": "client-token"},
        ),
        (
            DurableMessageTarget(
                function_id="checkout",
                execution_id=EXECUTION_ID,
                project_id=PROJECT_ID,
                client_token="client-token",
            ),
            PROJECT_PATH,
            {},
        ),
    ],
)
async def test_the_async_list_goes_over_either_route_with_every_filter(
    target: DurableMessageTarget, path: str, headers: dict[str, str]
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"data": [published(1)], "has_more": False})

    transport = GeneratedTransport(
        api_url=API_URL, httpx_transport=httpx.MockTransport(handle)
    )

    response = await transport.list_durable_messages_async(
        authorization="access-token",
        target=target,
        request=DurableMessageListRequest(
            direction="out", name="progress", after=7, limit=20
        ),
    )

    assert response.status_code == 200
    assert requests[0].url.path == path
    assert dict(requests[0].url.params) == {
        "direction": "out",
        "name": "progress",
        "after": "7",
        "limit": "20",
    }
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert {
        name: value
        for name, value in requests[0].headers.items()
        if name == "x-volcano-client-token"
    } == headers


def test_a_message_snapshots_its_data() -> None:
    message = durable_message(sent(data={"street": "Main St"}))

    assert isinstance(message.data, MappingProxyType)
    with pytest.raises(TypeError):
        assign_snapshot_value(message.data)


def test_an_undelivered_message_has_no_delivery_time() -> None:
    message = durable_message(
        sent(status="queued", delivered_at=None, sender={"type": "anon"})
    )

    assert message.delivered_at is None
    assert message.sender == DurableMessageSender(type="anon")


@pytest.mark.parametrize("payload", [None, [], "message", {1: "id"}])
def test_a_message_must_be_an_object(payload: object) -> None:
    with pytest.raises(TypeError, match="Expected a complete durable message"):
        _ = durable_message(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", ""),
        ("id", None),
        ("execution_id", 7),
        ("direction", "both"),
        ("seq", 0),
        ("seq", True),
        ("seq", "4"),
        ("name", ""),
        ("data", {"at": {1}}),
        ("sender", None),
        ("sender", {"type": ""}),
        ("sender", {"type": "user", "user_id": 7}),
        ("status", "sent"),
        ("sent_at", None),
        ("sent_at", "yesterday"),
        ("delivered_at", "soon"),
    ],
)
def test_a_message_must_be_complete(field: str, value: object) -> None:
    with pytest.raises(TypeError, match=r"^Expected a complete durable message$"):
        _ = durable_message(sent(**{field: value}))


def test_the_first_message_has_seq_one() -> None:
    assert durable_message(published(1)).seq == 1


def test_a_page_accepts_any_sequence_of_messages() -> None:
    page = durable_message_page({"data": (published(1),), "has_more": True})

    assert page.messages == (durable_message(published(1)),)
    assert page.has_more is True


@pytest.mark.parametrize(
    "payload",
    [
        None,
        {"data": None, "has_more": False},
        {"data": {}, "has_more": False},
        {"data": [], "has_more": None},
        {"data": []},
    ],
)
def test_a_page_must_be_complete(payload: object) -> None:
    with pytest.raises(TypeError, match="Expected a complete durable message page"):
        _ = durable_message_page(payload)


async def test_subscribe_delivers_what_was_published_then_live_messages() -> None:
    transport = FakeMessageTransport()
    transport.published = [1, 2]
    client, native = subscriber(transport)
    received = Received()
    try:
        subscription = await client.durable.messages.subscribe(
            "checkout", EXECUTION_ID, received, client_token="client-token"
        )

        assert isinstance(subscription, DurableMessageSubscription)
        assert received.seqs == [1, 2]
        channel = subscription_of(native)
        assert channel.data == {"client_token": "client-token"}
        assert channel.recoverable is False
        assert channel.join_leave is False
        assert transport.calls == [
            (
                "listDurableMessagesAsync",
                {
                    "authorization": "access-token",
                    "target": DurableMessageTarget(
                        function_id="checkout",
                        execution_id=EXECUTION_ID,
                        client_token="client-token",
                    ),
                    "request": DurableMessageListRequest(direction="out", after=0),
                },
            )
        ]

        await channel.emit(published(2))
        await channel.emit(published(3))

        assert await received.until(3) == [1, 2, 3]
        assert received.messages[2] == durable_message(published(3))
    finally:
        await client.realtime.disconnect()


async def test_subscribe_on_the_project_route_sends_no_client_token() -> None:
    transport = FakeMessageTransport()
    client, native = subscriber(transport)
    try:
        _ = await client.durable.messages.subscribe(
            "checkout", EXECUTION_ID, Received(), project_id=PROJECT_ID
        )

        assert subscription_of(native).data is None
        assert transport.calls[0][1]["target"] == DurableMessageTarget(
            function_id="checkout", execution_id=EXECUTION_ID, project_id=PROJECT_ID
        )
    finally:
        await client.realtime.disconnect()


async def test_subscribe_ignores_messages_sent_to_the_execution() -> None:
    transport = FakeMessageTransport()
    client, native = subscriber(transport)
    received = Received()
    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)
        channel = subscription_of(native)

        await channel.emit(published(1, direction="in"))
        await channel.emit({"seq": 2})
        await channel.emit(published(3))

        assert await received.until(1) == [3]
    finally:
        await client.realtime.disconnect()


async def test_live_messages_wait_for_the_first_read_and_follow_it_in_order() -> None:
    transport = FakeMessageTransport()
    transport.published = [1, 2]
    gate = asyncio.Event()
    transport.next_read_gate = gate
    client, native = subscriber(transport)
    received = Received()
    try:
        subscribing = asyncio.create_task(
            client.durable.messages.subscribe("checkout", EXECUTION_ID, received)
        )
        await transport.read_arrivals.wait_for(1)
        channel = subscription_of(native)
        await channel.emit(published(4))
        await channel.emit(published(3))
        await channel.emit(published(2))
        await dispatched(client)

        assert received.seqs == []
        gate.set()
        _ = await subscribing

        assert received.seqs == [1, 2, 3, 4]
    finally:
        await client.realtime.disconnect()


class PublishingBeforeReady(FakeSubscription):
    """Deliver a publication while subscribe still waits to be ready."""

    early: object = None

    @override
    async def ready(self) -> None:
        await super().ready()
        await self.emit(self.early)
        task = self._events().channel.callback_task
        if task is not None:
            await task


class PublishingBeforeReadyClient(FakeCentrifugeClient):
    def __init__(self, early: object) -> None:
        super().__init__()
        self.early: object = early

    @override
    def new_subscription(
        self,
        name: str,
        *,
        events: object,
        join_leave: bool = False,
        recoverable: bool = False,
        data: Mapping[str, str] | None = None,
    ) -> FakeSubscription:
        subscription = PublishingBeforeReady(
            name, events, join_leave=join_leave, recoverable=recoverable, data=data
        )
        subscription.early = self.early
        self.subscriptions[name] = subscription
        return subscription


async def test_a_message_published_before_the_first_read_is_not_delivered_early() -> (
    None
):
    transport = FakeMessageTransport()
    transport.published = [1]
    native = PublishingBeforeReadyClient(published(2))
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(native),
    )
    received = Received()
    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)

        assert received.seqs == [1, 2]
    finally:
        await client.realtime.disconnect()


async def test_a_resubscription_reads_back_what_the_channel_missed() -> None:
    transport = FakeMessageTransport()
    transport.published = [1]
    client, native = subscriber(transport)
    received = Received()
    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)
        channel = subscription_of(native)

        await channel.emit_subscribing()
        transport.published += [2, 3]
        await channel.emit(published(2))
        await channel.emit_subscribed()
        assert await received.until(3) == [1, 2, 3]
        await channel.emit(published(4))

        assert await received.until(4) == [1, 2, 3, 4]
        assert transport.read_after() == [0, 1]
    finally:
        await client.realtime.disconnect()


async def test_an_earlier_read_does_not_release_messages_a_later_one_must_precede() -> (
    None
):
    transport = FakeMessageTransport()
    transport.published = [1]
    client, native = subscriber(transport)
    received = Received()
    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)
        channel = subscription_of(native)
        gate = asyncio.Event()
        transport.next_read_gate = gate
        await channel.emit_subscribing()
        await channel.emit_subscribed()
        await transport.read_arrivals.wait_for(2)

        await channel.emit_subscribing()
        transport.published += [2, 3]
        await channel.emit_subscribed()
        await channel.emit(published(4))
        await dispatched(client)
        gate.set()

        assert await received.until(4) == [1, 2, 3, 4]
        assert transport.read_after() == [0, 1, 1]
    finally:
        await client.realtime.disconnect()


async def test_a_message_arriving_during_release_follows_the_held_ones() -> None:
    transport = FakeMessageTransport()
    transport.published = [1]
    gate = asyncio.Event()
    transport.next_read_gate = gate
    client, native = subscriber(transport)
    seqs: list[int] = []

    async def handle(message: DurableMessage) -> None:
        seqs.append(message.seq)
        if message.seq == 3:
            await subscription_of(native).emit(published(4))
            await dispatched(client)

    try:
        subscribing = asyncio.create_task(
            client.durable.messages.subscribe("checkout", EXECUTION_ID, handle)
        )
        await transport.read_arrivals.wait_for(1)
        await subscription_of(native).emit(published(3))
        await dispatched(client)
        gate.set()
        _ = await subscribing

        assert seqs == [1, 3, 4]
    finally:
        await client.realtime.disconnect()


async def test_a_read_waits_for_the_handler_still_running_on_a_live_message() -> None:
    transport = FakeMessageTransport()
    client, native = subscriber(transport)
    calls: list[tuple[str, int]] = []
    handling = asyncio.Event()
    finish = asyncio.Event()
    second = asyncio.Event()

    async def handle(message: DurableMessage) -> None:
        calls.append(("start", message.seq))
        if message.seq == 1:
            handling.set()
            _ = await finish.wait()
        calls.append(("end", message.seq))
        if message.seq == 2:
            second.set()

    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, handle)
        channel = subscription_of(native)
        await channel.emit(published(1))
        _ = await handling.wait()
        await channel.emit_subscribing()
        transport.published += [1, 2]
        await channel.emit_subscribed()
        await transport.read_arrivals.wait_for(2)
        await asyncio.sleep(0)

        assert calls == [("start", 1)]
        finish.set()
        _ = await second.wait()
        assert calls == [("start", 1), ("end", 1), ("start", 2), ("end", 2)]
    finally:
        await client.realtime.disconnect()


async def test_subscribe_reads_every_page() -> None:
    transport = FakeMessageTransport()
    transport.published = [1, 2, 3]
    transport.page_size = 2
    client, _native = subscriber(transport)
    received = Received()
    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)

        assert received.seqs == [1, 2, 3]
        assert transport.read_after() == [0, 2]
    finally:
        await client.realtime.disconnect()


async def test_an_empty_page_ends_the_read() -> None:
    transport = FakeMessageTransport()
    transport.read_answers = [FakeResponse(200, {"data": [], "has_more": True}, {})]
    client, _native = subscriber(transport)
    try:
        _ = await client.durable.messages.subscribe(
            "checkout", EXECUTION_ID, Received()
        )

        assert transport.read_after() == [0]
    finally:
        await client.realtime.disconnect()


async def test_a_page_that_delivers_nothing_new_ends_the_read() -> None:
    transport = FakeMessageTransport()
    unchanged = FakeResponse(200, {"data": [published(1)], "has_more": True}, {})
    transport.read_answers = [unchanged, unchanged]
    client, _native = subscriber(transport)
    received = Received()
    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)

        assert received.seqs == [1]
        assert transport.read_after() == [0, 1]
    finally:
        await client.realtime.disconnect()


async def test_a_broadcast_naming_a_missed_publish_reads_it_back() -> None:
    transport = FakeMessageTransport()
    transport.published = [1]
    client, native = subscriber(transport)
    received = Received()
    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)
        channel = subscription_of(native)

        transport.published += [2, 3]
        await channel.emit(published(3, prev_seq=2))
        assert await received.until(3) == [1, 2, 3]
        await channel.emit(published(2, prev_seq=1))
        await channel.emit(published(4, prev_seq=3))
        await channel.emit(published(5, prev_seq="9"))
        await channel.emit(published(6, prev_seq=True))
        await channel.emit(published(7))

        assert await received.until(7) == [1, 2, 3, 4, 5, 6, 7]
        assert transport.read_after() == [0, 1]
    finally:
        await client.realtime.disconnect()


async def test_a_first_broadcast_without_prev_seq_is_delivered_without_a_read() -> None:
    transport = FakeMessageTransport()
    client, native = subscriber(transport)
    received = Received()
    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)
        await subscription_of(native).emit(published(1))

        assert await received.until(1) == [1]
        assert transport.read_after() == [0]
    finally:
        await client.realtime.disconnect()


class Retries:
    """Stand in for the retry backoff, noting each call."""

    def __init__(self) -> None:
        self.failures: list[int] = []
        self.delay: float = 0.0

    def __call__(self, failures: int) -> float:
        self.failures.append(failures)
        return self.delay


@pytest.fixture
def retries(monkeypatch: pytest.MonkeyPatch) -> Retries:
    fake = Retries()
    monkeypatch.setattr("volcano_sdk._durable_message_stream.retry_delay", fake)
    return fake


class Reports:
    """Collect what the event loop's exception handler is given."""

    def __init__(self) -> None:
        self.contexts: list[dict[str, object]] = []
        self.arrivals: Arrivals = Arrivals()

    def __call__(
        self, _loop: asyncio.AbstractEventLoop, context: dict[str, object]
    ) -> None:
        self.contexts.append(context)
        self.arrivals.arrive()

    @property
    def messages(self) -> list[object]:
        return [context["message"] for context in self.contexts]


@pytest.fixture
async def reports() -> AsyncIterator[Reports]:
    loop = asyncio.get_running_loop()
    previous = loop.get_exception_handler()
    fake = Reports()
    loop.set_exception_handler(fake)
    try:
        yield fake
    finally:
        # Deliver queued loop callbacks before restoring the test handler.
        await asyncio.sleep(0)
        loop.set_exception_handler(previous)


def test_retries_back_off_from_half_a_second_to_thirty() -> None:
    assert [retry_delay(failures) for failures in range(9)] == [
        0.5,
        1.0,
        2.0,
        4.0,
        8.0,
        16.0,
        30.0,
        30.0,
        30.0,
    ]


async def test_a_failed_read_after_a_gap_holds_the_broadcast_until_a_retry(
    retries: Retries, reports: Reports
) -> None:
    transport = FakeMessageTransport()
    transport.published = [1]
    client, native = subscriber(transport)
    received = Received()
    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)
        channel = subscription_of(native)
        transport.read_answers = [FakeResponse(500, {"error": "list failed"}, {})]
        transport.published += [2, 3]
        await channel.emit(published(3, prev_seq=2))
        await channel.emit(published(4))

        assert await received.until(4) == [1, 2, 3, 4]
        assert transport.read_after() == [0, 1, 1]
        assert retries.failures == [0]
        assert reports.messages == ["Volcano durable message catch-up failed"]
        assert isinstance(reports.contexts[0]["exception"], ServerError)
    finally:
        await client.realtime.disconnect()


async def test_a_failed_read_still_releases_what_follows_on(
    retries: Retries, reports: Reports
) -> None:
    transport = FakeMessageTransport()
    transport.published = [1]
    gate = asyncio.Event()
    client, native = subscriber(transport)
    received = Received()
    retries.delay = 60.0
    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)
        channel = subscription_of(native)
        transport.read_answers = [FakeResponse(500, {"error": "list failed"}, {})]
        transport.next_read_gate = gate
        await channel.emit_subscribing()
        await channel.emit_subscribed()
        await transport.read_arrivals.wait_for(2)
        await channel.emit(published(2, prev_seq=1))
        await channel.emit(published(4, prev_seq=3))
        await dispatched(client)
        gate.set()
        await reports.arrivals.wait_for(1)

        assert received.seqs == [1, 2]
        assert retries.failures == [0]
        assert reports.messages == ["Volcano durable message catch-up failed"]
    finally:
        await client.realtime.disconnect()


async def test_a_failed_read_with_nothing_held_is_retried(
    retries: Retries, reports: Reports
) -> None:
    transport = FakeMessageTransport()
    transport.published = [1]
    client, native = subscriber(transport)
    received = Received()
    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)
        channel = subscription_of(native)
        transport.read_answers = [FakeResponse(500, {"error": "list failed"}, {})]
        transport.published += [2]
        await channel.emit_subscribing()
        await channel.emit_subscribed()

        assert await received.until(2) == [1, 2]
        assert transport.read_after() == [0, 1, 1]
        assert retries.failures == [0]
        assert reports.messages == ["Volcano durable message catch-up failed"]
    finally:
        await client.realtime.disconnect()


async def test_a_handler_raising_with_nothing_held_is_retried_after_it(
    retries: Retries, reports: Reports
) -> None:
    transport = FakeMessageTransport()
    transport.published = [1]
    client, native = subscriber(transport)
    received = Received()
    failure = RuntimeError("handler failed")

    def handle(message: DurableMessage) -> None:
        received(message)
        if message.seq == 2:
            raise failure

    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, handle)
        channel = subscription_of(native)
        transport.published += [2, 3]
        await channel.emit_subscribing()
        await channel.emit_subscribed()

        assert await received.until(3) == [1, 2, 3]
        assert transport.read_after() == [0, 1, 2]
        assert reports.contexts[0]["exception"] is failure
        assert retries.failures == [0]
    finally:
        await client.realtime.disconnect()


async def test_a_read_that_stops_short_of_a_held_broadcast_reads_again(
    retries: Retries,
) -> None:
    transport = FakeMessageTransport()
    transport.published = [1]
    gate = asyncio.Event()
    transport.next_read_gate = gate
    client, native = subscriber(transport)
    received = Received()
    try:
        subscribing = asyncio.create_task(
            client.durable.messages.subscribe("checkout", EXECUTION_ID, received)
        )
        await transport.read_arrivals.wait_for(1)
        transport.published += [2, 3]
        await subscription_of(native).emit(published(3, prev_seq=2))
        await dispatched(client)
        gate.set()
        _ = await subscribing

        assert await received.until(3) == [1, 2, 3]
        assert transport.read_after() == [0, 1]
        assert retries.failures == [0]
    finally:
        await client.realtime.disconnect()


@pytest.mark.usefixtures("reports")
async def test_the_backoff_starts_over_once_a_read_catches_up(
    retries: Retries,
) -> None:
    transport = FakeMessageTransport()
    transport.published = [1]
    client, native = subscriber(transport)
    received = Received()
    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)
        channel = subscription_of(native)
        failed = FakeResponse(500, {"error": "list failed"}, {})
        transport.read_answers = [failed, failed, failed]
        transport.published += [2, 3, 4]
        await channel.emit(published(4, prev_seq=3))
        assert await received.until(4) == [1, 2, 3, 4]

        transport.read_answers = [failed]
        transport.published += [5, 6]
        await channel.emit(published(6, prev_seq=5))
        assert await received.until(6) == [1, 2, 3, 4, 5, 6]

        assert retries.failures == [0, 1, 2, 0]
    finally:
        await client.realtime.disconnect()


async def test_a_later_read_resumes_after_the_message_a_handler_raised_on(
    retries: Retries, reports: Reports
) -> None:
    transport = FakeMessageTransport()
    transport.published = [1]
    client, native = subscriber(transport)
    received = Received()
    failure = RuntimeError("handler failed")

    def handle(message: DurableMessage) -> None:
        received(message)
        if message.seq == 2:
            raise failure

    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, handle)
        transport.published += [2, 3, 4]
        await subscription_of(native).emit(published(5, prev_seq=4))

        assert await received.until(5) == [1, 2, 3, 4, 5]
        assert transport.read_after() == [0, 1, 2]
        assert reports.contexts[0]["exception"] is failure
        assert retries.failures == [0]
    finally:
        await client.realtime.disconnect()


@pytest.mark.parametrize("end", ["remove_all_channels", "disconnect"])
async def test_ending_the_realtime_channels_ends_the_subscription(
    end: str, retries: Retries
) -> None:
    transport = FakeMessageTransport()
    transport.published = [1]
    client, native = subscriber(transport)
    received = Received()
    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)
        channel = subscription_of(native)
        gate = asyncio.Event()
        transport.next_read_gate = gate
        transport.published += [2]
        await channel.emit(published(3, prev_seq=2))
        await transport.read_arrivals.wait_for(2)
        await getattr(client.realtime, end)()
        transport.published += [3]
        gate.set()
        await asyncio.sleep(0.05)

        assert received.seqs == [1]
        assert transport.read_after() == [0, 1]
        assert retries.failures == []
    finally:
        await client.realtime.disconnect()


async def test_leaving_after_a_removal_spares_the_channel_that_replaced_it() -> None:
    transport = FakeMessageTransport()
    client, native = subscriber(transport)
    state = realtime_state(client.realtime)
    try:
        stale = await client.durable.messages.subscribe(
            "checkout", EXECUTION_ID, Received()
        )
        channel = subscription_of(native)
        channel.unsubscribe_entered = asyncio.Event()
        channel.unsubscribe_release = asyncio.Event()
        removing = asyncio.create_task(client.realtime.remove_all_channels())
        _ = await asyncio.wait_for(channel.unsubscribe_entered.wait(), timeout=2)

        async def replace() -> object:
            async with state.connection_lock:
                return DurableChannels(state).durable_channel(EXECUTION_ID, None)

        replacing = asyncio.create_task(replace())
        await asyncio.sleep(0)
        leaving = asyncio.create_task(stale.unsubscribe())
        await asyncio.sleep(0)
        channel.unsubscribe_release.set()
        await removing
        replacement = await replacing
        await leaving

        assert replacement is not None
        assert state.channels[CHANNEL].state is replacement
    finally:
        await client.realtime.disconnect()


async def test_unsubscribing_from_the_handler_stops_the_read() -> None:
    transport = FakeMessageTransport()
    transport.published = [1]
    transport.page_size = 1
    client, native = subscriber(transport)
    seqs: list[int] = []
    subscriptions: list[DurableMessageSubscription] = []
    left = asyncio.Event()

    async def handle(message: DurableMessage) -> None:
        seqs.append(message.seq)
        if message.seq == 2:
            await subscriptions[0].unsubscribe()
            left.set()

    try:
        subscriptions.append(
            await client.durable.messages.subscribe("checkout", EXECUTION_ID, handle)
        )
        channel = subscription_of(native)
        await channel.emit_subscribing()
        transport.published += [2, 3]
        await channel.emit_subscribed()
        _ = await asyncio.wait_for(left.wait(), timeout=2)

        assert seqs == [1, 2]
        assert CHANNEL not in native.subscriptions
        assert transport.read_after() == [0, 1]
        assert ("unsubscribe", None) in channel.calls
    finally:
        await client.realtime.disconnect()


async def test_unsubscribe_stops_delivery_and_can_be_repeated() -> None:
    transport = FakeMessageTransport()
    client, native = subscriber(transport)
    received = Received()
    try:
        subscription = await client.durable.messages.subscribe(
            "checkout", EXECUTION_ID, received
        )
        channel = subscription_of(native)

        await subscription.unsubscribe()
        await subscription.unsubscribe()
        await channel.emit(published(1))

        assert received.seqs == []
        assert channel.calls.count(("unsubscribe", None)) == 1
        assert CHANNEL not in realtime_state(client.realtime).channels
    finally:
        await client.realtime.disconnect()


async def test_one_client_subscribes_to_an_execution_once() -> None:
    transport = FakeMessageTransport()
    client, native = subscriber(transport)
    received = Received()
    try:
        subscription = await client.durable.messages.subscribe(
            "checkout", EXECUTION_ID, Received()
        )

        with pytest.raises(RuntimeError, match="already subscribes"):
            _ = await client.durable.messages.subscribe(
                "checkout", EXECUTION_ID, received
            )

        await subscription.unsubscribe()
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)
        await subscription_of(native).emit(published(1))

        assert await received.until(1) == [1]
    finally:
        await client.realtime.disconnect()


async def test_a_subscription_still_leaving_blocks_a_new_one() -> None:
    transport = FakeMessageTransport()
    client, native = subscriber(transport)
    try:
        subscription = await client.durable.messages.subscribe(
            "checkout", EXECUTION_ID, Received()
        )
        channel = subscription_of(native)
        channel.unsubscribe_entered = asyncio.Event()
        channel.unsubscribe_release = asyncio.Event()
        leaving = asyncio.create_task(subscription.unsubscribe())
        _ = await asyncio.wait_for(channel.unsubscribe_entered.wait(), timeout=2)

        with pytest.raises(RuntimeError, match="already subscribes"):
            _ = await client.durable.messages.subscribe(
                "checkout", EXECUTION_ID, Received()
            )

        channel.unsubscribe_release.set()
        await leaving
    finally:
        await client.realtime.disconnect()


async def test_an_old_subscription_leaves_a_replacement_alone() -> None:
    transport = FakeMessageTransport()
    client, native = subscriber(transport)
    received = Received()
    try:
        stale = await client.durable.messages.subscribe(
            "checkout", EXECUTION_ID, Received()
        )
        await client.realtime.remove_all_channels()
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)

        await stale.unsubscribe()
        await subscription_of(native).emit(published(1))

        assert await received.until(1) == [1]
        assert CHANNEL in realtime_state(client.realtime).channels
    finally:
        await client.realtime.disconnect()


async def test_a_failed_first_read_fails_subscribe_and_leaves_the_channel() -> None:
    transport = FakeMessageTransport()
    transport.read_answers = [FakeResponse(404, {"error": "execution not found"}, {})]
    client, native = subscriber(transport)
    try:
        with pytest.raises(NotFoundError, match="execution not found"):
            _ = await client.durable.messages.subscribe(
                "checkout", EXECUTION_ID, Received()
            )

        assert CHANNEL not in native.subscriptions
        _ = await client.durable.messages.subscribe(
            "checkout", EXECUTION_ID, Received()
        )
    finally:
        await client.realtime.disconnect()


async def test_a_failing_handler_fails_subscribe_and_leaves_the_channel() -> None:
    transport = FakeMessageTransport()
    transport.published = [1]
    client, native = subscriber(transport)
    failure = RuntimeError("handler failed")

    def fail(_message: DurableMessage) -> None:
        raise failure

    try:
        with pytest.raises(RuntimeError) as caught:
            _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, fail)

        assert caught.value is failure
        assert CHANNEL not in native.subscriptions
    finally:
        await client.realtime.disconnect()


@pytest.mark.parametrize("service_key", [None, "service-key"])
async def test_subscribe_needs_a_signed_in_session(service_key: str | None) -> None:
    native = FakeCentrifugeClient()
    transport = FakeMessageTransport()
    client = VolcanoClient(
        anon_key="anon-key",
        service_key=service_key,
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(native),
    )
    try:
        for _attempt in range(2):
            with pytest.raises(RuntimeError, match=r"^subscribe\(\) needs a signed-in"):
                _ = await client.durable.messages.subscribe(
                    "checkout", EXECUTION_ID, Received(), client_token="client-token"
                )

        assert CHANNEL not in realtime_state(client.realtime).channels
        assert native.subscriptions == {}
        assert transport.reads() == []
    finally:
        await client.realtime.disconnect()


async def test_a_failed_read_after_a_resubscription_is_reported() -> None:
    transport = FakeMessageTransport()
    client, native = subscriber(transport)
    received = Received()
    errors: list[dict[str, object]] = []
    reported = asyncio.Event()
    loop = asyncio.get_running_loop()
    previous = loop.get_exception_handler()

    def report(_loop: asyncio.AbstractEventLoop, context: dict[str, object]) -> None:
        errors.append(context)
        reported.set()

    loop.set_exception_handler(report)
    try:
        _ = await client.durable.messages.subscribe("checkout", EXECUTION_ID, received)
        channel = subscription_of(native)
        transport.read_answers = [FakeResponse(500, {"error": "list failed"}, {})]
        await channel.emit_subscribing()
        await channel.emit_subscribed()
        _ = await asyncio.wait_for(reported.wait(), timeout=2)

        assert [error["message"] for error in errors] == [
            "Volcano durable message catch-up failed"
        ]
        assert isinstance(errors[0]["exception"], ServerError)
        await channel.emit(published(1))
        assert await received.until(1) == [1]
    finally:
        loop.set_exception_handler(previous)
        await client.realtime.disconnect()


async def test_subscribe_needs_the_client_s_realtime_connection() -> None:
    transport = FakeMessageTransport()
    durable = Durable(client=messages_client(transport, session=True))

    with pytest.raises(RuntimeError, match="needs a VolcanoClient"):
        _ = await durable.messages.subscribe("checkout", EXECUTION_ID, Received())
    assert transport.calls == []


async def test_subscribe_refuses_a_handler_it_cannot_call() -> None:
    transport = FakeMessageTransport()
    client, native = subscriber(transport)

    with pytest.raises(TypeError, match=r"^subscribe\(\) requires a handler function$"):
        await non_callable_message_handler(client.durable.messages, EXECUTION_ID)
    with pytest.raises(TypeError, match="unexpected option: after"):
        await unknown_subscription_option(client.durable.messages, EXECUTION_ID)

    assert transport.calls == []
    assert native.subscriptions == {}


async def test_a_durable_channel_is_not_a_public_channel_type() -> None:
    realtime = subscriber(FakeMessageTransport())[0].realtime

    with pytest.raises(ValueError, match="unsupported realtime channel type: durable"):
        durable_realtime_channel(realtime, EXECUTION_ID)
    with pytest.raises(ValueError, match="unsupported realtime channel type: durable"):
        await remove_durable_realtime_channel(realtime, EXECUTION_ID)
