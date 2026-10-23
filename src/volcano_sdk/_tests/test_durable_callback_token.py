from __future__ import annotations

import asyncio
import hashlib
import inspect
import json
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol

import httpx
import pytest

from volcano_sdk import ConflictError
from volcano_sdk._durable_callback_token import (
    CallbackFailedError,
    callback_failure,
    callback_result,
    register_callback,
    replayed_operation,
    token_submitter,
)
from volcano_sdk._transport_types import decode_json

from .fixtures.durable_platform import Answer, Platform, install_platform, refused

if TYPE_CHECKING:
    from collections.abc import Coroutine, Generator

    from volcano_sdk.models import JSONValue

API_URL = "https://api.volcano.test"
TOKEN = "vcb_fake-token-for-tests"
UNREADABLE_REGISTRATION = (
    "Volcano registered the callback with a token this SDK cannot read"
)
UNREADABLE_RESULT = "Volcano resumed the callback with a result this SDK cannot read"
SYNCHRONOUS = r"^wait_for_callback\(\) requires a synchronous submitter"


class InstallPlatform(Protocol):
    def __call__(self, *answers: Answer) -> Platform: ...


@pytest.fixture
def platform(monkeypatch: pytest.MonkeyPatch) -> InstallPlatform:
    def install(*answers: Answer) -> Platform:
        return install_platform(monkeypatch, *answers)

    return install


def issued(status: int = 201, token: object = TOKEN) -> httpx.Response:
    return httpx.Response(status, json={"token": token, "expires_at": None})


def register() -> str | None:
    return register_callback(API_URL, "arn:execution/order-1", "callback-1", "payment")


def test_a_callback_registers_for_its_token(platform: InstallPlatform) -> None:
    fake = platform(issued())

    assert register() == TOKEN

    [request] = fake.requests
    assert request.method == "POST"
    assert str(request.url) == f"{API_URL}/durable-callbacks"
    assert request.headers["Content-Type"] == "application/json"
    assert decode_json(request.content) == {
        "execution_ref": "arn:execution/order-1",
        "callback_id": "callback-1",
        "name": "payment",
    }


def test_a_callback_registered_before_returns_its_token(
    platform: InstallPlatform,
) -> None:
    _ = platform(issued(status=200))

    assert register() == TOKEN


def test_a_callback_the_runtime_has_not_recorded_yet_is_retried(
    platform: InstallPlatform,
) -> None:
    fake = platform(refused(409, "callback_not_ready"), issued())

    assert register() == TOKEN

    assert len(fake.requests) == 2
    assert fake.sleeps == [0.5]


def test_a_callback_that_already_closed_has_no_token(
    platform: InstallPlatform,
) -> None:
    fake = platform(refused(409, "callback_closed"))

    assert register() is None

    assert len(fake.requests) == 1
    assert fake.sleeps == []


@pytest.mark.parametrize(
    "code",
    ["callback_taken", "too_many_callback_tokens", "execution_ended", None],
)
def test_a_callback_refused_for_another_reason_raises_at_once(
    platform: InstallPlatform, code: str | None
) -> None:
    fake = platform(refused(409, code))

    with pytest.raises(ConflictError, match="refused with 409") as caught:
        _ = register()

    assert caught.value.code == code
    assert len(fake.requests) == 1


@pytest.mark.parametrize(
    "answer",
    [
        issued(token=""),
        issued(token=7),
        httpx.Response(201, json={"expires_at": None}),
        httpx.Response(201, json=[TOKEN]),
        httpx.Response(201),
    ],
    ids=["empty", "number", "missing", "list", "no-body"],
)
def test_a_registration_without_a_readable_token_is_refused(
    platform: InstallPlatform, answer: httpx.Response
) -> None:
    _ = platform(answer)

    with pytest.raises(TypeError, match=f"^{UNREADABLE_REGISTRATION}$"):
        _ = register()


def test_the_submitter_hands_the_token_on(platform: InstallPlatform) -> None:
    fake = platform(issued())
    handed: list[str] = []
    submit = token_submitter(API_URL, "arn:execution", "payment", handed.append)

    submit("callback-4", None)

    assert handed == [TOKEN]
    assert decode_json(fake.requests[0].content) == {
        "execution_ref": "arn:execution",
        "callback_id": "callback-4",
        "name": "payment",
    }


def test_a_replayed_submitter_names_the_callbacks_operation(
    platform: InstallPlatform,
) -> None:
    fake = platform(issued())
    handed: list[str] = []
    submit = token_submitter(API_URL, "arn:execution", "payment", handed.append, "ab12")

    submit("callback-4", None)

    assert decode_json(fake.requests[0].content) == {
        "execution_ref": "arn:execution",
        "callback_id": "callback-4",
        "name": "payment",
        "operation_id": "ab12",
    }


@dataclass(frozen=True)
class Checkpoint:
    exists: bool

    def is_existent(self) -> bool:
        return self.exists


@dataclass
class Checkpoints:
    recorded: set[str] = field(default_factory=set[str])

    def get_checkpoint_result(self, operation_id: str) -> Checkpoint:
        return Checkpoint(operation_id in self.recorded)


@dataclass
class OpaqueCheckpoints:
    result: object

    def get_checkpoint_result(self, operation_id: str) -> object:
        _ = operation_id
        return self.result


