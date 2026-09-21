from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from typing import TYPE_CHECKING

import httpx
import pytest
from session_fixtures import access_token

from volcano_sdk import (
    AuthenticationError,
    Session,
    SessionChangedError,
    TransportError,
    VolcanoClient,
    VolcanoError,
)
from volcano_sdk._transport import GeneratedTransport

if TYPE_CHECKING:
    from collections.abc import Callable
    from concurrent.futures import Future

    from volcano_sdk.models import FunctionResponse, JSONValue

USER_ID = "00000000-0000-4000-8000-000000000001"
FUNCTION_ID = "00000000-0000-4000-8000-000000000040"


def make_client(handler: Callable[[httpx.Request], httpx.Response]) -> VolcanoClient:
    client = VolcanoClient(
        anon_key="anon",
        _transport=GeneratedTransport(
            api_url="https://api.test.volcano.dev",
            httpx_transport=httpx.MockTransport(handler),
        ),
    )
    client.auth.set_session(Session(access_token("old"), "old-refresh", USER_ID))
    return client


def refreshed_response() -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "access_token": access_token("new"),
            "refresh_token": "new-refresh",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": {"id": USER_ID, "email": "user@example.com", "status": "active"},
        },
    )


def resolved_response(invoke_url: str | None = None) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "name": "echo",
            "function_id": FUNCTION_ID,
            "cache_ttl_seconds": 60,
            "invoke_url": invoke_url,
        },
    )


@pytest.mark.parametrize("rejected_stage", ["resolve", "invoke"])
@pytest.mark.parametrize(
    "resolved_url", [None, "https://echo.functions.test.volcano.dev/invoke"]
)
def test_function_refreshes_rejected_stage_and_preserves_payload(
    rejected_stage: str,
    resolved_url: str | None,
) -> None:
    requests: list[httpx.Request] = []
    values: list[JSONValue] = ["original"]
    payload: dict[str, JSONValue] = {"values": values}

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            values.append("changed")
            return refreshed_response()
        stage = "resolve" if request.url.path == "/functions/resolve" else "invoke"
        if (
            stage == rejected_stage
            and request.headers["authorization"] == f"Bearer {access_token('old')}"
        ):
            return httpx.Response(401, json={"error": "expired", "code": "expired"})
        return (
            resolved_response(resolved_url)
            if stage == "resolve"
            else httpx.Response(200, json={"ok": True})
        )

    client = make_client(handle)
    assert client.functions.invoke("echo", payload).data == {"ok": True}
    assert sum(request.url.path == "/auth/refresh" for request in requests) == 1
    invokes = [request for request in requests if request.url.path.endswith("/invoke")]
    assert all(
        json.loads(request.content) == {"payload": {"values": ["original"]}}
        for request in invokes
    )
    assert invokes[-1].headers["authorization"] == f"Bearer {access_token('new')}"
    assert client.current_session is not None
    assert client.current_session.access_token == access_token("new")


@pytest.mark.parametrize("status", [401, 403])
def test_function_owned_authentication_error_never_replays(status: int) -> None:
    requests: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request.url.path)
        if request.url.path == "/functions/resolve":
            return resolved_response()
        return httpx.Response(
            status,
            json={"error": "application response"},
            headers={"X-Volcano-Function-Invoked": "true"},
        )

    result = make_client(handle).functions.invoke("echo")
    assert result.status == status
    assert requests == ["/functions/resolve", f"/functions/{FUNCTION_ID}/invoke"]


@pytest.mark.parametrize("stage", ["resolve", "invoke"])
def test_function_rejects_replacement_session_before_return_or_dispatch(
    stage: str,
) -> None:
    invokes: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        current = "resolve" if request.url.path == "/functions/resolve" else "invoke"
        if current == stage:
            client.auth.set_session(
                Session(access_token("replacement"), "replacement-refresh", USER_ID)
            )
        if current == "invoke":
            invokes.append(request.headers["authorization"])
            return httpx.Response(200, json={"ok": True})
        return resolved_response()

    client = make_client(handle)
    with pytest.raises(SessionChangedError):
        client.functions.invoke("echo")
    assert len(invokes) == (0 if stage == "resolve" else 1)
    assert client.current_session is not None
    assert client.current_session.refresh_token == "replacement-refresh"


@pytest.mark.parametrize("refresh_status", [200, 401, 503])
def test_function_bounds_retry_and_preserves_original_rejection(
    refresh_status: int,
) -> None:
    requests: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request.url.path)
        if request.url.path == "/auth/refresh":
            return (
                refreshed_response()
                if refresh_status == 200
                else httpx.Response(refresh_status, json={"error": "refresh failed"})
            )
        return httpx.Response(
            401, json={"error": "original denial", "code": "original"}
        )

    with pytest.raises(AuthenticationError, match="original denial") as failure:
        make_client(handle).functions.invoke("echo")
    assert failure.value.status == 401
    assert failure.value.code == "original"
    assert requests.count("/auth/refresh") == 1
    assert requests.count("/functions/resolve") == (2 if refresh_status == 200 else 1)


@pytest.mark.parametrize("rejected_stage", ["resolve", "invoke"])
def test_function_refreshes_a_malformed_platform_401(rejected_stage: str) -> None:
    calls: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        if request.url.path == "/auth/refresh":
            return refreshed_response()
        stage = "resolve" if request.url.path == "/functions/resolve" else "invoke"
        if (
            stage == rejected_stage
            and request.headers["authorization"] == f"Bearer {access_token('old')}"
        ):
            return httpx.Response(401, text="not JSON")
        return (
            resolved_response()
            if stage == "resolve"
            else httpx.Response(200, json={"ok": True})
        )

    assert make_client(handle).functions.invoke("echo").data == {"ok": True}
    assert calls.count("/auth/refresh") == 1


