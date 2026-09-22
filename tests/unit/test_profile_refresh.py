from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import pytest
from session_fixtures import access_token

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

OPERATIONS = ("get_user", "update_user", "convert_anonymous", "confirm_email_change")
USER_ID = "00000000-0000-4000-8000-000000000001"
PROFILE = {"id": USER_ID, "email": "updated@example.com", "status": "active"}


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


def profile_operation(
    client: VolcanoClient, operation: str, metadata: dict[str, object]
) -> object:
    operations: dict[str, Callable[[], object]] = {
        "get_user": client.auth.get_user,
        "update_user": lambda: client.auth.update_user(
            password="secret", metadata=metadata
        ),
        "convert_anonymous": lambda: client.auth.convert_anonymous(
            email="updated@example.com", password="secret", metadata=metadata
        ),
        "confirm_email_change": lambda: client.auth.confirm_email_change(
            token="confirmation"
        ),
    }
    return operations[operation]()


def refresh_response() -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "access_token": access_token("new"),
            "refresh_token": "new-refresh",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": PROFILE,
        },
    )


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("rejection", [b'{"error":"expired"}', b"", b"not json"])
def test_profile_refreshes_once_preserving_request_and_cached_user(
    operation: str, rejection: bytes
) -> None:
    requests: list[httpx.Request] = []
    roles = ["editor"]
    metadata: dict[str, object] = {"roles": roles}

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            roles.append("changed while refreshing")
            return refresh_response()
        if request.headers["authorization"] == f"Bearer {access_token('old')}":
            return httpx.Response(401, content=rejection)
        return httpx.Response(200, json={"user": PROFILE})

    client = make_client(handle)
    events: list[str] = []
    client.auth.on_auth_state_change(lambda event, _session: events.append(event))
    profile_operation(client, operation, metadata)
    assert [r.headers["authorization"] for r in requests] == [
        f"Bearer {access_token('old')}",
        "Bearer anon",
        f"Bearer {access_token('new')}",
    ]
    assert requests[0].url == requests[2].url
    assert requests[0].method == requests[2].method
    assert requests[0].content == requests[2].content
    assert client.current_session is not None
    assert client.current_session.access_token == access_token("new")
    assert client.current_session.user is not None
    assert client.current_session.user["email"] == PROFILE["email"]
    assert events == ["INITIAL_SESSION", "TOKEN_REFRESHED"]


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("refresh_status", [200, 401, 503])
def test_profile_bounds_retries_and_retains_original_failure(
    operation: str, refresh_status: int
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            return (
                refresh_response()
                if refresh_status == 200
                else httpx.Response(refresh_status, json={"error": "refresh failed"})
            )
        return httpx.Response(401, json={"error": "profile denied"})

    client = make_client(handle)
    with pytest.raises(AuthenticationError, match="profile denied"):
        profile_operation(client, operation, {})
    assert len(requests) == (3 if refresh_status == 200 else 2)
    assert (client.current_session is None) == (refresh_status == 401)


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("status", [403, 500])
def test_profile_does_not_refresh_other_failures(operation: str, status: int) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(status, json={"error": "denied"})

    with pytest.raises(VolcanoError):
        profile_operation(make_client(handle), operation, {})
    assert len(requests) == 1


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("replace_at", ["first", "refresh", "retry"])
def test_profile_refresh_never_adopts_a_replacement_session(
    operation: str, replace_at: str
) -> None:
    requests: list[httpx.Request] = []
    replacement = Session("replacement-access", "replacement-refresh", USER_ID)

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        stage = (
            "refresh"
            if request.url.path == "/auth/refresh"
            else ("first" if len(requests) == 1 else "retry")
        )
        if stage == replace_at:
            client.auth.set_session(replacement)
        if stage == "refresh":
            return refresh_response()
        return (
            httpx.Response(401, json={"error": "expired"})
            if stage == "first"
            else httpx.Response(200, json={"user": PROFILE})
        )

    client = make_client(handle)
    with pytest.raises(SessionChangedError):
        profile_operation(client, operation, {})
    assert client.current_session == replacement
    assert len(requests) == {"first": 1, "refresh": 2, "retry": 3}[replace_at]


@pytest.mark.parametrize("operation", OPERATIONS)
def test_profile_does_not_replay_an_ambiguous_transport_failure(operation: str) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        message = "response lost"
        raise httpx.ReadError(message, request=request)

    with pytest.raises(VolcanoError, match="response lost"):
        profile_operation(make_client(handle), operation, {})
    assert len(requests) == 1


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize(
    "payload", [b"", b"not-json", b"null", b"42", b"true", b"\xff"]
)
def test_malformed_profile_response_preserves_the_current_session(
    operation: str, payload: bytes
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, content=payload)

    client = make_client(handle)
    original = client.current_session

    with pytest.raises(
        AuthenticationError, match="Expected a complete user profile"
    ) as error:
        profile_operation(client, operation, {})

    assert error.value.__cause__ is not None
    assert client.current_session is original
    assert len(requests) == 1
    assert requests[0].headers["authorization"] == f"Bearer {access_token('old')}"