@dataclass
class RuntimeInternals:
    """Stand in for the runtime's private operation cursor and checkpoint."""

    next_operation: str
    state: object

    def _peek_next_operation_id(self) -> str:
        return self.next_operation


@dataclass
class NoCursor:
    state: object


def callback_of(child_id: str) -> str:
    return hashlib.blake2b(f"{child_id}-1".encode()).hexdigest()[:64]


def test_a_replay_names_the_operation_an_earlier_invocation_opened() -> None:
    context = RuntimeInternals("child-7", Checkpoints({callback_of("child-7")}))

    assert replayed_operation(context) == callback_of("child-7")


def test_the_invocation_that_opens_the_callback_names_no_operation() -> None:
    context = RuntimeInternals("child-7", Checkpoints({callback_of("child-6")}))

    assert replayed_operation(context) is None


@pytest.mark.parametrize(
    "context",
    [
        NoCursor(Checkpoints({callback_of("child-7")})),
        RuntimeInternals("child-7", None),
        RuntimeInternals("child-7", OpaqueCheckpoints(object())),
        object(),
    ],
    ids=["no cursor", "no checkpoint", "unreadable checkpoint", "plain object"],
)
def test_a_runtime_without_its_internals_names_no_operation(context: object) -> None:
    assert replayed_operation(context) is None


def test_the_submitter_ignores_what_the_hand_off_returns(
    platform: InstallPlatform,
) -> None:
    _ = platform(issued())
    handed: list[str] = []

    def hand_off(token: str) -> int:
        handed.append(token)
        return len(handed)

    token_submitter(API_URL, "arn:execution", "payment", hand_off)("callback-4", None)

    assert handed == [TOKEN]


def test_the_submitter_refuses_a_hand_off_that_returns_an_awaitable(
    platform: InstallPlatform,
) -> None:
    _ = platform(issued())
    handed: list[str] = []
    started: list[Coroutine[object, object, None]] = []

    async def deliver(token: str) -> None:
        await asyncio.sleep(0)
        handed.append(token)

    def hand_off(token: str) -> Coroutine[object, object, None]:
        started.append(deliver(token))
        return started[-1]

    submit = token_submitter(API_URL, "arn:execution", "payment", hand_off)

    with pytest.raises(TypeError, match=SYNCHRONOUS):
        submit("callback-4", None)
    assert handed == []
    [coroutine] = started
    assert inspect.getcoroutinestate(coroutine) == inspect.CORO_CLOSED


class Pending:
    """An awaitable that is not a coroutine, as a future is."""

    def __await__(self) -> Generator[None]:
        yield


def test_the_submitter_refuses_an_awaitable_that_is_not_a_coroutine(
    platform: InstallPlatform,
) -> None:
    _ = platform(issued())
    submit = token_submitter(
        API_URL, "arn:execution", "payment", lambda _token: Pending()
    )

    with pytest.raises(TypeError, match=SYNCHRONOUS):
        submit("callback-4", None)


def test_the_submitter_skips_a_callback_that_already_closed(
    platform: InstallPlatform,
) -> None:
    _ = platform(refused(409, "callback_closed"))
    handed: list[str] = []
    submit = token_submitter(API_URL, "arn:execution", "payment", handed.append)

    submit("callback-4", None)

    assert handed == []


@pytest.mark.parametrize(
    ("result", "expected"),
    [
        ('{"charge": "ch_1"}', {"charge": "ch_1"}),
        (b'{"charge": "ch_1"}', {"charge": "ch_1"}),
        ('"done"', "done"),
        ("[1, 2]", [1, 2]),
        ({"items": (1, 2)}, {"items": [1, 2]}),
    ],
    ids=["text", "bytes", "string", "list", "decoded"],
)
def test_a_result_is_read_from_the_callback(
    result: object, expected: JSONValue
) -> None:
    assert callback_result(result) == expected


@pytest.mark.parametrize("result", ["{not json", b"\xff", {"a": {1, 2}}])
def test_an_unreadable_result_is_refused(result: object) -> None:
    with pytest.raises(TypeError, match=f"^{UNREADABLE_RESULT}$"):
        _ = callback_result(result)


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (
            {"type": "CardDeclined", "message": "Insufficient funds"},
            ("CardDeclined", "Insufficient funds"),
        ),
        ({"type": "Cancelled"}, ("Cancelled", "")),
        ({"type": "Cancelled", "message": 42}, ("Cancelled", "")),
        ({"type": "Cancelled", "message": ""}, ("Cancelled", "")),
    ],
    ids=["both", "no-message", "message-not-text", "empty-message"],
)
def test_a_failure_is_read_from_its_data(
    data: dict[str, JSONValue], expected: tuple[str, str]
) -> None:
    assert callback_failure(json.dumps(data)) == expected


@pytest.mark.parametrize(
    "data",
    [None, "not json", "[]", json.dumps({"message": "x"}), json.dumps({"type": 7})],
    ids=["none", "not-json", "list", "no-type", "type-not-text"],
)
def test_data_volcano_did_not_send_is_no_failure(data: str | None) -> None:
    assert callback_failure(data) is None


def test_a_failed_callback_error_carries_its_type_and_message() -> None:
    error = CallbackFailedError("CardDeclined", "Insufficient funds")

    assert error.type == "CardDeclined"
    assert error.message == "Insufficient funds"
    assert str(error) == "Insufficient funds"
