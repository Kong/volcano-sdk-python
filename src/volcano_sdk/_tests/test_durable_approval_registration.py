from __future__ import annotations

import json
from types import MappingProxyType
from typing import TYPE_CHECKING, Protocol

import httpx
import pytest

from volcano_sdk import (
    ConflictError,
    NotFoundError,
    RateLimitedError,
    ServerError,
    TransportError,
    ValidationError,
    VolcanoError,
)
from volcano_sdk._durable_approval_registration import (
    approval_body,
    approval_decision,
    platform_api_url,
    register_approval,
)
from volcano_sdk.durable_authoring import ApprovalDecision
from volcano_sdk.models import DurableApprovalDecider

if TYPE_CHECKING:
    from collections.abc import Callable

    from volcano_sdk.models import JSONValue

API_URL = "https://api.volcano.test"
BODY: dict[str, JSONValue] = {
    "execution_ref": "arn:execution/order-1234",
    "callback_id": "callback-1",
    "name": "ship-order",
    "title": "Ship order 1234?",
}
RETRY_DELAYS = [0.5, 1.0, 2.0, 4.0, 5.0, 5.0, 5.0, 5.0]
# The fixture replaces httpx.Client for the module under test, which is the
# same attribute everywhere.
REAL_CLIENT = httpx.Client


class Platform:
    """Answer registrations in order and record what was sent."""

    def __init__(self, *answers: httpx.Response | Exception) -> None:
        self.answers: list[httpx.Response | Exception] = list(answers)
        self.requests: list[httpx.Request] = []
        self.sleeps: list[float] = []
        self.client_timeouts: list[object] = []

    def handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        answer = self.answers[0] if len(self.answers) == 1 else self.answers.pop(0)
        if isinstance(answer, Exception):
            raise answer
        return answer

    def client(self, *, timeout: float) -> httpx.Client:
        self.client_timeouts.append(timeout)
        return REAL_CLIENT(timeout=timeout, transport=httpx.MockTransport(self.handle))


class InstallPlatform(Protocol):
    def __call__(self, *answers: httpx.Response | Exception) -> Platform: ...


@pytest.fixture
def platform(monkeypatch: pytest.MonkeyPatch) -> InstallPlatform:
    def install(*answers: httpx.Response | Exception) -> Platform:
        fake = Platform(*answers)
        monkeypatch.setattr(
            "volcano_sdk._durable_approval_registration.httpx.Client", fake.client
        )
        monkeypatch.setattr(
            "volcano_sdk._durable_approval_registration.sleep", fake.sleeps.append
        )
        return fake

    return install


def registered(status: int = 201) -> httpx.Response:
    return httpx.Response(
        status,
        json={"id": "approval-1", "status": "pending", "expires_at": None},
    )


def refused(status: int, code: str | None = None) -> httpx.Response:
    body = {"error": f"refused with {status}"}
    if code is not None:
        body["code"] = code
    return httpx.Response(status, json=body)


def test_registration_posts_the_body_without_credentials(
    platform: InstallPlatform,
) -> None:
    fake = platform(registered())

    register_approval(f"{API_URL}/", BODY)

    assert len(fake.requests) == 1
    request = fake.requests[0]
    assert request.method == "POST"
    assert str(request.url) == f"{API_URL}/durable-approvals"
    assert "authorization" not in request.headers
    assert request.headers["content-type"] == "application/json"
    assert json.loads(request.content) == BODY
    assert fake.sleeps == []
    assert fake.client_timeouts == [10.0]


def test_an_already_registered_approval_is_success(
    platform: InstallPlatform,
) -> None:
    fake = platform(registered(200))

    register_approval(API_URL, BODY)

    assert len(fake.requests) == 1
    assert fake.sleeps == []


def test_frozen_details_are_sent_as_json(platform: InstallPlatform) -> None:
    fake = platform(registered())
    details: JSONValue = MappingProxyType({"items": (1, 2)})

    register_approval(API_URL, {**BODY, "details": details})

    assert json.loads(fake.requests[0].content)["details"] == {"items": [1, 2]}


@pytest.mark.parametrize(
    "first",
    [
        pytest.param(refused(409, "approval_not_ready"), id="not ready"),
        pytest.param(refused(429), id="rate limited"),
        pytest.param(refused(503), id="unavailable"),
        pytest.param(refused(502), id="bad gateway"),
        pytest.param(httpx.ConnectError("connection refused"), id="network"),
    ],
)
def test_a_transient_failure_is_retried(
    platform: InstallPlatform, first: httpx.Response | Exception
) -> None:
    fake = platform(first, registered())

    register_approval(API_URL, BODY)

    assert len(fake.requests) == 2
    assert fake.sleeps == [0.5]
    assert json.loads(fake.requests[1].content) == BODY


