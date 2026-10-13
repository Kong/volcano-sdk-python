"""Wait for, and publish, the messages a durable execution exchanges."""

from __future__ import annotations

from hashlib import sha256
from typing import TYPE_CHECKING

from ._durable_callback import callback_fields, has_nul, is_mapping
from ._durable_platform_request import PlatformRequest, encode, post_to_platform
from ._durable_response import json_value
from ._durable_results import PublishedMessage, ReceivedMessage
from ._transport_response import plain_json
from .models import DurableMessageSender

if TYPE_CHECKING:
    from collections.abc import Mapping

    from .models import JSONValue

SESSION_NAME = "volcano:messages-session"
_NOT_READY = "callback_not_ready"
_CLOSED = "callback_closed"
_SESSION_HEADER = "X-Volcano-Durable-Session"
_IDEMPOTENCY_HEADER = "Idempotency-Key"
_MAX_DATA_BYTES = 65536
_INVALID_DATA = (
    "data must be JSON-serializable: mappings with string keys, lists, "
    "tuples, strings, finite numbers, booleans, and None"
)
_UNREADABLE_MESSAGE = (
    "Volcano resumed the message wait with a message this SDK cannot read"
)
_UNREADABLE_SESSION = (
    "Volcano opened the messages session with a token this SDK cannot read"
)
_UNREADABLE_PUBLISH = "Volcano answered the publish with a message this SDK cannot read"


def message_data(value: object) -> JSONValue:
    """Validate what a publish sends, before its step runs.

    Returns:
        A plain copy, so a change the caller makes later cannot slip past the
        checks.

    Raises:
        ValueError: The data holds a NUL, or is over 64 KiB as JSON.

    """
    data = plain_json(json_value(value, _INVALID_DATA))
    if has_nul(data):
        message = "data must not contain NUL characters"
        raise ValueError(message)
    if len(encode(data)) > _MAX_DATA_BYTES:
        message = "data must be at most 64 KiB once encoded as JSON"
        raise ValueError(message)
    return data


def register_wait(
    api_url: str, execution_ref: str, callback_id: str, name: str
) -> None:
    """Ask Volcano to complete the callback with the next message of a name.

    A wait that already closed, normally because its timeout passed first,
    needs no registration: the callback's own outcome is what the execution
    resumes with.
    """
    body: dict[str, JSONValue] = {
        "execution_ref": execution_ref,
        "callback_id": callback_id,
        "name": name,
    }
    _ = post_to_platform(api_url, _registration("/durable-messages/waits", body))


def open_session(api_url: str, execution_ref: str, callback_id: str) -> None:
    """Ask Volcano to complete the callback with a token to publish with."""
    body: dict[str, JSONValue] = {
        "execution_ref": execution_ref,
        "callback_id": callback_id,
    }
    _ = post_to_platform(api_url, _registration("/durable-messages/sessions", body))


def _registration(path: str, body: Mapping[str, JSONValue]) -> PlatformRequest:
    return PlatformRequest(path, body, not_ready=_NOT_READY, closed=_CLOSED)


def publish_key(token: str, position: int) -> str:
    """Key a publish by its context's session and its place in that context.

    Unique within the execution, because every context has its own session,
    and the same when a step runs again. Hashed, so Volcano never stores the
    token itself.

    Returns:
        The idempotency key.

    """
    return f"{sha256(token.encode()).hexdigest()}:{position}"


def publish_message(
    api_url: str, token: str, key: str, message: Mapping[str, JSONValue]
) -> dict[str, JSONValue]:
    """Publish the message, or return the one this key already published.

    Returns:
        The message's id and seq, in the form the step checkpoints.

    """
    payload = post_to_platform(
        api_url,
        PlatformRequest(
            "/durable-messages/publish",
            message,
            headers={_SESSION_HEADER: token, _IDEMPOTENCY_HEADER: key},
        ),
    )
    published = published_message(payload)
    return {"id": published.id, "seq": published.seq}


def published_message(value: object) -> PublishedMessage:
    """Read a publish's answer, live or as its step recorded it.

    Returns:
        The published message's id and seq.

    Raises:
        TypeError: The value is not a published message.

    """
    if not is_mapping(value):
        raise TypeError(_UNREADABLE_PUBLISH)
    message_id = value.get("id")
    seq = value.get("seq")
    if not isinstance(message_id, str) or type(seq) is not int:
        raise TypeError(_UNREADABLE_PUBLISH)
    return PublishedMessage(id=message_id, seq=seq)


def received_message(result: object) -> ReceivedMessage:
    """Read the message Volcano completed a wait's callback with.

    Returns:
        The message.

    Raises:
        TypeError: The result is not a message.

    """
    values = callback_fields(result, _UNREADABLE_MESSAGE)
    message_id = values.get("id")
    name = values.get("name")
    sent_at = values.get("sent_at")
    if not (
        isinstance(message_id, str)
        and isinstance(name, str)
        and isinstance(sent_at, str)
    ):
        raise TypeError(_UNREADABLE_MESSAGE)
    return ReceivedMessage(
        id=message_id,
        name=name,
        data=json_value(values.get("data"), _UNREADABLE_MESSAGE),
        sender=_sender(values.get("sender")),
        sent_at=sent_at,
    )


def _sender(value: object) -> DurableMessageSender:
    if not is_mapping(value) or not isinstance(sender_type := value.get("type"), str):
        raise TypeError(_UNREADABLE_MESSAGE)
    user_id = value.get("user_id")
    return DurableMessageSender(
        type=sender_type, user_id=user_id if isinstance(user_id, str) else None
    )


def session_token(result: object) -> str:
    """Read the token Volcano completed a messages session's callback with.

    Returns:
        The session token.

    Raises:
        TypeError: The result carries no token.

    """
    token = callback_fields(result, _UNREADABLE_SESSION).get("token")
    if not isinstance(token, str) or not token:
        raise TypeError(_UNREADABLE_SESSION)
    return token
