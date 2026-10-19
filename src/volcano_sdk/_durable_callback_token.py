"""Hand a waiting step to another system, with a token Volcano issues for it."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._durable_callback import is_mapping
from ._durable_platform_request import PlatformRequest, post_to_platform
from ._durable_response import json_value
from ._transport_response import plain_json
from ._transport_types import decode_json
from .errors import ConflictError

if TYPE_CHECKING:
    from collections.abc import Callable

    from .models import JSONValue

_NOT_READY = "callback_not_ready"
_CLOSED = "callback_closed"
_UNREADABLE_REGISTRATION = (
    "Volcano registered the callback with a token this SDK cannot read"
)
_UNREADABLE_RESULT = "Volcano resumed the callback with a result this SDK cannot read"


class CallbackFailedError(Exception):
    """Raised by `ctx.wait_for_callback` when the token's holder fails it.

    `type` and `message` are what it sent. `type` is a name to branch on, such
    as `CardDeclined`.
    """

    def __init__(self, error_type: str, message: str) -> None:
        """Carry the failure's type and message."""
        super().__init__(message)
        self.type: str = error_type
        self.message: str = message


def token_submitter(
    api_url: str,
    execution_ref: str,
    name: str,
    hand_off: Callable[[str], object],
) -> Callable[[str, object], None]:
    """Build the runtime's submitter: register the callback, then hand its token on.

    It runs inside the runtime's checkpointed submitter step, so a replay does
    not register the callback again, and a step that runs again registers the
    same callback and gets the same token.

    Returns:
        The submitter the runtime calls with the callback's id.

    """

    def submit(callback_id: str, _context: object) -> None:
        token = register_callback(api_url, execution_ref, callback_id, name)
        # A closed callback already timed out; the wait resumes with that.
        if token is not None:
            _ = hand_off(token)

    return submit


def register_callback(
    api_url: str, execution_ref: str, callback_id: str, name: str
) -> str | None:
    """Ask Volcano for the token that completes the callback.

    Returns:
        The token, or None when the callback stopped waiting before the
        request landed, normally because its timeout passed first.

    Raises:
        ConflictError: Volcano refused the callback for another reason, such
            as the step being registered for something else.
        TypeError: Volcano answered without a token this SDK can read.

    """
    body: dict[str, JSONValue] = {
        "execution_ref": execution_ref,
        "callback_id": callback_id,
        "name": name,
    }
    try:
        answer = post_to_platform(
            api_url, PlatformRequest("/durable-callbacks", body, not_ready=_NOT_READY)
        )
    except ConflictError as error:
        if error.code != _CLOSED:
            raise
        return None
    token = answer.get("token") if is_mapping(answer) else None
    if not isinstance(token, str) or not token:
        raise TypeError(_UNREADABLE_REGISTRATION)
    return token


def callback_result(result: object) -> JSONValue:
    """Read the result the token's holder succeeded the callback with.

    The runtime hands it back as the JSON document Volcano sent, or already
    decoded.

    Returns:
        The result, as plain JSON.

    Raises:
        TypeError: The result is not JSON.

    """
    if isinstance(result, (str, bytes)):
        document = result.encode() if isinstance(result, str) else result
        try:
            result = decode_json(document)
        except ValueError as error:
            raise TypeError(_UNREADABLE_RESULT) from error
    return plain_json(json_value(result, _UNREADABLE_RESULT))


def callback_failure(data: str | None) -> tuple[str, str] | None:
    """Read the failure Volcano delivered from the runtime's error data.

    Volcano sends the failure's type and message as the error's data, because
    on replay the runtime rebuilds the error from its message and data alone.

    Returns:
        The failure's type and message, or None when the data is not one
        Volcano sent, as for a callback that ended because its execution
        stopped.

    """
    if data is None:
        return None
    try:
        value = decode_json(data.encode())
    except ValueError:
        return None
    if not is_mapping(value) or not isinstance(error_type := value.get("type"), str):
        return None
    message = value.get("message")
    return error_type, message if isinstance(message, str) else ""