def test_retries_back_off_to_a_cap_and_then_raise(
    platform: InstallPlatform,
) -> None:
    fake = platform(refused(503))

    with pytest.raises(ServerError, match="refused with 503") as caught:
        register_approval(API_URL, BODY)

    assert caught.value.status == 503
    assert fake.sleeps == RETRY_DELAYS
    assert len(fake.requests) == len(RETRY_DELAYS) + 1


def test_the_last_attempt_can_still_succeed(platform: InstallPlatform) -> None:
    fake = platform(*([refused(429)] * len(RETRY_DELAYS)), registered())

    register_approval(API_URL, BODY)

    assert fake.sleeps == RETRY_DELAYS
    assert len(fake.requests) == len(RETRY_DELAYS) + 1


def test_a_network_failure_that_persists_raises_a_transport_error(
    platform: InstallPlatform,
) -> None:
    fake = platform(httpx.ConnectError("connection refused"))

    with pytest.raises(TransportError, match="connection refused"):
        register_approval(API_URL, BODY)

    assert len(fake.requests) == len(RETRY_DELAYS) + 1


@pytest.mark.parametrize(
    ("answer", "expected"),
    [
        pytest.param(refused(400), ValidationError, id="invalid"),
        pytest.param(refused(404), NotFoundError, id="no execution"),
        pytest.param(refused(409, "approval_closed"), ConflictError, id="closed"),
        pytest.param(refused(409, "execution_ended"), ConflictError, id="ended"),
        pytest.param(refused(409), ConflictError, id="conflict"),
        pytest.param(refused(413), VolcanoError, id="too large"),
    ],
)
def test_a_refusal_is_raised_without_retrying(
    platform: InstallPlatform,
    answer: httpx.Response,
    expected: type[VolcanoError],
) -> None:
    fake = platform(answer)

    with pytest.raises(expected) as caught:
        register_approval(API_URL, BODY)

    assert type(caught.value) is expected
    assert caught.value.status == answer.status_code
    assert len(fake.requests) == 1
    assert fake.sleeps == []


def test_a_rate_limit_that_persists_raises_rate_limited(
    platform: InstallPlatform,
) -> None:
    _ = platform(refused(429))

    with pytest.raises(RateLimitedError):
        register_approval(API_URL, BODY)


def test_the_platform_api_url_comes_from_the_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("VOLCANO_PLATFORM_API_URL", f" {API_URL} ")

    assert platform_api_url() == API_URL


@pytest.mark.parametrize("value", [None, "", "  "])
def test_a_missing_platform_api_url_is_explained(
    monkeypatch: pytest.MonkeyPatch, value: str | None
) -> None:
    if value is None:
        monkeypatch.delenv("VOLCANO_PLATFORM_API_URL", raising=False)
    else:
        monkeypatch.setenv("VOLCANO_PLATFORM_API_URL", value)

    with pytest.raises(RuntimeError) as caught:
        _ = platform_api_url()

    assert str(caught.value) == (
        "wait_for_approval() needs VOLCANO_PLATFORM_API_URL. Volcano sets it on "
        "deployed durable functions; set it yourself to run the handler elsewhere."
    )


def test_the_body_carries_only_what_was_given() -> None:
    assert approval_body("ship", "Ship?", None, None) == {
        "name": "ship",
        "title": "Ship?",
    }
    assert approval_body("ship", "Ship?", "", {"a": [1]}) == {
        "name": "ship",
        "title": "Ship?",
        "description": "",
        "details": {"a": [1]},
    }


def test_text_at_its_limit_is_accepted() -> None:
    body = approval_body("n" * 255, "t" * 200, "d" * 4000, details=False)

    assert body == {
        "name": "n" * 255,
        "title": "t" * 200,
        "description": "d" * 4000,
        "details": False,
    }


