from __future__ import annotations

import json
from typing import TYPE_CHECKING, Protocol

import httpx
import pytest

from volcano_sdk import AuthenticationError, ConflictError, VolcanoError
from volcano_sdk._durable_message import (
    message_data,
    open_session,
    publish_key,
    publish_message,
    published_message,
    received_message,
    register_wait,
    session_token,
)
from volcano_sdk._durable_results import PublishedMessage, ReceivedMessage
from volcano_sdk._transport_types import decode_json
from volcano_sdk.models import DurableMessageSender

from .fixtures.durable_platform import Answer, Platform, install_platform, refused

if TYPE_CHECKING:
    from collections.abc import Callable

    from volcano_sdk.models import JSONValue

API_URL = "https://api.volcano.test"
TOKEN = "session-token"
# sha256("session-token"), as every SDK keys a publish.
TOKEN_DIGEST = "c101e911469c969171040b50d70543313cf968fdef5bacc780776f8fb399ab36"
UNREADABLE_MESSAGE = (
    "Volcano resumed the message wait with a message this SDK cannot read"
)
UNREADABLE_SESSION = (
    "Volcano opened the messages session with a token this SDK cannot read"
)
UNREADABLE_PUBLISH = "Volcano answered the publish with a message this SDK cannot read"
INVALID_DATA = (
    "data must be JSON-serializable: mappings with string keys, lists, "
    "tuples, strings, finite numbers, booleans, and None"
)


class InstallPlatform(Protocol):
    def __call__(self, *answers: Answer) -> Platform: ...


@pytest.fixture
def platform(monkeypatch: pytest.MonkeyPatch) -> InstallPlatform:
    def install(*answers: Answer) -> Platform:
        return install_platform(monkeypatch, *answers)

    return install


def registered() -> httpx.Response:
    return httpx.Response(201, json={"id": "wait-1"})


def published(status: int = 201, seq: int = 3) -> httpx.Response:
    return httpx.Response(
        status,
        json={
            "id": "message-1",
            "execution_id": "execution-1",
            "direction": "out",
            "seq": seq,
            "name": "progress",
            "data": {"done": 2},
            "sender": {"type": "execution", "user_id": None},
            "status": "published",
            "delivered_at": None,
            "sent_at": "2026-10-12T09:00:00Z",
        },
    )


def sent(request: httpx.Request) -> object:
    return decode_json(request.content)


def test_a_wait_registers_its_callback_for_the_name(
    platform: InstallPlatform,
) -> None:
    fake = platform(registered())

    register_wait(API_URL, "arn:execution/order-1", "callback-1", "approve")

    [request] = fake.requests
    assert request.method == "POST"
    assert str(request.url) == f"{API_URL}/durable-messages/waits"
    assert request.headers["Content-Type"] == "application/json"
    assert sent(request) == {
        "execution_ref": "arn:execution/order-1",
        "callback_id": "callback-1",
        "name": "approve",
    }


def test_a_session_opens_for_its_callback(platform: InstallPlatform) -> None:
    fake = platform(registered())

    open_session(API_URL, "arn:execution/order-1", "callback-2")

    [request] = fake.requests
    assert str(request.url) == f"{API_URL}/durable-messages/sessions"
    assert sent(request) == {
        "execution_ref": "arn:execution/order-1",
        "callback_id": "callback-2",
    }


@pytest.mark.parametrize(
    "register",
    [
        lambda: register_wait(API_URL, "arn:execution", "callback-1", "approve"),
        lambda: open_session(API_URL, "arn:execution", "callback-1"),
    ],
    ids=["wait", "session"],
)
def test_a_callback_the_runtime_has_not_recorded_yet_is_retried(
    platform: InstallPlatform, register: Callable[[], None]
) -> None:
    fake = platform(refused(409, "callback_not_ready"), registered())

    register()

    assert len(fake.requests) == 2
    assert fake.sleeps == [0.5]


@pytest.mark.parametrize(
    "register",
    [
        lambda: register_wait(API_URL, "arn:execution", "callback-1", "approve"),
        lambda: open_session(API_URL, "arn:execution", "callback-1"),
    ],
    ids=["wait", "session"],
)
def test_a_callback_that_already_closed_needs_no_registration(
    platform: InstallPlatform, register: Callable[[], None]
) -> None:
    fake = platform(refused(409, "callback_closed"))

    register()

    assert len(fake.requests) == 1
    assert fake.sleeps == []


