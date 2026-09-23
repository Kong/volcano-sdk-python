from __future__ import annotations

import base64
import json
from typing import TYPE_CHECKING

import httpx
import pytest

from volcano_sdk import (
    AuthenticationError,
    Session,
    SessionChangedError,
    VolcanoClient,
    VolcanoError,
)
from volcano_sdk._transport import GeneratedTransport

if TYPE_CHECKING:
    from collections.abc import Callable

USER_ID = "00000000-0000-4000-8000-000000000001"
SUPPLIED_ACCESS = "supplied-access"
PROFILE = {"id": USER_ID, "email": "user@example.com", "status": "active"}


def bootstrap_token(*, renewed: bool = False) -> str:
    payload = base64.urlsafe_b64encode(
        json.dumps(
            {"session_id": "00000000-0000-4000-8000-000000000012", "renewed": renewed}
        ).encode()
    ).decode()
    return f"header.{payload}.signature"


def token_client(
    handler: Callable[[httpx.Request], httpx.Response],
    *,
    refresh_token: str | None = None,
    access_token: str = SUPPLIED_ACCESS,
) -> VolcanoClient:
    return VolcanoClient(
        anon_key="anon",
        access_token=access_token,
        refresh_token=refresh_token,
        _transport=GeneratedTransport(
            api_url="https://api.test.volcano.dev",
            httpx_transport=httpx.MockTransport(handler),
        ),
    )


def test_token_bootstrap_is_local_until_profile_validation() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"user": PROFILE})

    client = token_client(handle)
    initial = client.auth.get_session()
    assert initial is not None
    assert initial.access_token == "supplied-access"
    assert initial.refresh_token is None
    assert initial.user_id is None
    assert initial.user is None
    assert not requests
    assert client.auth.get_user().id == USER_ID
    current = client.current_session
    assert current is not None
    assert current.user_id == USER_ID
    assert current.user == PROFILE
    assert current.access_token == initial.access_token
    assert current.refresh_token is None
    assert initial.user_id is None
    assert requests[0].headers["authorization"] == "Bearer supplied-access"


def test_token_bootstrap_retains_an_invalid_token_until_local_sign_out() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(401, json={"error": "expired supplied token"})

    client = token_client(handle)
    initial = client.current_session
    with pytest.raises(AuthenticationError, match="expired supplied token"):
        _ = client.auth.get_user()
    with pytest.raises(AuthenticationError, match="No refresh token"):
        _ = client.auth.refresh_session()
    assert client.current_session is initial
    assert len(requests) == 1
    client.auth.sign_out()
    assert client.current_session is None
    assert len(requests) == 1


def test_token_bootstrap_can_refresh_when_a_refresh_token_was_supplied() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            return httpx.Response(
                200,
                json={
                    "access_token": bootstrap_token(renewed=True),
                    "refresh_token": "rotated-refresh",
                    "token_type": "bearer",
                    "expires_in": 3600,
                    "user": PROFILE,
                },
            )
        if request.headers["authorization"] == f"Bearer {bootstrap_token()}":
            return httpx.Response(401, json={"error": "expired"})
        return httpx.Response(200, json={"user": PROFILE})

    client = token_client(
        handle, refresh_token="supplied-refresh", access_token=bootstrap_token()
    )
    assert client.auth.get_user().id == USER_ID
    current = client.current_session
    assert current is not None
    assert current.refresh_token == "rotated-refresh"
    assert [request.headers["authorization"] for request in requests] == [
        f"Bearer {bootstrap_token()}",
        "Bearer anon",
        f"Bearer {bootstrap_token(renewed=True)}",
    ]


def test_bootstrap_profile_cannot_overwrite_a_replacement_session() -> None:
    replacement = Session("replacement", "refresh", USER_ID)

    def handle(_request: httpx.Request) -> httpx.Response:
        _ = client.auth.set_session(replacement)
        return httpx.Response(200, json={"user": PROFILE})

    client = token_client(handle)
    with pytest.raises(SessionChangedError):
        _ = client.auth.get_user()
    assert client.current_session == replacement


def test_bootstrap_cannot_change_identity_after_profile_validation() -> None:
    responses = iter(
        [PROFILE, {**PROFILE, "id": "00000000-0000-4000-8000-000000000002"}]
    )
    client = token_client(
        lambda _request: httpx.Response(200, json={"user": next(responses)})
    )
    _ = client.auth.get_user()
    with pytest.raises(AuthenticationError, match="does not match"):
        _ = client.auth.get_user()
    assert client.current_session is not None
    assert client.current_session.user_id == USER_ID


