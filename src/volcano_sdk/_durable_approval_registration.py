"""Register a durable approval with Volcano, and read the decision it returns."""

from __future__ import annotations

import os
from collections.abc import Mapping
from time import sleep
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
    RateLimitedError,
    ServerError,
    TransportError,
    VolcanoError,
)
from .models import DurableApprovalDecider

if TYPE_CHECKING:
    from .models import JSONValue

# 0.5 s doubling to a 5 s cap, about 30 s in all: long enough to outlast the
# moment the platform has not yet seen the callback open.
_RETRY_DELAYS = (0.5, 1.0, 2.0, 4.0, 5.0, 5.0, 5.0, 5.0)
_REQUEST_TIMEOUT_SECONDS = 10.0
_NOT_READY = "approval_not_ready"
_INVALID_DECISION = "Expected a complete approval decision"
_API_URL_VARIABLE = "VOLCANO_PLATFORM_API_URL"
_MISSING_API_URL = (
    "wait_for_approval() needs VOLCANO_PLATFORM_API_URL. Volcano sets it on "
    "deployed durable functions; set it yourself to run the handler elsewhere."
)
_INVALID_DETAILS = "details must be a JSON value"
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
    if required and not value.strip():
        message = f"{field} must not be empty"
        raise ValueError(message)
    limit = _TEXT_LIMITS[field]
    if len(value) > limit:
        message = f"{field} must be at most {limit} characters"
        raise ValueError(message)
    return value


def register_approval(api_url: str, body: Mapping[str, JSONValue]) -> None:
    """Ask Volcano to record the approval and hold the callback for a person.

    The route takes no credential: the execution reference and callback id in
    the body are what Volcano checks against the running execution.

    Raises:
        VolcanoError: Volcano refused the approval, or kept failing until the
            retries ran out.

    """
    url = f"{api_url.removesuffix('/')}/durable-approvals"
    with httpx.Client(timeout=_REQUEST_TIMEOUT_SECONDS) as client:
        for delay in _RETRY_DELAYS:
            try:
                _post(client, url, body)
            except VolcanoError as error:
                if not _retryable(error):
                    raise
                sleep(delay)
            else:
                return
        _post(client, url, body)


def _post(client: httpx.Client, url: str, body: Mapping[str, JSONValue]) -> None:
    response = unparsed_response(invoke(client.post, url, json=plain_json(body)))
    if response.status_code != HTTP_CREATED:
        _ = response_payload(response, HTTP_OK)


def _retryable(error: VolcanoError) -> bool:
    if isinstance(error, (TransportError, RateLimitedError, ServerError)):
        return True
    return isinstance(error, ConflictError) and error.code == _NOT_READY


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
