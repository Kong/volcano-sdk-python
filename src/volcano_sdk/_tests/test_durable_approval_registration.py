from __future__ import annotations

import asyncio
import json
import time
from types import MappingProxyType
from typing import TYPE_CHECKING, NoReturn, Protocol, TypeAlias

import httpx
import pytest
from typing_extensions import override

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
    check_size,
    platform_api_url,
    register_approval,
)
from volcano_sdk.durable_authoring import ApprovalDecision
from volcano_sdk.models import DurableApprovalDecider

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Callable

    from volcano_sdk.models import JSONValue

API_URL = "https://api.volcano.test"
BODY: dict[str, JSONValue] = {
    "execution_ref": "arn:execution/order-1234",
    "callback_id": "callback-1",
    "name": "ship-order",
    "title": "Ship order 1234?",
}
RETRY_DELAYS = [0.5, 1.0, 2.0, 4.0, 5.0, 5.0, 5.0, 5.0]
# The fixture replaces httpx.AsyncClient for the module under test, which is
# the same attribute everywhere.
REAL_CLIENT = httpx.AsyncClient
REGISTRATION = "volcano_sdk._durable_approval_registration"
INVALID_DETAILS = (
    "details must be JSON-serializable: mappings with string keys, lists, "
    "tuples, strings, finite numbers, booleans, and None"
)
# Long past any attempt's deadline: a slow answer still running by then was
# never cut off, and ends rather than hang the suite.
_GIVE_UP_SECONDS = 10.0
_TRICKLE_INTERVAL = 0.01
_NEVER_CANCELLED = "the attempt outlived its deadline"


class Stall:
    """Accept the request and never answer it."""

    def __init__(self) -> None:
        self.released: bool = False

    async def hold(self) -> NoReturn:
        try:
            await asyncio.sleep(_GIVE_UP_SECONDS)
        finally:
            self.released = True
        raise AssertionError(_NEVER_CANCELLED)


class Trickle(httpx.AsyncByteStream):
    """Send a body one byte at a time, each well inside any read timeout."""

    def __init__(self) -> None:
        self.sent: int = 0
        self.closed: bool = False

    @override
    async def __aiter__(self) -> AsyncIterator[bytes]:
        for _ in range(int(_GIVE_UP_SECONDS / _TRICKLE_INTERVAL)):
            await asyncio.sleep(_TRICKLE_INTERVAL)
            self.sent += 1
            yield b" "

    @override
    async def aclose(self) -> None:
        self.closed = True


class Flood(httpx.AsyncByteStream):
    """Send a body as fast as it is read, forever."""

    def __init__(self) -> None:
        self.sent: int = 0

    @override
    async def __aiter__(self) -> AsyncIterator[bytes]:
        while True:
            self.sent += 4096
            yield b" " * 4096


class Pieces(httpx.AsyncByteStream):
    """Send a body split into the given pieces."""

    def __init__(self, *pieces: bytes) -> None:
        self.pieces: tuple[bytes, ...] = pieces

    @override
    async def __aiter__(self) -> AsyncIterator[bytes]:
        for piece in self.pieces:
            yield piece


Answer: TypeAlias = "httpx.Response | Exception | Stall"


class Platform:
    """Answer registrations in order and record what was sent.

    Time is the platform's own: it passes while the registration sleeps and
    while a request runs into its timeout, and nowhere else. An attempt that
    is cancelled at its deadline takes real time, not platform time.
    """

    def __init__(self, *answers: Answer) -> None:
        self.answers: list[Answer] = list(answers)
        self.requests: list[httpx.Request] = []
        self.timeouts: list[float] = []
        self.sleeps: list[float] = []
        self.now: float = 0.0
        # How much longer than asked each sleep takes.
        self.oversleep: float = 0.0
        self.clock_runs: bool = True

    async def handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        match request.extensions:
            case {"timeout": {"read": float(timeout)}}:
                self.timeouts.append(timeout)
            case _:
                message = f"expected a read timeout, got {request.extensions}"
                raise AssertionError(message)
        answer = self.answers[0] if len(self.answers) == 1 else self.answers.pop(0)
        if isinstance(answer, Stall):
            await answer.hold()
        if isinstance(answer, httpx.TimeoutException):
            self.advance(timeout)
        if isinstance(answer, Exception):
            raise answer
        return answer

    def client(self, *, timeout: float) -> httpx.AsyncClient:
        return REAL_CLIENT(transport=httpx.MockTransport(self.handle), timeout=timeout)

    def monotonic(self) -> float:
        return self.now

    def sleep(self, delay: float) -> None:
        self.sleeps.append(delay)
        self.advance(delay + self.oversleep)

    def advance(self, seconds: float) -> None:
        if self.clock_runs:
            self.now += seconds


