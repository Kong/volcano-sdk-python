"""Register a durable approval with Volcano, and read the decision it returns."""

from __future__ import annotations

import json
import os
from collections.abc import Mapping
from time import monotonic, sleep
from typing import TYPE_CHECKING, TypeGuard

import httpx

from ._durable_response import json_value
from ._durable_results import ApprovalDecision
from ._transport_response import (
    invoke,
    plain_json,
    response_payload,
    unparsed_response,
)
from ._transport_types import HTTP_CREATED, HTTP_OK, decode_json
from .errors import (
    ConflictError,
    NotFoundError,
    RateLimitedError,
    ServerError,
    TransportError,
    VolcanoError,
)
from .models import DurableApprovalDecider

if TYPE_CHECKING:
    from .models import JSONValue

# 0.5 s doubling to a 5 s cap, within the deadline: long enough to outlast the
# moment the platform has not yet seen the execution start or the callback open.
_RETRY_DELAYS = (0.5, 1.0, 2.0, 4.0, 5.0, 5.0, 5.0, 5.0)
_DEADLINE_SECONDS = 30.0
_REQUEST_TIMEOUT_SECONDS = 10.0
_NOT_READY = "approval_not_ready"
_CLOSED = "approval_closed"
_HEADERS = {"Content-Type": "application/json"}
_MAX_BODY_BYTES = 65536
# The callback id is assigned once the callback opens, after the size check;
# the spec allows it 1024 characters.
_LONGEST_CALLBACK_ID = "x" * 1024
_TOO_LARGE = (
    "the approval is larger than the 64 KiB Volcano accepts once encoded as "
    "JSON; send less in details"
)
_INVALID_DECISION = "Expected a complete approval decision"
_API_URL_VARIABLE = "VOLCANO_PLATFORM_API_URL"
_MISSING_API_URL = (
    "wait_for_approval() needs VOLCANO_PLATFORM_API_URL. Volcano sets it on "
    "deployed durable functions; set it yourself to run the handler elsewhere."
)
_INVALID_DETAILS = (
    "details must be JSON-serializable: mappings with string keys, lists, "
    "tuples, strings, finite numbers, booleans, and None"
)
# The spec's limits on what the approval shows the person deciding.
_TEXT_LIMITS = {"name": 255, "title": 200, "description": 4000}
EXPIRED = ApprovalDecision(approved=False, status="expired")


def platform_api_url() -> str:
    """Read the Volcano API address the platform gives durable functions.

    Returns:
        The API base URL.

    Raises:
        RuntimeError: The variable is unset or empty.

    """
    url = os.environ.get(_API_URL_VARIABLE, "").strip()
    if not url:
        raise RuntimeError(_MISSING_API_URL)
    return url


def approval_body(
    name: object, title: object, description: object, details: object
) -> dict[str, JSONValue]:
    """Validate what the approval shows, before any callback is opened.

    Returns:
        The registration body without the execution reference or callback id.

    """
    body: dict[str, JSONValue] = {
        "name": _text(name, "name", required=True),
        "title": _text(title, "title", required=True),
    }
    if description is not None:
        body["description"] = _text(description, "description", required=False)
    if details is not None:
        body["details"] = json_value(details, _INVALID_DETAILS)
    return body


def _text(value: object, field: str, *, required: bool) -> str:
    if not isinstance(value, str):
        message = f"{field} must be a string"
        raise TypeError(message)
    try:
        _ = value.encode()
    except UnicodeEncodeError as error:
        message = f"{field} must be JSON-serializable: it contains a surrogate"
        raise TypeError(message) from error
    if required and not value.strip():
        message = f"{field} must not be empty"
        raise ValueError(message)
    limit = _TEXT_LIMITS[field]
    if len(value) > limit:
        message = f"{field} must be at most {limit} characters"
        raise ValueError(message)
    return value


def check_size(body: Mapping[str, JSONValue]) -> None:
    """Refuse an approval too large for Volcano, before any callback is opened.

    Raises:
        ValueError: The registration, with the longest callback id the runtime
            can assign, would encode to more than 64 KiB.

    """
    if len(_encode({**body, "callback_id": _LONGEST_CALLBACK_ID})) > _MAX_BODY_BYTES:
        raise ValueError(_TOO_LARGE)


def _encode(body: Mapping[str, JSONValue]) -> bytes:
    return json.dumps(
        plain_json(body), ensure_ascii=False, separators=(",", ":"), allow_nan=False
    ).encode()


