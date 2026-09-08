from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from typing import TYPE_CHECKING

import httpx
import pytest

from volcano_sdk import AuthenticationError, Session, SessionChangedError, VolcanoClient
from volcano_sdk._transport import GeneratedTransport

if TYPE_CHECKING:
    from collections.abc import Callable


def make_client(handler: Callable[[httpx.Request], httpx.Response]) -> VolcanoClient:
    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handler),
    )
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.set_session(Session("old-access", "old-refresh", "user"))
    return client


def refreshed_response() -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "access_token": "new-access",
            "refresh_token": "new-refresh",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": {
                "id": "00000000-0000-4000-8000-000000000001",
                "email": "user@example.com",
                "status": "active",
            },
        },
    )


def rows_response() -> httpx.Response:
    return httpx.Response(200, json={"data": [{"id": 1}], "count": 1})


def test_select_refreshes_once_and_replays_the_same_query() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            return refreshed_response()
        if request.headers["authorization"] == "Bearer old-access":
            return httpx.Response(401, json={"error": "expired"})
        return rows_response()

    client = make_client(handle)
    query = client.database("db").from_("items").select("id").eq("id", 1).limit(2)

    assert query.execute() == [{"id": 1}]
    assert [request.headers["authorization"] for request in requests] == [
        "Bearer old-access",
        "Bearer anon",
        "Bearer new-access",
    ]
    assert requests[0].content == requests[2].content
    assert json.loads(requests[1].content)["refresh_token"] == "old-refresh"


def test_second_401_is_returned_without_another_refresh() -> None:
    paths: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.path)
        if request.url.path == "/auth/refresh":
            return refreshed_response()
        return httpx.Response(401, json={"error": "denied"})

    client = make_client(handle)
    with pytest.raises(AuthenticationError, match="denied"):
        client.database("db").from_("items").execute()
    assert len(paths) == 3
    assert paths.count("/auth/refresh") == 1


@pytest.mark.parametrize("refresh_status", [401, 503])
def test_failed_refresh_preserves_original_read_error(refresh_status: int) -> None:
    paths: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.path)
        if request.url.path == "/auth/refresh":
            return httpx.Response(refresh_status, json={"error": "refresh failed"})
        return httpx.Response(401, json={"error": "read expired", "code": "expired"})

    client = make_client(handle)
    with pytest.raises(AuthenticationError, match="read expired") as caught:
        client.database("db").from_("items").execute()
    assert caught.value.code == "expired"
    assert len(paths) == 2
    assert (client.current_session is None) == (refresh_status == 401)


@pytest.mark.parametrize("replace_at", ["read", "refresh", "listener"])
def test_read_never_retries_under_a_replacement_session(replace_at: str) -> None:
    paths: list[str] = []
    replacement = Session("replacement", "replacement-refresh", "other-user")

    def handle(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.path)
        stage = "refresh" if request.url.path == "/auth/refresh" else "read"
        if stage == replace_at:
            client.auth.set_session(replacement)
        return (
            refreshed_response()
            if stage == "refresh"
            else httpx.Response(401, json={"error": "expired"})
        )

    client = make_client(handle)
    if replace_at == "listener":

        def replace_on_refresh(event: str, _session: Session | None) -> None:
            if event == "TOKEN_REFRESHED":
                client.auth.set_session(replacement)

        client.auth.on_auth_state_change(replace_on_refresh)
    with pytest.raises(SessionChangedError):
        client.database("db").from_("items").execute()
    assert client.current_session == replacement
    assert len(paths) == (1 if replace_at == "read" else 2)


def test_concurrent_reads_share_refresh_for_the_captured_session() -> None:
    initial_reads = Barrier(2, timeout=5)
    refresh_requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/auth/refresh":
            refresh_requests.append(request)
            return refreshed_response()
        if request.headers["authorization"] == "Bearer old-access":
            initial_reads.wait()
            return httpx.Response(401, json={"error": "expired"})
        return rows_response()

    client = make_client(handle)
    query = client.database("db").from_("items")
    with ThreadPoolExecutor(max_workers=2) as pool:
        reads = [pool.submit(query.execute) for _ in range(2)]
        results = [read.result(timeout=5) for read in reads]
    assert results == [[{"id": 1}], [{"id": 1}]]
    assert len(refresh_requests) == 1


@pytest.mark.parametrize("operation", ["select", "insert", "update", "delete"])
def test_only_select_401_is_eligible_for_refresh(operation: str) -> None:
    paths: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.path)
        return httpx.Response(
            403 if operation == "select" else 401, json={"error": "denied"}
        )

    client = make_client(handle)
    table = client.database("db").from_("items")
    queries = {
        "select": table.execute,
        "insert": table.insert({"id": 1}).execute,
        "update": table.update({"id": 1}).execute,
        "delete": table.delete().execute,
    }
    with pytest.raises(AuthenticationError):
        queries[operation]()
    assert len(paths) == 1