class InstallPlatform(Protocol):
    def __call__(self, *answers: Answer) -> Platform: ...


@pytest.fixture
def platform(monkeypatch: pytest.MonkeyPatch) -> InstallPlatform:
    def install(*answers: Answer) -> Platform:
        fake = Platform(*answers)
        monkeypatch.setattr(f"{REGISTRATION}.httpx.AsyncClient", fake.client)
        monkeypatch.setattr(f"{REGISTRATION}.monotonic", fake.monotonic)
        monkeypatch.setattr(f"{REGISTRATION}.sleep", fake.sleep)
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
    assert request.extensions["timeout"] == dict.fromkeys(
        ("connect", "read", "write", "pool"), 10.0
    )
    assert fake.sleeps == []


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
        pytest.param(refused(404), id="execution not recorded yet"),
        pytest.param(refused(429), id="rate limited"),
        pytest.param(refused(500), id="server error"),
        pytest.param(refused(503), id="unavailable"),
        pytest.param(refused(502), id="bad gateway"),
        pytest.param(httpx.ConnectError("connection refused"), id="network"),
        pytest.param(httpx.ReadTimeout("timed out"), id="timeout"),
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


@pytest.mark.parametrize(
    ("answers", "sleeps"),
    [
        pytest.param([refused(409, "approval_closed")], [], id="at once"),
        pytest.param(
            [refused(404), refused(409, "approval_closed")], [0.5], id="on a retry"
        ),
    ],
)
def test_an_approval_that_already_closed_needs_no_registration(
    platform: InstallPlatform, answers: list[httpx.Response], sleeps: list[float]
) -> None:
    fake = platform(*answers)

    register_approval(API_URL, BODY)

    assert len(fake.requests) == len(answers)
    assert fake.sleeps == sleeps


def test_retries_back_off_until_the_deadline_and_then_raise(
    platform: InstallPlatform,
) -> None:
    fake = platform(refused(503))

    with pytest.raises(ServerError, match="refused with 503") as caught:
        register_approval(API_URL, BODY)

    assert caught.value.status == 503
    assert fake.sleeps == RETRY_DELAYS
    assert len(fake.requests) == len(RETRY_DELAYS) + 1
    # The last attempt starts 27.5 s in and gets only what is left.
    assert fake.timeouts[-1] == pytest.approx(2.5)


def test_the_last_attempt_before_the_deadline_can_still_succeed(
    platform: InstallPlatform,
) -> None:
    fake = platform(*([refused(429)] * len(RETRY_DELAYS)), registered())

    register_approval(API_URL, BODY)

    assert fake.sleeps == RETRY_DELAYS
    assert len(fake.requests) == len(RETRY_DELAYS) + 1


def test_the_schedule_bounds_the_attempts_while_time_is_left(
    platform: InstallPlatform,
) -> None:
    fake = platform(refused(503))
    fake.clock_runs = False

    with pytest.raises(ServerError, match="refused with 503"):
        register_approval(API_URL, BODY)

    assert fake.sleeps == RETRY_DELAYS
    assert len(fake.requests) == len(RETRY_DELAYS) + 1
    assert fake.timeouts == [10.0] * (len(RETRY_DELAYS) + 1)


def test_each_attempt_is_given_what_is_left_of_the_deadline(
    platform: InstallPlatform,
) -> None:
    fake = platform(httpx.ReadTimeout("timed out"))

    with pytest.raises(TransportError, match="timed out"):
        register_approval(API_URL, BODY)

    assert fake.timeouts == [10.0, 10.0, 8.5]
    assert fake.sleeps == [0.5, 1.0]


def test_a_late_wake_up_leaves_the_retry_only_the_time_left(
    platform: InstallPlatform,
) -> None:
    fake = platform(httpx.ReadTimeout("timed out"), registered())
    fake.oversleep = 19.0

    register_approval(API_URL, BODY)

    assert fake.sleeps == [0.5]
    assert fake.timeouts == [10.0, 0.5]


def test_waking_up_at_the_deadline_raises_the_last_failure(
    platform: InstallPlatform,
) -> None:
    fake = platform(httpx.ReadTimeout("timed out"))
    fake.oversleep = 19.5

    with pytest.raises(TransportError, match="timed out"):
        register_approval(API_URL, BODY)

    assert fake.sleeps == [0.5]
    assert fake.timeouts == [10.0]


