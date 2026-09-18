from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING
from uuid import UUID

import httpx
import pytest

from volcano_sdk import LockLease, VolcanoClient, VolcanoError
from volcano_sdk._transport import GeneratedTransport

if TYPE_CHECKING:
    from collections.abc import Callable

OWNER_TOKEN = "00000000-0000-4000-8000-000000000001"
REQUEST_ID = "00000000-0000-4000-8000-000000000002"
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


@pytest.mark.parametrize("failure", ["transport", "503"])
@pytest.mark.parametrize("supplied", [False, True])
def test_acquire_retries_once_with_the_same_owner_and_request(
    failure: str, *, supplied: bool
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if len(requests) == 1:
            if failure == "transport":
                message = "response lost after acquiring"
                raise httpx.ReadError(message, request=request)
            return httpx.Response(503, json={"error": "acquire outcome unknown"})
        return httpx.Response(201, json=LEASE)

    client = make_client(handle)
    options = {"token": OWNER_TOKEN, "request_id": REQUEST_ID} if supplied else {}
    lease = client.locks.acquire("build", ttl=30, **options)
    assert len(requests) == 2
    assert requests[0].headers == requests[1].headers
    assert requests[0].content == requests[1].content
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

    with pytest.raises(ValueError, match=name):
        make_client(handle).locks.acquire("build", ttl=30, **{name: value})
    assert not requests


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