def test_bootstrap_does_not_relax_complete_session_adoption() -> None:
    client = token_client(lambda _request: httpx.Response(500))
    initial = client.current_session
    assert initial is not None
    with pytest.raises(ValueError, match="complete Session"):
        _ = client.auth.set_session(initial)
    assert client.current_session is initial


@pytest.mark.parametrize("access_token", ["", " "])
def test_bootstrap_rejects_empty_access_tokens(access_token: str) -> None:
    with pytest.raises(ValueError, match="access_token"):
        _ = VolcanoClient(anon_key="anon", access_token=access_token)


def test_bootstrap_rejects_refresh_without_access_token() -> None:
    with pytest.raises(ValueError, match="access_token"):
        _ = VolcanoClient(anon_key="anon", refresh_token="refresh")


@pytest.mark.parametrize("enrich_during_refresh", [False, True])
@pytest.mark.parametrize("operation", ["refresh", "mutation"])
def test_refresh_cannot_replace_a_validated_bootstrap_identity(
    *, enrich_during_refresh: bool, operation: str
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/user":
            return httpx.Response(200, json={"user": PROFILE})
        if request.url.path == "/auth/refresh":
            if enrich_during_refresh:
                _ = client.auth.get_user()
            return httpx.Response(
                200,
                json={
                    "access_token": "other-user-access",
                    "refresh_token": "other-user-refresh",
                    "token_type": "bearer",
                    "expires_in": 3600,
                    "user": {**PROFILE, "id": "00000000-0000-4000-8000-000000000002"},
                },
            )
        return httpx.Response(401, json={"error": "expired"})

    client = token_client(
        handle, refresh_token="supplied-refresh", access_token=bootstrap_token()
    )
    enrich_before_refresh(client, enrich_during_refresh=enrich_during_refresh)
    run: Callable[[], object] = (
        client.auth.refresh_session
        if operation == "refresh"
        else client.database("main").from_("items").insert({"name": "example"}).execute
    )
    with pytest.raises(AuthenticationError):
        _ = run()
    assert client.current_session is not None
    assert client.current_session.user_id == USER_ID
    assert client.current_session.access_token == bootstrap_token()
    assert all(
        request.headers["authorization"] != "Bearer other-user-access"
        for request in requests
    )


@pytest.mark.parametrize("refresh_token", [None, "another-session-refresh"])
@pytest.mark.parametrize("outcome", [204, 401, 503, "transport"])
@pytest.mark.parametrize("replace", [False, True])
def test_token_only_sign_out_revokes_the_captured_session(
    outcome: int | str, *, replace: bool, refresh_token: str | None
) -> None:
    session_id = "00000000-0000-4000-8000-000000000002"
    payload = (
        base64.urlsafe_b64encode(json.dumps({"session_id": session_id}).encode())
        .decode()
        .rstrip("=")
    )
    token = f"header.{payload}.signature"
    requests: list[httpx.Request] = []
    replacement = Session("replacement", "refresh", USER_ID)

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if replace:
            _ = client.auth.set_session(replacement)
        return revocation_response(request, outcome)

    client = token_client(handle, access_token=token, refresh_token=refresh_token)
    if replace or outcome != 204:
        with pytest.raises(SessionChangedError if replace else VolcanoError):
            client.auth.sign_out()
    else:
        client.auth.sign_out()
    expected = [("DELETE", f"/auth/user/sessions/{session_id}", f"Bearer {token}")]
    if outcome == 401 and refresh_token is not None:
        expected.append(("POST", "/auth/refresh", "Bearer anon"))
    assert [
        (r.method, r.url.path, r.headers["authorization"]) for r in requests
    ] == expected
    assert client.current_session == (replacement if replace else None)


def enrich_before_refresh(
    client: VolcanoClient, *, enrich_during_refresh: bool
) -> None:
    if not enrich_during_refresh:
        _ = client.auth.get_user()


def revocation_response(request: httpx.Request, outcome: int | str) -> httpx.Response:
    if outcome == "transport":
        message = "connection lost"
        raise httpx.ReadError(message, request=request)
    return httpx.Response(
        int(outcome),
        json={"error": "revocation failed"} if outcome != 204 else None,
    )
