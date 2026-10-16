"""Register a durable approval with Volcano, and read the decision it returns."""

from __future__ import annotations

import re
from datetime import datetime
from typing import TYPE_CHECKING

from ._durable_callback import (
    callback_fields,
    has_nul,
    is_mapping,
    operation_name,
    text,
)
from ._durable_platform_request import PlatformRequest, encode, post_to_platform
from ._durable_response import json_value
from ._durable_results import ApprovalDecision
from ._transport_response import plain_json
from .models import DurableApprovalDecider

if TYPE_CHECKING:
    from collections.abc import Mapping

    from .models import JSONValue

_NOT_READY = "approval_not_ready"
_CLOSED = "approval_closed"
_MAX_BODY_BYTES = 65536
# The callback id is assigned once the callback opens, after the size check;
# the spec allows it 1024 characters.
_LONGEST_CALLBACK_ID = "x" * 1024
_TOO_LARGE = (
    "the approval is larger than the 64 KiB Volcano accepts once encoded as "
    "JSON; send less in details"
)
_INVALID_DECISION = "Expected a complete approval decision"
_INVALID_DETAILS = (
    "details must be JSON-serializable: mappings with string keys, lists, "
    "tuples, strings, finite numbers, booleans, and None"
)
# The limits on what the approval shows the person deciding.
_TEXT_LIMITS = {"title": 200, "description": 4000}
EXPIRED = ApprovalDecision(approved=False, status="expired")


def approval_body(
    name: object, title: object, description: object, details: object
) -> dict[str, JSONValue]:
    """Validate what the approval shows, before any callback is opened.

    Returns:
        The registration body without the execution reference or callback id.

    """
    body: dict[str, JSONValue] = {
        "name": operation_name(name),
        "title": _text(title, "title", required=True),
    }
    if description is not None:
        body["description"] = _text(description, "description", required=False)
    if details is not None:
        body["details"] = _details(details)
    return body


def _details(value: object) -> JSONValue:
    # A copy, so a change the caller makes while the callback opens cannot
    # slip past the checks.
    details = plain_json(json_value(value, _INVALID_DETAILS))
    if has_nul(details):
        message = "details must not contain NUL characters"
        raise ValueError(message)
    return details


def _text(value: object, field: str, *, required: bool) -> str:
    return text(value, field, limit=_TEXT_LIMITS[field], required=required)


def check_size(body: Mapping[str, JSONValue]) -> None:
    """Refuse an approval too large for Volcano, before any callback is opened.

    Raises:
        ValueError: The registration, with the longest callback id the runtime
            can assign, would encode to more than 64 KiB.

    """
    if len(encode({**body, "callback_id": _LONGEST_CALLBACK_ID})) > _MAX_BODY_BYTES:
        raise ValueError(_TOO_LARGE)


def register_approval(api_url: str, body: Mapping[str, JSONValue]) -> None:
    """Ask Volcano to record the approval and hold the callback for a person.

    The execution reference and callback id in the body are what Volcano
    checks against the running execution. An approval that already closed,
    normally because its timeout passed first, needs no registration: the
    callback's own outcome is what the execution resumes with. A refusal, or a
    failure that outlasts the retries, raises its `VolcanoError`.
    """
    _ = post_to_platform(
        api_url,
        PlatformRequest(
            "/durable-approvals", body, not_ready=_NOT_READY, closed=_CLOSED
        ),
    )


def approval_decision(result: object) -> ApprovalDecision:
    """Read the decision Volcano completed the callback with.

    Only the status has to be readable. The decision is already recorded, so
    refusing it over a detail would fail the execution again on every replay;
    an unreadable comment, decider, or decision time reads as absent instead.

    Returns:
        The approved or denied decision.

    Raises:
        TypeError: The callback result is not a decision.

    """
    values = callback_fields(result, _INVALID_DECISION)
    status = values.get("status")
    if status not in {"approved", "denied"}:
        raise TypeError(_INVALID_DECISION)
    approved = status == "approved"
    comment = values.get("comment")
    return ApprovalDecision(
        approved=approved,
        status="approved" if approved else "denied",
        comment=comment if isinstance(comment, str) else "",
        decided_by=_decider(values.get("decided_by")),
        decided_at=_decided_at(values.get("decided_at")),
    )


def _decider(value: object) -> DurableApprovalDecider | None:
    if not is_mapping(value):
        return None
    decider_id = value.get("id")
    email = value.get("email")
    if not isinstance(decider_id, str) or not isinstance(email, str):
        return None
    return DurableApprovalDecider(id=decider_id, email=email)


# RFC 3339 date-time, the form Volcano writes. fromisoformat alone also takes a
# bare date, a time without an offset, and other ISO 8601 shapes.
_TIMESTAMP = re.compile(
    (
        r"\d{4}-\d{2}-\d{2}T(?:[01]\d|2[0-3])(?::[0-5]\d){2}(?:\.\d+)?"
        r"(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)"
    ),
    re.ASCII,
)


def _decided_at(value: object) -> str | None:
    if not isinstance(value, str) or not _TIMESTAMP.fullmatch(value):
        return None
    # It also refuses an impossible day, such as February 30.
    try:
        _ = datetime.fromisoformat(value)
    except ValueError:
        return None
    return value
