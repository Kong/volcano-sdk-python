from __future__ import annotations

import base64
import json
from typing import TYPE_CHECKING

import pytest
from test_session_continuity import (
    SESSION_A,
    USER_A,
    USER_B,
    access_token,
    client_for,
    refreshed,
)

from volcano_sdk import AuthenticationError, Session

if TYPE_CHECKING:
    import httpx


@pytest.mark.parametrize(
    "payload",
    [
        b"null",
        b"[]",
        b'"claim"',
        b"1",
        b"true",
        b"{}",
        b'{"session_id": null}',
        b'{"session_id": 1}',
        b'{"session_id": " "}',
        b'{"session_id": "invalid"}',
        b"\xff",
        b"{",
    ],
)
def test_untrusted_claims_cannot_send_refresh_credentials(payload: bytes) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return refreshed(SESSION_A)

    client = client_for(handle)
    encoded = base64.urlsafe_b64encode(payload).decode().rstrip("=")
    adopted = client.auth.set_session(
        Session(f"header.{encoded}.signature", "supplied-refresh", USER_A)
    )

    with pytest.raises(AuthenticationError, match="without a session identifier"):
        _ = client.auth.refresh_session()

    assert not requests
    assert client.auth.get_session() is adopted


@pytest.mark.parametrize(
    "session_id", [SESSION_A.replace("-", ""), f"{{{SESSION_A}}}", f" {SESSION_A} "]
)
@pytest.mark.parametrize(
    "user_id",
    [
        "abcdef12-0000-4000-8000-000000000003",
        "ABCDEF12-0000-4000-8000-000000000003",
        "abcdef12000040008000000000000003",
        "{abcdef12-0000-4000-8000-000000000003}",
    ],
)
def test_refresh_accepts_equivalent_uuid_spellings(
    session_id: str, user_id: str
) -> None:
    requests: list[httpx.Request] = []
    canonical_user = "abcdef12-0000-4000-8000-000000000003"

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return refreshed(SESSION_A, canonical_user)

    client = client_for(handle)
    _ = client.auth.set_session(
        Session(access_token(session_id), "supplied-refresh", user_id)
    )

    session = client.auth.refresh_session()

    assert session.user_id == canonical_user
    assert session.access_token == access_token(SESSION_A, renewed=True)
    assert session.refresh_token == "rotated-refresh"
    assert client.auth.get_session() is session
    assert len(requests) == 1
    assert requests[0].url.path == "/auth/refresh"
    assert requests[0].headers["authorization"] == "Bearer anon"
    assert json.loads(requests[0].content) == {"refresh_token": "supplied-refresh"}


@pytest.mark.parametrize("user_id", [USER_A, "legacy-user"])
def test_same_server_session_cannot_replace_a_known_user(user_id: str) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return refreshed(SESSION_A, USER_B)

    client = client_for(handle)
    adopted = client.auth.set_session(
        Session(access_token(SESSION_A), "supplied-refresh", user_id)
    )

    with pytest.raises(AuthenticationError, match="different user"):
        _ = client.auth.refresh_session()

    assert len(requests) == 1
    assert client.auth.get_session() is adopted