def register_approval(api_url: str, body: Mapping[str, JSONValue]) -> None:
    """Ask Volcano to record the approval and hold the callback for a person.

    The route takes no credential: the execution reference and callback id in
    the body are what Volcano checks against the running execution.

    What can clear on its own is retried until a 30 second deadline: no
    answer, an execution or callback Volcano cannot see yet, throttling, and
    server failures. An approval that already closed, normally because its
    timeout passed first, needs no registration: the callback's own outcome
    is what the execution resumes with.

    Raises:
        VolcanoError: Volcano refused the approval, or kept failing until the
            deadline passed or the retries ran out.

    """
    url = f"{api_url.removesuffix('/')}/durable-approvals"
    content = _encode(body)
    deadline = monotonic() + _DEADLINE_SECONDS
    timeout = _REQUEST_TIMEOUT_SECONDS
    with httpx.Client() as client:
        for delay in _RETRY_DELAYS:
            try:
                _post(client, url, content, timeout)
            except VolcanoError as error:
                next_timeout = _next_timeout(error, delay, deadline)
                if next_timeout is None:
                    raise
                timeout = next_timeout
            else:
                return
        _post(client, url, content, timeout)


def _post(client: httpx.Client, url: str, content: bytes, timeout: float) -> None:
    response = unparsed_response(
        invoke(client.post, url, content=content, headers=_HEADERS, timeout=timeout)
    )
    if response.status_code == HTTP_CREATED:
        return
    try:
        _ = response_payload(response, HTTP_OK)
    except ConflictError as error:
        if error.code != _CLOSED:
            raise


def _retryable(error: VolcanoError) -> bool:
    # NotFoundError included: Volcano records an execution only once it has
    # started, so an approval that is its first operation can arrive first.
    if isinstance(
        error, (TransportError, NotFoundError, RateLimitedError, ServerError)
    ):
        return True
    return isinstance(error, ConflictError) and error.code == _NOT_READY


def _next_timeout(error: VolcanoError, delay: float, deadline: float) -> float | None:
    """Wait to retry a failed attempt, if it is worth retrying in the time left.

    Returns:
        The next attempt's timeout, or None when the failure is final.

    """
    if not _retryable(error) or monotonic() + delay >= deadline:
        return None
    sleep(delay)
    remaining = deadline - monotonic()
    if remaining <= 0:
        return None
    return min(_REQUEST_TIMEOUT_SECONDS, remaining)


def approval_decision(result: object) -> ApprovalDecision:
    """Read the decision Volcano completed the callback with.

    Returns:
        The approved or denied decision.

    Raises:
        TypeError: The callback result is not a decision.

    """
    values = _decision_fields(result)
    status = values.get("status")
    approved = status == "approved"
    if status not in {"approved", "denied"} or values.get("approved") is not approved:
        raise TypeError(_INVALID_DECISION)
    comment = values.get("comment", "")
    decided_at = values.get("decided_at")
    if not isinstance(comment, str) or not isinstance(decided_at, str):
        raise TypeError(_INVALID_DECISION)
    return ApprovalDecision(
        approved=approved,
        status="approved" if approved else "denied",
        comment=comment,
        decided_by=_decider(values.get("decided_by")),
        decided_at=decided_at,
    )


def _decision_fields(result: object) -> Mapping[str, object]:
    if isinstance(result, (str, bytes)):
        document = result.encode() if isinstance(result, str) else result
        try:
            result = decode_json(document)
        except ValueError as error:
            raise TypeError(_INVALID_DECISION) from error
    if not _is_fields(result):
        raise TypeError(_INVALID_DECISION)
    return result


def _is_fields(value: object) -> TypeGuard[Mapping[str, object]]:
    return _is_mapping(value) and all(isinstance(key, str) for key in value)


def _is_mapping(value: object) -> TypeGuard[Mapping[object, object]]:
    return isinstance(value, Mapping)


def _decider(value: object) -> DurableApprovalDecider | None:
    if value is None:
        return None
    if not _is_fields(value):
        raise TypeError(_INVALID_DECISION)
    decider_id = value.get("id")
    email = value.get("email")
    if not isinstance(decider_id, str) or not isinstance(email, str):
        raise TypeError(_INVALID_DECISION)
    return DurableApprovalDecider(id=decider_id, email=email)
