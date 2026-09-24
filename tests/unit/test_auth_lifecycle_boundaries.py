from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import pytest
from test_session_continuity import SESSION_A, USER_A, client_for, refreshed

from volcano_sdk import AuthenticationError, Session, SessionChangedError, VolcanoClient
from volcano_sdk import auth as auth_module
from volcano_sdk._session_operations import SessionOperations

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from volcano_sdk import User
    from volcano_sdk._transport import TransportResponse
    from volcano_sdk.models import JSONValue


def test_profile_commit_rechecks_ownership_after_parsing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for(
        lambda _request: httpx.Response(
            200,
            json={
                "user": {"id": USER_A, "email": "user@example.com", "status": "active"}
            },
        )
    )
    replacement = Session("replacement", "replacement-refresh", "other-user")
    parse = auth_module._user_from_payload

    def parse_and_replace(payload: object) -> tuple[User, Mapping[str, JSONValue]]:
        profile = parse(payload)
        _ = client.auth.set_session(replacement)
        return profile

    monkeypatch.setattr(auth_module, "_user_from_payload", parse_and_replace)

    with pytest.raises(SessionChangedError):
        _ = client.auth.get_user()

    current = client.current_session
    assert current is not None
    assert current == replacement
    assert current.user is None


def test_session_request_requires_credentials_before_running_the_operation() -> None:
    client = VolcanoClient(anon_key="anon")

    def operation(_access_token: str) -> TransportResponse:
        pytest.fail("an unauthenticated operation must not run")

    with pytest.raises(RuntimeError, match="No active session"):
        _ = client.auth._session_request(operation)


def test_refresh_adopts_an_already_completed_refresh_without_rotating_again() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return refreshed(SESSION_A)

    client = client_for(handle)
    binding = client._capture_session_binding()
    assert binding[2] is not None
    completed = client.auth.refresh_session()
    notifications: list[Callable[[], None]] = []

    result = client.auth._perform_refresh(binding, binding[2], notifications)

    assert result is completed
    assert client.current_session is completed
    assert [request.url.path for request in requests] == ["/auth/refresh"]
    assert notifications == []


def test_empty_captured_sign_out_has_no_work_or_notifications() -> None:
    client = VolcanoClient(anon_key="anon")
    binding = client._capture_session_binding()
    notifications: list[Callable[[], None]] = []

    client.auth._sign_out_captured(binding, None, notifications, pending=False)

    assert client.current_session is None
    assert client._capture_session_binding() == binding
    assert notifications == []


def test_revocation_preserves_refresh_failure_without_an_access_session() -> None:
    client = VolcanoClient(anon_key="anon")
    failure = AuthenticationError("refresh rejected", status=401, code="expired")

    with pytest.raises(AuthenticationError) as caught:
        client.auth._revoke_session(
            Session("no-session-claim", "refresh", USER_A),
            SessionOperations(),
            failure,
            joined=True,
        )

    assert caught.value is failure


def test_joined_revocation_does_not_start_another_refresh_after_401() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(401, json={"error": "access expired", "code": "expired"})

    client = client_for(handle)
    original = client.current_session
    assert original is not None

    with pytest.raises(AuthenticationError) as caught:
        client.auth._revoke_access_session(original, SESSION_A, None, joined=True)

    assert caught.value.status == 401
    assert caught.value.code == "expired"
    assert str(caught.value) == "access expired"
    assert [(request.method, request.url.path) for request in requests] == [
        ("DELETE", f"/auth/user/sessions/{SESSION_A}")
    ]
    assert requests[0].headers["authorization"] == f"Bearer {original.access_token}"
    assert client.current_session is original