@pytest.mark.parametrize(
    "code", ["too_many_message_waits", "execution_ended", "approval_closed", None]
)
def test_a_wait_refused_for_another_reason_raises_at_once(
    platform: InstallPlatform, code: str | None
) -> None:
    fake = platform(refused(409, code))

    with pytest.raises(ConflictError, match="refused with 409") as caught:
        register_wait(API_URL, "arn:execution", "callback-1", "approve")

    assert caught.value.code == code
    assert len(fake.requests) == 1


def test_a_session_refused_for_too_many_sessions_raises(
    platform: InstallPlatform,
) -> None:
    _ = platform(refused(409, "too_many_message_sessions"))

    with pytest.raises(ConflictError) as caught:
        open_session(API_URL, "arn:execution", "callback-1")

    assert caught.value.code == "too_many_message_sessions"


def test_publish_sends_the_session_and_key_and_returns_id_and_seq(
    platform: InstallPlatform,
) -> None:
    fake = platform(published())
    key = publish_key(TOKEN, 1)

    result = publish_message(
        API_URL, TOKEN, key, {"name": "progress", "data": {"done": 2}}
    )

    assert result == {"id": "message-1", "seq": 3}
    [request] = fake.requests
    assert str(request.url) == f"{API_URL}/durable-messages/publish"
    assert request.headers["X-Volcano-Durable-Session"] == TOKEN
    assert request.headers["Idempotency-Key"] == f"{TOKEN_DIGEST}:1"
    assert request.headers["Content-Type"] == "application/json"
    assert sent(request) == {"name": "progress", "data": {"done": 2}}


def test_a_repeated_publish_returns_the_message_already_published(
    platform: InstallPlatform,
) -> None:
    _ = platform(published(status=200, seq=7))

    result = publish_message(API_URL, TOKEN, "key", {"name": "progress"})

    assert result == {"id": "message-1", "seq": 7}


@pytest.mark.parametrize(
    "code",
    ["callback_not_ready", "callback_closed", "execution_not_running"],
)
def test_a_publish_conflict_is_never_retried_or_ignored(
    platform: InstallPlatform, code: str
) -> None:
    fake = platform(refused(409, code))

    with pytest.raises(ConflictError) as caught:
        _ = publish_message(API_URL, TOKEN, "key", {"name": "progress"})

    assert caught.value.code == code
    assert len(fake.requests) == 1


def test_a_publish_with_a_rejected_session_raises(platform: InstallPlatform) -> None:
    _ = platform(refused(401))

    with pytest.raises(AuthenticationError, match="refused with 401"):
        _ = publish_message(API_URL, TOKEN, "key", {"name": "progress"})


def test_a_publish_too_large_for_volcano_raises(platform: InstallPlatform) -> None:
    fake = platform(refused(413))

    with pytest.raises(VolcanoError) as caught:
        _ = publish_message(API_URL, TOKEN, "key", {"name": "progress"})

    assert caught.value.status == 413
    assert len(fake.requests) == 1


def test_a_publish_answered_without_a_message_raises(
    platform: InstallPlatform,
) -> None:
    _ = platform(httpx.Response(201, json={"id": "message-1"}))

    with pytest.raises(TypeError, match=UNREADABLE_PUBLISH):
        _ = publish_message(API_URL, TOKEN, "key", {"name": "progress"})


def test_a_publish_key_names_the_session_digest_and_position() -> None:
    assert publish_key(TOKEN, 1) == f"{TOKEN_DIGEST}:1"
    assert publish_key(TOKEN, 12) == f"{TOKEN_DIGEST}:12"
    assert publish_key("other-token", 1) != publish_key(TOKEN, 1)


@pytest.mark.parametrize(
    "value",
    [
        None,
        "message-1",
        {"seq": 1},
        {"id": "message-1"},
        {"id": 1, "seq": 1},
        {"id": "message-1", "seq": "1"},
        {"id": "message-1", "seq": 1.0},
        {"id": "message-1", "seq": True},
    ],
)
def test_an_unreadable_published_message_is_refused(value: object) -> None:
    with pytest.raises(TypeError, match=UNREADABLE_PUBLISH):
        _ = published_message(value)


