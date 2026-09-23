from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING
from uuid import UUID

import httpx
import pytest
from transport_fixtures import RejectingTransport

from volcano_sdk import LockLease, VolcanoClient, VolcanoError
from volcano_sdk import _lock_guard as guard_module
from volcano_sdk import locks as locks_module
from volcano_sdk._lock_guard import LockGuard
from volcano_sdk._transport import GeneratedTransport
from volcano_sdk.locks import _lock_values

if TYPE_CHECKING:
    from collections.abc import Callable

OWNER_TOKEN = "ABCDEFAB-1234-4567-89AB-ABCDEFABCDEF"
REQUEST_ID = "BBCDEFAB-1234-4567-89AB-ABCDEFABCDEF"
LEASE = {"expires_at": "2026-09-18T18:00:00Z", "fencing_token": 7}


def make_client(handler: Callable[[httpx.Request], httpx.Response]) -> VolcanoClient:
    return VolcanoClient(
        anon_key="anon",
        service_key="service",
        _transport=GeneratedTransport(
            api_url="https://api.test.volcano.dev",
            httpx_transport=httpx.MockTransport(handler),
        ),
    )


def test_optional_lock_operations_require_transport_capabilities() -> None:
    client = VolcanoClient(
        anon_key="anon", service_key="service", _transport=RejectingTransport()
    )
    lease = LockLease(key="build", token=OWNER_TOKEN, expires_at=None, fencing_token=7)

    with pytest.raises(TypeError, match="requested lock operation"):
        client.locks.get("build")
    with pytest.raises(TypeError, match="requested lock operation"):
        client.locks.renew("build", lease, ttl=30)
    with pytest.raises(TypeError, match="requested lock operation"):
        client.locks.force_release("build")


def failed_acquisition_response(request: httpx.Request, failure: str) -> httpx.Response:
    if failure == "transport":
        message = "response lost after acquiring"
        raise httpx.ReadError(message, request=request)
    bodies = {"empty": b"", "html": b"<h1>Unavailable</h1>", "malformed": b"{"}
    if failure in bodies:
        return httpx.Response(503, content=bodies[failure])
    return httpx.Response(503, json={"error": "acquire outcome unknown"})


def lease_response(request: httpx.Request) -> httpx.Response:
    if request.method == "DELETE":
        return httpx.Response(204)
    return httpx.Response(201 if request.method == "POST" else 200, json=LEASE)


def test_preparing_a_closed_guard_preserves_lost_ownership(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "lease_now", lambda: 100.0)
    monkeypatch.setattr(locks_module, "lease_now", lambda: 100.0)
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return lease_response(request)

    client = make_client(handle)
    original = client.locks.acquire("build", ttl=30)
    guard = LockGuard(original, ttl=30, started_at=100.0)
    guard._close()

    with pytest.raises(
        RuntimeError, match="lock guard rejected renewal without a failure"
    ):
        client.locks._prepare_guard("build", guard, ttl=30)

    assert guard.lost
    assert guard.lease is original
    assert [request.method for request in requests] == ["POST", "PATCH"]
    assert requests[1].headers["x-volcano-lock-token"] == original.token
    assert requests[0].url.path == requests[1].url.path