@pytest.mark.parametrize(
    ("arguments", "error", "message"),
    [
        pytest.param(
            (3, "t", None, None), TypeError, "name must be a string", id="name type"
        ),
        pytest.param(
            (" ", "t", None, None), ValueError, "name must not be empty", id="blank"
        ),
        pytest.param(
            ("n" * 256, "t", None, None),
            ValueError,
            "name must be at most 255 characters",
            id="long name",
        ),
        pytest.param(
            ("n", None, None, None), TypeError, "title must be a string", id="title"
        ),
        pytest.param(
            ("n", "", None, None), ValueError, "title must not be empty", id="empty"
        ),
        pytest.param(
            ("n", "t" * 201, None, None),
            ValueError,
            "title must be at most 200 characters",
            id="long title",
        ),
        pytest.param(
            ("n", "t", 1, None),
            TypeError,
            "description must be a string",
            id="description type",
        ),
        pytest.param(
            ("n", "t", "d" * 4001, None),
            ValueError,
            "description must be at most 4000 characters",
            id="long description",
        ),
        pytest.param(
            ("n", "t", None, {"when": object()}),
            TypeError,
            "details must be a JSON value",
            id="details",
        ),
        pytest.param(
            ("n", "t", None, float("nan")),
            TypeError,
            "details must be a JSON value",
            id="nan details",
        ),
    ],
)
def test_an_invalid_body_is_refused(
    arguments: tuple[object, object, object, object],
    error: type[Exception],
    message: str,
) -> None:
    with pytest.raises(error) as caught:
        _ = approval_body(*arguments)

    assert str(caught.value) == message


DECIDED_BY = {"id": "user-7", "email": "ops@example.com"}


def as_bytes(value: object) -> object:
    return json.dumps(value).encode()


def as_decoded(value: object) -> object:
    return value


@pytest.mark.parametrize(
    "encode",
    [
        pytest.param(json.dumps, id="string"),
        pytest.param(as_bytes, id="bytes"),
        pytest.param(as_decoded, id="decoded"),
    ],
)
def test_an_approval_decision_is_read(encode: Callable[[object], object]) -> None:
    result = encode(
        {
            "status": "approved",
            "approved": True,
            "comment": "Ship it",
            "decided_by": DECIDED_BY,
            "decided_at": "2026-10-06T12:05:00Z",
        }
    )

    assert approval_decision(result) == ApprovalDecision(
        approved=True,
        status="approved",
        comment="Ship it",
        decided_by=DurableApprovalDecider(id="user-7", email="ops@example.com"),
        decided_at="2026-10-06T12:05:00Z",
    )


def test_a_denial_is_a_decision_and_the_comment_defaults_to_empty() -> None:
    result = json.dumps(
        {
            "status": "denied",
            "approved": False,
            "decided_by": None,
            "decided_at": "2026-10-06T12:05:00Z",
        }
    )

    assert approval_decision(result) == ApprovalDecision(
        approved=False,
        status="denied",
        comment="",
        decided_by=None,
        decided_at="2026-10-06T12:05:00Z",
    )


def test_an_expired_decision_has_nothing_but_its_status() -> None:
    expired = ApprovalDecision(approved=False, status="expired")

    assert (expired.comment, expired.decided_by, expired.decided_at) == (
        "",
        None,
        None,
    )


def complete_decision(**overrides: object) -> dict[str, object]:
    decision: dict[str, object] = {
        "status": "approved",
        "approved": True,
        "comment": "",
        "decided_by": DECIDED_BY,
        "decided_at": "2026-10-06T12:05:00Z",
    }
    decision.update(overrides)
    return decision


@pytest.mark.parametrize(
    "result",
    [
        pytest.param(None, id="none"),
        pytest.param("not json", id="not json"),
        pytest.param(b"\xff", id="not utf-8"),
        pytest.param("[]", id="list"),
        pytest.param({1: "approved"}, id="key"),
        pytest.param(complete_decision(status="expired"), id="status"),
        pytest.param(complete_decision(status=None), id="no status"),
        pytest.param(complete_decision(approved=False), id="disagrees"),
        pytest.param(complete_decision(status="denied"), id="denied but approved"),
        pytest.param(complete_decision(approved=1), id="approved type"),
        pytest.param(complete_decision(comment=None), id="comment"),
        pytest.param(complete_decision(decided_at=None), id="decided at"),
        pytest.param(complete_decision(decided_by="ops"), id="decider"),
        pytest.param(complete_decision(decided_by={1: "ops"}), id="decider key"),
        pytest.param(complete_decision(decided_by={"id": "u"}), id="decider email"),
        pytest.param(
            complete_decision(decided_by={"email": "ops@example.com"}), id="decider id"
        ),
    ],
)
def test_a_malformed_decision_is_refused(result: object) -> None:
    with pytest.raises(TypeError, match="Expected a complete approval decision"):
        _ = approval_decision(result)
