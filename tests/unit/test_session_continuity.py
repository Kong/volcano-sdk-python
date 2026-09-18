from __future__ import annotations

import base64
import json
from typing import TYPE_CHECKING

import httpx
import pytest

from volcano_sdk import AuthenticationError, Session, SessionChangedError, VolcanoClient
from volcano_sdk._transport import GeneratedTransport

if TYPE_CHECKING:
    from collections.abc import Callable

SESSION_A = "00000000-0000-4000-8000-000000000001"
SESSION_B = "00000000-0000-4000-8000-000000000002"
USER_A = "00000000-0000-4000-8000-000000000003"
USER_B = "00000000-0000-4000-8000-000000000004"


def access_token(session_id: str, *, renewed: bool = False) -> str:
    payload = (
        base64.urlsafe_b64encode(
            json.dumps({"session_id": session_id, "renewed": renewed}).encode()
        )
        .decode()
        .rstrip("=")
    )
    return f"header.{payload}.signature"


def refreshed(session_id: str, user_id: str = USER_A) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "access_token": access_token(session_id, renewed=True),
            "refresh_token": "rotated-refresh",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": {"id": user_id, "email": "u@example.com", "status": "active"},
        },
    )


def client_for(handler: Callable[[httpx.Request], httpx.Response]) -> VolcanoClient:
    return VolcanoClient(
        anon_key="anon",
        access_token=access_token(SESSION_A),
        refresh_token="supplied-refresh",
        _transport=GeneratedTransport(
            api_url="https://api.test.volcano.dev",
            httpx_transport=httpx.MockTransport(handler),
        ),
    )


@pytest.mark.parametrize("user_id", [USER_A, USER_B])
@pytest.mark.parametrize("profile_first", [False, True])
def test_refresh_cannot_replay_a_bootstrap_mutation_in_another_server_session(
    user_id: str, *, profile_first: bool
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/user":
            return httpx.Response(
                200,
                json={
                    "user": {"id": USER_A, "email": "u@example.com", "status": "active"}
                },
            )
        if request.url.path == "/auth/refresh":
            return refreshed(SESSION_B, user_id)
        assert (
            request.headers["authorization"] == f"Bearer {access_token(SESSION_A)}"
        ), "mutation replayed in a different session"
        return httpx.Response(401, json={"error": "expired"})

    client = client_for(handle)
    if profile_first:
        client.auth.get_user()
    with pytest.raises(AuthenticationError):
        client.database("main").from_("items").insert({"name": "example"}).execute()
    assert client.current_session is not None
    assert client.current_session.access_token == access_token(SESSION_A)
    assert len([r for r in requests if r.url.path != "/auth/user"]) == 2


def test_unidentified_bootstrap_cannot_refresh_without_a_continuity_identifier() -> (
    None
):
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return refreshed(SESSION_B)

    client = VolcanoClient(
        anon_key="anon",
        access_token="malformed",
        refresh_token="supplied-refresh",
        _transport=GeneratedTransport(
            api_url="https://api.test.volcano.dev",
            httpx_transport=httpx.MockTransport(handle),
        ),
    )
    with pytest.raises(AuthenticationError, match="session identifier"):
        client.auth.refresh_session()
    assert not requests


@pytest.mark.parametrize("replace", [False, True])
def test_sign_out_renews_expired_access_only_for_the_same_captured_session(
    *, replace: bool
) -> None:
    requests: list[httpx.Request] = []
    replacement = Session("replacement", "replacement-refresh", USER_B)

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            if replace:
                client.auth.set_session(replacement)
            return refreshed(SESSION_A)
        assert request.url.path == f"/auth/user/sessions/{SESSION_A}"
        if request.headers["authorization"] == f"Bearer {access_token(SESSION_A)}":
            return httpx.Response(401, json={"error": "expired"})
        assert (
            request.headers["authorization"]
            == f"Bearer {access_token(SESSION_A, renewed=True)}"
        )
        return httpx.Response(204)

    client = client_for(handle)
    if replace:
        with pytest.raises(SessionChangedError):
            client.auth.sign_out()
    else:
        client.auth.sign_out()
    assert [r.method for r in requests] == ["DELETE", "POST", "DELETE"]
    assert client.current_session == (replacement if replace else None)


def test_sign_out_clears_a_refresh_of_the_same_server_session() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            return refreshed(SESSION_A)
        client.auth.refresh_session()
        return httpx.Response(204)

    client = client_for(handle)
    client.auth.sign_out()
    assert client.current_session is None
    assert [r.method for r in requests] == ["DELETE", "POST"]


@pytest.mark.parametrize("token", ["a.é.c", "a.☃.c", "a.!!!!.c"])
def test_sign_out_clears_malformed_bootstrap_tokens(token: str) -> None:
    client = VolcanoClient(anon_key="anon", access_token=token)
    client.auth.sign_out()
    assert client.current_session is None


@pytest.mark.parametrize("user_id", [USER_A, USER_B])
def test_expired_sign_out_never_revokes_a_mismatched_refresh_session(
    user_id: str,
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            return refreshed(SESSION_B, user_id)
        assert len(requests) == 1, "revoked a different refreshed session"
        return httpx.Response(401, json={"error": "expired"})

    client = client_for(handle)
    with pytest.raises(AuthenticationError, match="different server session"):
        client.auth.sign_out()
    assert client.current_session is None
    assert [r.method for r in requests] == ["DELETE", "POST"]