@pytest.mark.parametrize("failure", ["transport", "503", "empty", "html", "malformed"])
@pytest.mark.parametrize("supplied", [False, True])
def test_acquire_retries_once_with_the_same_owner_and_request(
    failure: str, *, supplied: bool
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if len(requests) == 1:
            return failed_acquisition_response(request, failure)
        return httpx.Response(201, json=LEASE)

    client = make_client(handle)
    options = {"token": OWNER_TOKEN, "request_id": REQUEST_ID} if supplied else {}
    lease = client.locks.acquire("build", ttl=30, **options)
    assert len(requests) == 2
    assert requests[0].headers == requests[1].headers
    assert requests[0].content == requests[1].content
    assert requests[0].url == requests[1].url
    assert requests[0].headers["authorization"] == "Bearer service"
    assert str(UUID(requests[0].headers["x-volcano-request-id"]))
    assert lease.token == requests[0].headers["x-volcano-lock-token"]
    assert lease.fencing_token == 7
    if supplied:
        assert lease.token == OWNER_TOKEN
        assert requests[0].headers["x-volcano-request-id"] == REQUEST_ID


@pytest.mark.parametrize(
    ("status", "attempts"),
    [(400, 1), (401, 1), (403, 1), (409, 1), (429, 1), (500, 1), (503, 2)],
)
def test_acquire_bounds_retries_and_preserves_failure(
    status: int, attempts: int
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            status, json={"error": "acquire rejected", "code": "lock_failure"}
        )

    with pytest.raises(VolcanoError) as caught:
        make_client(handle).locks.acquire(
            "build", ttl=30, token=OWNER_TOKEN, request_id=REQUEST_ID
        )
    assert caught.value.status == status
    assert caught.value.code == "lock_failure"
    assert len(requests) == attempts
    assert all(r.headers["x-volcano-lock-token"] == OWNER_TOKEN for r in requests)
    assert OWNER_TOKEN not in str(caught.value)


def test_acquire_stops_after_two_transport_failures() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        message = "response lost"
        raise httpx.ReadError(message, request=request)

    with pytest.raises(VolcanoError):
        make_client(handle).locks.acquire(
            "build", ttl=30, token=OWNER_TOKEN, request_id=REQUEST_ID
        )
    assert len(requests) == 2
    assert requests[0].headers == requests[1].headers


@pytest.mark.parametrize("name", ["token", "request_id"])
@pytest.mark.parametrize("value", ["", "not-a-uuid"])
def test_acquire_rejects_invalid_identifiers_before_a_request(
    name: str, value: str
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(201, json=LEASE)

    with pytest.raises(ValueError, match=f"^{name} must be a UUID string$"):
        make_client(handle).locks.acquire("build", ttl=30, **{name: value})
    assert not requests


@pytest.mark.parametrize(
    "operation", ["get", "acquire", "renew", "release", "force_release"]
)
def test_every_lock_operation_names_an_invalid_request_identifier(
    operation: str,
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return lease_response(request)

    client = make_client(handle)
    lease = LockLease(key="build", token=OWNER_TOKEN, expires_at=None, fencing_token=7)
    operations: dict[str, Callable[[], object]] = {
        "get": lambda: client.locks.get("build", request_id="invalid"),
        "acquire": lambda: client.locks.acquire("build", ttl=30, request_id="invalid"),
        "renew": lambda: client.locks.renew(
            "build", lease, ttl=30, request_id="invalid"
        ),
        "release": lambda: client.locks.release("build", lease, request_id="invalid"),
        "force_release": lambda: client.locks.force_release(
            "build", request_id="invalid"
        ),
    }

    with pytest.raises(ValueError, match="request_id must be a UUID string"):
        _ = operations[operation]()
    assert requests == []


@pytest.mark.parametrize("ttl", [5, 7_776_000])
def test_acquire_accepts_both_ttl_boundaries(ttl: int) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(201, json=LEASE)

    _ = make_client(handle).locks.acquire("build", ttl=ttl)

    assert len(requests) == 1
    assert json.loads(requests[0].content)["ttl_seconds"] == ttl


def test_each_lock_operation_forwards_the_supplied_request_id() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "GET":
            return httpx.Response(200, json={"held": True, **LEASE})
        if request.method == "PATCH":
            return httpx.Response(200, json=LEASE)
        return httpx.Response(204)

    client = make_client(handle)
    lease = LockLease(
        key="build", token=OWNER_TOKEN, expires_at=None, fencing_token=None
    )
    assert client.locks.get("build", request_id=REQUEST_ID).held
    renewed = client.locks.renew("build", lease, ttl=30, request_id=REQUEST_ID)
    client.locks.release("build", renewed, request_id=REQUEST_ID)
    client.locks.force_release("build", request_id=REQUEST_ID)
    assert [r.method for r in requests] == ["GET", "PATCH", "DELETE", "DELETE"]
    assert all(r.headers["x-volcano-request-id"] == REQUEST_ID for r in requests)
    assert json.loads(requests[1].content) == {"ttl_seconds": 30}


@pytest.mark.parametrize("operation", ["release", "force_release"])
def test_release_operations_reject_a_non_no_content_response(operation: str) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"error": "lock remained held"})

    client = make_client(handle)
    lease = LockLease(key="build", token=OWNER_TOKEN, expires_at=None, fencing_token=7)
    operations: dict[str, Callable[[], None]] = {
        "release": lambda: client.locks.release("build", lease),
        "force_release": lambda: client.locks.force_release("build"),
    }

    with pytest.raises(VolcanoError, match="lock remained held"):
        operations[operation]()
    assert len(requests) == 1


def test_lock_response_rejects_a_non_object_payload() -> None:
    with pytest.raises(TypeError, match="Expected a complete lock response"):
        _lock_values([])


@pytest.mark.parametrize(
    "payload",
    [{"held": "yes"}, {"held": True, "fencing_token": "seven"}],
)
def test_get_rejects_invalid_lock_response_fields(payload: object) -> None:
    def handle(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    with pytest.raises(TypeError, match="Expected a complete lock response"):
        make_client(handle).locks.get("build")


@pytest.mark.parametrize("value", [None, "seven", True])
def test_acquisition_rejects_invalid_fencing_tokens(value: object) -> None:
    def handle(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            201,
            json={"expires_at": "2026-09-18T18:00:00Z", "fencing_token": value},
        )

    with pytest.raises(TypeError, match="Expected a complete lock response"):
        make_client(handle).locks.acquire("build", ttl=30)


def test_renew_rejects_a_non_integer_fencing_token() -> None:
    def handle(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"expires_at": "2026-09-18T18:00:00Z", "fencing_token": "seven"},
        )

    lease = LockLease(key="build", token=OWNER_TOKEN, expires_at=None, fencing_token=7)
    with pytest.raises(TypeError, match="Expected a complete lock response"):
        make_client(handle).locks.renew("build", lease, ttl=30)


def test_acquire_keeps_the_original_service_credential_on_retry() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if len(requests) == 1:
            client._service_key = "replacement"
            return httpx.Response(503, json={"error": "outcome unknown"})
        return httpx.Response(201, json=LEASE)

    client = make_client(handle)
    client.locks.acquire("build", ttl=30)
    assert [r.headers["authorization"] for r in requests] == ["Bearer service"] * 2


def test_with_lock_forwards_acquisition_ids_but_release_gets_a_new_request_id() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "POST":
            return httpx.Response(
                201,
                json={
                    "expires_at": (
                        datetime.now(UTC) + timedelta(seconds=30)
                    ).isoformat(),
                    "fencing_token": 7,
                },
            )
        return httpx.Response(204)

    client = make_client(handle)
    with client.locks.with_lock(
        "build", ttl=30, token=OWNER_TOKEN, request_id=REQUEST_ID
    ) as guard:
        assert guard.lease.token == OWNER_TOKEN
    assert [r.method for r in requests] == ["POST", "DELETE"]
    assert requests[0].headers["x-volcano-request-id"] == REQUEST_ID
    assert requests[1].headers["x-volcano-request-id"] != REQUEST_ID
    assert requests[1].headers["x-volcano-lock-token"] == OWNER_TOKEN


@pytest.mark.parametrize("retry_duration", [1.0, 31.0])
def test_guard_uses_successful_attempt_start_without_extending_a_slow_retry(
    monkeypatch: pytest.MonkeyPatch, retry_duration: float
) -> None:
    clock = [100.0]
    monkeypatch.setattr(locks_module, "lease_now", lambda: clock[0])
    monkeypatch.setattr(guard_module, "lease_now", lambda: clock[0])
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if len(requests) == 1:
            clock[0] += 40
            message = "first response stalled past the TTL"
            raise httpx.ReadError(message, request=request)
        if request.method == "POST":
            clock[0] += retry_duration
        return lease_response(request)

    client = make_client(handle)
    if retry_duration > 30:
        with pytest.raises(TimeoutError), client.locks.with_lock("build", ttl=30):
            pytest.fail("an expired retry must not enter the critical section")
    else:
        with client.locks.with_lock("build", ttl=30) as guard:
            assert not guard.lost
            assert guard._remaining_seconds() == 29
        assert [request.method for request in requests] == ["POST", "POST", "DELETE"]


def test_guard_uses_attempt_start_for_a_first_try_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = iter((100.0, 101.0))
    monkeypatch.setattr(locks_module, "lease_now", lambda: next(clock))
    monkeypatch.setattr(guard_module, "lease_now", lambda: 101.0)

    with make_client(lease_response).locks.with_lock("build", ttl=30) as guard:
        assert guard._remaining_seconds() == pytest.approx(30.0)


def test_with_lock_preserves_renewal_failure_when_release_fails() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "POST":
            return httpx.Response(201, json=LEASE)
        return httpx.Response(500, json={"error": "release failed"})

    client = make_client(handle)
    failure = RuntimeError("ownership lost")
    with (
        pytest.raises(RuntimeError, match="ownership lost"),
        client.locks.with_lock("build", ttl=30) as guard,
    ):
        guard.mark_lost(failure)

    assert [request.method for request in requests] == ["POST", "DELETE"]
    assert requests[0].url.path == requests[1].url.path


def test_with_lock_surfaces_release_failure_after_a_successful_body() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "POST":
            return httpx.Response(201, json=LEASE)
        return httpx.Response(500, json={"error": "release failed"})

    with (
        pytest.raises(VolcanoError, match="release failed"),
        make_client(handle).locks.with_lock("build", ttl=30),
    ):
        pass

    assert [request.method for request in requests] == ["POST", "DELETE"]
    assert requests[0].url.path == requests[1].url.path


@pytest.mark.parametrize("body", [b"", b"<h1>Unavailable</h1>", b"{"])
def test_repeated_unparseable_503_preserves_status_and_retry_bound(body: bytes) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(503, content=body)

    with pytest.raises(VolcanoError) as caught:
        make_client(handle).locks.acquire("build", ttl=30)
    assert caught.value.status == 503
    assert len(requests) == 2
    assert requests[0].headers == requests[1].headers