def test_a_published_message_is_read_from_its_checkpoint() -> None:
    assert published_message({"id": "message-1", "seq": 0}) == PublishedMessage(
        id="message-1", seq=0
    )


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, None),
        ({"done": (1, 2)}, {"done": [1, 2]}),
        ("é" * 32767, "é" * 32767),
        ("x" * 65534, "x" * 65534),
    ],
    ids=["none", "tuple", "multibyte-limit", "limit"],
)
def test_message_data_returns_a_plain_copy(value: object, expected: object) -> None:
    assert message_data(value) == expected


def test_message_data_is_copied_before_it_is_sent() -> None:
    original: dict[str, JSONValue] = {"items": [1]}

    data = message_data(original)
    original["items"] = [2]

    assert data == {"items": [1]}


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ("x" * 65535, "data must be at most 64 KiB once encoded as JSON"),
        ("é" * 32768, "data must be at most 64 KiB once encoded as JSON"),
        ({"key\0": 1}, "data must not contain NUL characters"),
        (["\0"], "data must not contain NUL characters"),
    ],
)
def test_message_data_volcano_would_refuse_is_refused(
    value: object, message: str
) -> None:
    with pytest.raises(ValueError, match=f"^{message}$"):
        _ = message_data(value)


@pytest.mark.parametrize("value", [{1: "a"}, {"a": float("nan")}, {"a": {1, 2}}])
def test_message_data_that_is_not_json_is_refused(value: object) -> None:
    with pytest.raises(TypeError, match=f"^{INVALID_DATA}$"):
        _ = message_data(value)


def message_result(**overrides: object) -> dict[str, object]:
    message: dict[str, object] = {
        "id": "message-1",
        "name": "approve",
        "data": {"approved": True},
        "sender": {"type": "user", "user_id": "user-7"},
        "sent_at": "2026-10-12T09:00:00Z",
    }
    message.update(overrides)
    return message


@pytest.mark.parametrize(
    "result",
    [
        message_result(),
        json.dumps(message_result()),
        json.dumps(message_result()).encode(),
    ],
    ids=["decoded", "text", "bytes"],
)
def test_a_received_message_is_read_from_the_callback(result: object) -> None:
    assert received_message(result) == ReceivedMessage(
        id="message-1",
        name="approve",
        data={"approved": True},
        sender=DurableMessageSender(type="user", user_id="user-7"),
        sent_at="2026-10-12T09:00:00Z",
    )


def test_a_received_message_may_carry_no_data_or_user() -> None:
    message = received_message(
        message_result(data=None, sender={"type": "service_key", "user_id": None})
    )

    assert message.data is None
    assert message.sender == DurableMessageSender(type="service_key")


def test_a_sender_without_a_readable_user_has_none() -> None:
    message = received_message(message_result(sender={"type": "anon", "user_id": 7}))

    assert message.sender == DurableMessageSender(type="anon", user_id=None)


def test_received_data_stays_plain_for_the_handler_to_return() -> None:
    message = received_message(message_result(data={"items": [1, 2]}))

    assert message.data == {"items": [1, 2]}
    assert isinstance(message.data, dict)


@pytest.mark.parametrize(
    "result",
    [
        None,
        "not json",
        b"[1]",
        {1: "id"},
        message_result(id=None),
        message_result(name=1),
        message_result(sent_at=None),
        message_result(data={"a": {1, 2}}),
        message_result(sender=None),
        message_result(sender={"user_id": "user-7"}),
        message_result(sender={"type": 1}),
    ],
)
def test_an_unreadable_received_message_is_refused(result: object) -> None:
    with pytest.raises(TypeError, match=f"^{UNREADABLE_MESSAGE}$"):
        _ = received_message(result)


@pytest.mark.parametrize(
    "result", [{"token": TOKEN}, json.dumps({"token": TOKEN})], ids=["decoded", "text"]
)
def test_a_session_token_is_read_from_the_callback(result: object) -> None:
    assert session_token(result) == TOKEN


@pytest.mark.parametrize(
    "result", [None, "[]", {}, {"token": ""}, {"token": 1}, {"token": None}]
)
def test_an_unreadable_session_token_is_refused(result: object) -> None:
    with pytest.raises(TypeError, match=f"^{UNREADABLE_SESSION}$"):
        _ = session_token(result)