def test_a_retry_that_would_wake_at_the_deadline_is_not_slept_for(
    platform: InstallPlatform,
) -> None:
    # The retry wakes 29 s in; its attempt fails, and the next delay of 1 s
    # would end exactly at the deadline.
    fake = platform(refused(503))
    fake.oversleep = 28.5

    with pytest.raises(ServerError, match="refused with 503"):
        register_approval(API_URL, BODY)

    assert fake.sleeps == [0.5]
    assert fake.timeouts == [10.0, 1.0]


# Nothing in a mock transport times out, so only the attempt's own deadline can
# end these early. The retry wakes 29.8 s in, which leaves its attempt 0.2 s.
_WAKE_LATE = 29.3
_ENDED_PROMPTLY = 3.0


def test_an_attempt_ends_by_its_deadline_when_volcano_never_answers(
    platform: InstallPlatform,
) -> None:
    stall = Stall()
    fake = platform(refused(503), stall)
    fake.oversleep = _WAKE_LATE
    started = time.perf_counter()

    with pytest.raises(TransportError) as caught:
        register_approval(API_URL, BODY)

    assert time.perf_counter() - started < _ENDED_PROMPTLY
    assert str(caught.value) == "Volcano did not answer within 0.2 seconds"
    assert stall.released
    assert fake.timeouts == [10.0, pytest.approx(0.2)]
    assert fake.sleeps == [0.5]


def test_an_attempt_ends_by_its_deadline_while_the_answer_trickles_in(
    platform: InstallPlatform,
) -> None:
    # Each byte arrives long before any per-read timeout would fire.
    trickle = Trickle()
    fake = platform(refused(503), httpx.Response(503, stream=trickle))
    fake.oversleep = _WAKE_LATE
    started = time.perf_counter()

    with pytest.raises(TransportError) as caught:
        register_approval(API_URL, BODY)

    assert time.perf_counter() - started < _ENDED_PROMPTLY
    assert str(caught.value) == "Volcano did not answer within 0.2 seconds"
    assert trickle.sent > 0
    assert trickle.closed
    assert fake.timeouts == [10.0, pytest.approx(0.2)]


def test_an_answer_too_large_to_be_volcanos_is_not_read_to_the_end(
    platform: InstallPlatform,
) -> None:
    flood = Flood()
    fake = platform(httpx.Response(409, stream=flood))

    with pytest.raises(ConflictError) as caught:
        register_approval(API_URL, BODY)

    assert caught.value.code is None
    assert flood.sent <= 65536 + 4096
    assert len(fake.requests) == 1


def test_an_answer_at_the_size_limit_is_read(platform: InstallPlatform) -> None:
    closed = refused(409, "approval_closed").content
    fake = platform(httpx.Response(409, content=closed.ljust(65536)))

    register_approval(API_URL, BODY)

    assert len(fake.requests) == 1


def test_an_answer_that_arrives_in_pieces_is_read_whole(
    platform: InstallPlatform,
) -> None:
    closed = refused(409, "approval_closed").content
    middle = len(closed) // 2
    fake = platform(
        httpx.Response(409, stream=Pieces(closed[:middle], closed[middle:]))
    )

    register_approval(API_URL, BODY)

    assert len(fake.requests) == 1


@pytest.mark.parametrize(
    ("answer", "expected"),
    [
        pytest.param(refused(404), NotFoundError, id="no execution"),
        pytest.param(refused(429), RateLimitedError, id="rate limited"),
        pytest.param(
            httpx.ConnectError("connection refused"), TransportError, id="network"
        ),
    ],
)
def test_a_failure_that_persists_raises_its_own_error(
    platform: InstallPlatform,
    answer: httpx.Response | Exception,
    expected: type[VolcanoError],
) -> None:
    fake = platform(answer)

    with pytest.raises(expected) as caught:
        register_approval(API_URL, BODY)

    assert type(caught.value) is expected
    assert len(fake.requests) == len(RETRY_DELAYS) + 1


