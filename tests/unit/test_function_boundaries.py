from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import pytest
from session_fixtures import access_token
from test_function_refresh import FUNCTION_ID, USER_ID, resolved_response

from volcano_sdk import Session, SessionChangedError, VolcanoClient
from volcano_sdk._transport import GeneratedTransport
from volcano_sdk.functions import _function_payload, _FunctionAuth, _header

if TYPE_CHECKING:
    from collections.abc import Callable


def key_client(handler: Callable[[httpx.Request], httpx.Response]) -> VolcanoClient:
    return VolcanoClient(
        anon_key="anon-key",
        _transport=GeneratedTransport(
            api_url="https://api.test.volcano.dev",
            httpx_transport=httpx.MockTransport(handler),
        ),
    )


@pytest.mark.parametrize(
    "payload",
    [None, [], "invalid", 1, {}, {"function_id": ""}, {"function_id": 1}],
)
def test_function_rejects_incomplete_resolution_before_dispatch(
    payload: object,
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=payload)

    client = key_client(handle)
    with pytest.raises(TypeError, match="Expected a complete function response"):
        client.functions.invoke("echo")
    assert [request.url.path for request in requests] == ["/functions/resolve"]


@pytest.mark.parametrize("stage", ["resolve", "invoke"])
def test_key_invocation_rejects_a_session_installed_during_the_request(
    stage: str,
) -> None:
    requests: list[httpx.Request] = []
    session = Session(access_token("new"), "new-refresh", USER_ID)

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        current = "resolve" if request.url.path == "/functions/resolve" else "invoke"
        if current == stage:
            client.auth.set_session(session)
        return (
            resolved_response()
            if current == "resolve"
            else httpx.Response(200, json={"ok": True})
        )

    client = key_client(handle)
    with pytest.raises(SessionChangedError):
        client.functions.invoke("echo")
    expected_paths = ["/functions/resolve"]
    if stage == "invoke":
        expected_paths.append(f"/functions/{FUNCTION_ID}/invoke")
    assert [request.url.path for request in requests] == expected_paths
    assert all(
        request.headers["authorization"] == "Bearer anon-key" for request in requests
    )
    assert client.current_session == session


def test_key_binding_rejects_a_session_installed_before_dispatch() -> None:
    client = VolcanoClient(anon_key="anon-key")
    auth = _FunctionAuth(client)
    session = Session(access_token("new"), "new-refresh", USER_ID)
    client.auth.set_session(session)
    tokens: list[str] = []

    with pytest.raises(SessionChangedError):
        auth.run(tokens.append)

    assert tokens == []
    assert client.current_session == session


@pytest.mark.parametrize("payload", [False, 1, [], "invalid"])
def test_function_payload_rejects_non_mappings(payload: object) -> None:
    with pytest.raises(TypeError, match="Function payload must be a mapping"):
        _function_payload(payload)


def test_function_header_without_a_header_mapping_is_absent() -> None:
    assert _header(None, "X-Volcano-Function-Invoked") is None