@pytest.mark.parametrize("stage", ["resolve", "invoke"])
@pytest.mark.parametrize("failure", ["forbidden", "network"])
def test_function_never_replays_forbidden_or_uncertain_requests(
    stage: str, failure: str
) -> None:
    paths: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.path)
        current = "resolve" if request.url.path == "/functions/resolve" else "invoke"
        if current == stage:
            if failure == "network":
                message = "connection lost"
                raise httpx.ReadError(message)
            return httpx.Response(403, json={"error": "forbidden"})
        return resolved_response()

    with pytest.raises(TransportError if failure == "network" else VolcanoError):
        make_client(handle).functions.invoke("echo")
    assert len(paths) == (1 if stage == "resolve" else 2)
    assert "/auth/refresh" not in paths


@pytest.mark.parametrize("key", ["anon", "service"])
def test_function_does_not_refresh_key_credentials(key: str) -> None:
    paths: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.path)
        assert request.headers["authorization"] == f"Bearer {key}"
        return httpx.Response(401, json={"error": "invalid key"})

    client = VolcanoClient(
        anon_key="anon",
        service_key=key if key == "service" else None,
        _transport=GeneratedTransport(
            api_url="https://api.test.volcano.dev",
            httpx_transport=httpx.MockTransport(handle),
        ),
    )
    with pytest.raises(AuthenticationError, match="invalid key"):
        client.functions.invoke("echo")
    assert paths == ["/functions/resolve"]


def replace_session_on_refresh(
    client: VolcanoClient, replacement: Session
) -> Callable[[str, Session | None], None]:
    def listener(event: str, _session: Session | None) -> None:
        if event == "TOKEN_REFRESHED":
            client.auth.set_session(replacement)

    return listener


def assert_invocation_outcome(
    call: Future[FunctionResponse], refresh_status: int
) -> None:
    if refresh_status == 200:
        assert call.result(timeout=5).data == {"ok": True}
        return
    with pytest.raises(AuthenticationError, match="invocation rejected"):
        call.result(timeout=5)


def refresh_invocation_response(
    request: httpx.Request, refreshes: list[str]
) -> httpx.Response:
    refreshes.append(request.url.path)
    result = refreshed_response().json()
    result["access_token"] = access_token(f"renewed-{len(refreshes)}")
    result["refresh_token"] = f"refresh-{len(refreshes)}"
    return httpx.Response(200, json=result)


@pytest.mark.parametrize("replace_at", ["refresh", "listener"])
def test_function_does_not_dispatch_after_refresh_replaces_session(
    replace_at: str,
) -> None:
    paths: list[str] = []
    replacement = Session(access_token("replacement"), "replacement-refresh", USER_ID)

    def handle(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.path)
        if request.url.path == "/auth/refresh":
            if replace_at == "refresh":
                client.auth.set_session(replacement)
            return refreshed_response()
        return httpx.Response(401, json={"error": "expired"})

    client = make_client(handle)
    if replace_at == "listener":
        client.auth.on_auth_state_change(
            replace_session_on_refresh(client, replacement)
        )
    with pytest.raises(SessionChangedError):
        client.functions.invoke("echo")
    assert paths == ["/functions/resolve", "/auth/refresh"]
    assert client.current_session == replacement


@pytest.mark.parametrize("refresh_status", [200, 401])
def test_concurrent_function_invocations_share_refresh(refresh_status: int) -> None:
    initial_calls = Barrier(2, timeout=5)
    refreshes: list[httpx.Request] = []

    client = make_client(
        concurrent_invocation_handler(initial_calls, refreshes, refresh_status)
    )
    with ThreadPoolExecutor(max_workers=2) as pool:
        calls = [pool.submit(client.functions.invoke, "echo") for _ in range(2)]
        for call in calls:
            assert_invocation_outcome(call, refresh_status)
    assert len(refreshes) == 1


def test_function_refreshes_the_token_captured_at_each_rejected_stage() -> None:
    refreshes: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/auth/refresh":
            return refresh_invocation_response(request, refreshes)
        return invocation_stage_response(request)

    assert make_client(handle).functions.invoke("echo").data == {"ok": True}
    assert len(refreshes) == 2


def invocation_stage_response(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/functions/resolve":
        if request.headers["authorization"] != f"Bearer {access_token('old')}":
            return resolved_response()
    elif request.headers["authorization"] == f"Bearer {access_token('renewed-2')}":
        return httpx.Response(200, json={"ok": True})
    return httpx.Response(401, json={"error": "stage expired"})


def refresh_outcome_response(status: int) -> httpx.Response:
    if status == 200:
        return refreshed_response()
    return httpx.Response(401, json={"error": "refresh rejected"})


def concurrent_invocation_handler(
    initial_calls: Barrier, refreshes: list[httpx.Request], refresh_status: int
) -> Callable[[httpx.Request], httpx.Response]:
    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/auth/refresh":
            refreshes.append(request)
            return refresh_outcome_response(refresh_status)
        if request.url.path == "/functions/resolve":
            return resolved_response()
        if request.headers["authorization"] == f"Bearer {access_token('old')}":
            initial_calls.wait()
            return httpx.Response(401, json={"error": "invocation rejected"})
        return httpx.Response(200, json={"ok": True})

    return handle