@pytest.mark.parametrize(
    ("answer", "expected"),
    [
        pytest.param(refused(400), ValidationError, id="invalid"),
        pytest.param(refused(409, "execution_ended"), ConflictError, id="ended"),
        pytest.param(
            refused(409, "too_many_pending_approvals"), ConflictError, id="too many"
        ),
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
            ("n\ud800", "t", None, None),
            TypeError,
            "name must be JSON-serializable: it contains a surrogate",
            id="surrogate name",
        ),
        pytest.param(
            ("n", "\udfff", None, None),
            TypeError,
            "title must be JSON-serializable: it contains a surrogate",
            id="surrogate title",
        ),
        pytest.param(
            ("n", "t", "\ud83d", None),
            TypeError,
            "description must be JSON-serializable: it contains a surrogate",
            id="surrogate description",
        ),
        pytest.param(
            ("n", "t", None, {"when": object()}),
            TypeError,
            INVALID_DETAILS,
            id="details",
        ),
        pytest.param(
            ("n", "t", None, float("nan")),
            TypeError,
            INVALID_DETAILS,
            id="nan details",
        ),
        pytest.param(
            ("n", "t", None, {"note": "\ud800"}),
            TypeError,
            INVALID_DETAILS,
            id="surrogate details",
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


def test_whitespace_is_kept_and_only_blank_text_is_refused() -> None:
    assert approval_body(" ship ", "\tShip?\n", "  ", None) == {
        "name": " ship ",
        "title": "\tShip?\n",
        "description": "  ",
    }
    with pytest.raises(ValueError, match="name must not be empty"):
        _ = approval_body("\u00a0\u2003", "t", None, None)


LONGEST_CALLBACK_ID = "c" * 1024


def sized_body(size: int) -> dict[str, JSONValue]:
    """Pad a body to encode, with the longest callback id, to `size` bytes.

    Returns:
        The body, without the callback id.
    """
    body: dict[str, JSONValue] = {
        "name": "ship-order",
        "title": "Ship?",
        "execution_ref": "arn:" + "e" * 2044,
        "details": "",
    }
    encoded = json.dumps(
        {**body, "callback_id": LONGEST_CALLBACK_ID},
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode()
    # Three bytes each in UTF-8, so the body is measured as sent, not escaped.
    euros, rest = divmod(size - len(encoded), 3)
    body["details"] = "\u20ac" * euros + "d" * rest
    return body


def test_an_approval_at_the_size_limit_is_sent_as_measured(
    platform: InstallPlatform,
) -> None:
    fake = platform(registered())
    body = sized_body(65536)

    check_size(body)
    register_approval(API_URL, {**body, "callback_id": LONGEST_CALLBACK_ID})

    assert len(fake.requests[0].content) == 65536
    assert json.loads(fake.requests[0].content)["details"] == body["details"]


def test_a_body_that_is_not_json_is_never_sent(platform: InstallPlatform) -> None:
    fake = platform(registered())

    with pytest.raises(ValueError, match="not JSON compliant"):
        register_approval(API_URL, {**BODY, "details": float("nan")})

    assert fake.requests == []


def test_an_approval_over_the_size_limit_is_refused() -> None:
    with pytest.raises(ValueError, match="64 KiB") as caught:
        check_size(sized_body(65537))

    assert str(caught.value) == (
        "the approval is larger than the 64 KiB Volcano accepts once encoded as "
        "JSON; send less in details"
    )


def test_the_size_limit_counts_encoded_bytes() -> None:
    body: dict[str, JSONValue] = {
        "name": "ship-order",
        "title": "Ship?",
        "execution_ref": "arn:execution",
        "details": "\u20ac" * 21_500,
    }

    with pytest.raises(ValueError, match="64 KiB"):
        check_size(body)
    check_size({**body, "details": "d" * 21_500})


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


def without(field: str) -> dict[str, object]:
    decision = complete_decision()
    del decision[field]
    return decision


@pytest.mark.parametrize(
    "result",
    [
        pytest.param(None, id="none"),
        pytest.param("not json", id="not json"),
        pytest.param(b"\xff", id="not utf-8"),
        pytest.param("[]", id="list"),
        pytest.param({1: "approved"}, id="key"),
        pytest.param(complete_decision(status="expired"), id="expired"),
        pytest.param(complete_decision(status="Approved"), id="status case"),
        pytest.param(complete_decision(status=None), id="null status"),
        pytest.param(complete_decision(status=True), id="status type"),
        pytest.param(without("status"), id="no status"),
    ],
)
def test_a_decision_without_a_readable_status_is_refused(result: object) -> None:
    with pytest.raises(TypeError, match="Expected a complete approval decision"):
        _ = approval_decision(result)


@pytest.mark.parametrize(
    ("result", "expected"),
    [
        pytest.param(
            complete_decision(approved=False),
            ApprovalDecision(
                approved=True,
                status="approved",
                decided_by=DurableApprovalDecider(id="user-7", email="ops@example.com"),
                decided_at="2026-10-06T12:05:00Z",
            ),
            id="approved disagrees with status",
        ),
        pytest.param(
            complete_decision(status="denied", approved="yes"),
            ApprovalDecision(
                approved=False,
                status="denied",
                decided_by=DurableApprovalDecider(id="user-7", email="ops@example.com"),
                decided_at="2026-10-06T12:05:00Z",
            ),
            id="denied whatever approved says",
        ),
        pytest.param(
            {"status": "approved"},
            ApprovalDecision(approved=True, status="approved"),
            id="status alone",
        ),
    ],
)
def test_the_status_alone_decides(result: object, expected: ApprovalDecision) -> None:
    assert approval_decision(result) == expected


@pytest.mark.parametrize(
    ("result", "expected"),
    [
        pytest.param(without("comment"), {"comment": ""}, id="no comment"),
        pytest.param(complete_decision(comment=None), {"comment": ""}, id="null"),
        pytest.param(complete_decision(comment=7), {"comment": ""}, id="comment type"),
        pytest.param(without("decided_at"), {"decided_at": None}, id="no time"),
        pytest.param(
            complete_decision(decided_at=None), {"decided_at": None}, id="null time"
        ),
        pytest.param(
            complete_decision(decided_at=""), {"decided_at": None}, id="empty time"
        ),
        pytest.param(
            complete_decision(decided_at="yesterday"),
            {"decided_at": None},
            id="not a time",
        ),
        pytest.param(
            complete_decision(decided_at=1_791_288_300),
            {"decided_at": None},
            id="epoch seconds",
        ),
        *(
            pytest.param(
                complete_decision(decided_at=value), {"decided_at": None}, id=case
            )
            for case, value in [
                ("bare year", "2026"),
                ("date without a time", "2026-10-06"),
                ("time without an offset", "2026-10-06T12:05:00"),
                ("time without seconds", "2026-10-06T12:05Z"),
                ("space for the T", "2026-10-06 12:05:00Z"),
                ("basic format", "20261006T120500Z"),
                ("text before it", "at 2026-10-06T12:05:00Z"),
                ("text after it", "2026-10-06T12:05:00Z UTC"),
                ("interval", "2026-10-06T12:05:00Z/2026-10-07T12:05:00Z"),
                ("day zero", "2026-10-00T12:05:00Z"),
                ("impossible day of any month", "2026-10-32T12:05:00Z"),
                ("impossible day", "2026-02-30T12:05:00Z"),
                ("impossible hour", "2026-10-06T24:00:00Z"),
                ("three-digit hour", "2026-10-06T012:05:00Z"),
                ("impossible month", "2026-13-06T12:05:00Z"),
                ("impossible offset", "2026-10-06T12:05:00+24:00"),
                ("leap second", "2026-10-06T23:59:60Z"),
            ]
        ),
        *(
            pytest.param(
                complete_decision(decided_at=value), {"decided_at": value}, id=case
            )
            for case, value in [
                ("last day of a month kept", "2026-10-31T12:05:00Z"),
                ("latest time and widest offset kept", "2026-10-06T23:59:59-23:59"),
            ]
        ),
        pytest.param(
            complete_decision(decided_at="2026-10-06T12:05:00.123456+02:00"),
            {"decided_at": "2026-10-06T12:05:00.123456+02:00"},
            id="offset time kept as sent",
        ),
        pytest.param(
            complete_decision(decided_at="2028-02-29T12:05:00Z"),
            {"decided_at": "2028-02-29T12:05:00Z"},
            id="leap day kept",
        ),
        pytest.param(without("decided_by"), {"decided_by": None}, id="no decider"),
        pytest.param(
            complete_decision(decided_by="ops"), {"decided_by": None}, id="decider type"
        ),
        pytest.param(
            complete_decision(decided_by=["user-7", "ops@example.com"]),
            {"decided_by": None},
            id="decider list",
        ),
        pytest.param(
            complete_decision(decided_by={"id": "user-7"}),
            {"decided_by": None},
            id="decider without email",
        ),
        pytest.param(
            complete_decision(decided_by={"email": "ops@example.com"}),
            {"decided_by": None},
            id="decider without id",
        ),
        pytest.param(
            complete_decision(decided_by={"id": 7, "email": "ops@example.com"}),
            {"decided_by": None},
            id="decider id type",
        ),
    ],
)
def test_an_unreadable_detail_reads_as_absent(
    result: dict[str, object], expected: dict[str, object]
) -> None:
    decision = approval_decision(json.dumps(result))

    assert decision.approved is True
    assert decision.status == "approved"
    read = {
        "comment": decision.comment,
        "decided_by": decision.decided_by,
        "decided_at": decision.decided_at,
    }
    assert read == {
        "comment": "",
        "decided_by": DurableApprovalDecider(id="user-7", email="ops@example.com"),
        "decided_at": "2026-10-06T12:05:00Z",
        **expected,
    }
