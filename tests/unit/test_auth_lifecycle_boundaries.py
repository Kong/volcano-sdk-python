from __future__ import annotations

from typing import TYPE_CHECKING, Never

import httpx
import pytest
from test_session_continuity import (
    SESSION_A,
    SESSION_B,
    USER_A,
    access_token,
    client_for,
    refreshed,
)

from volcano_sdk import AuthenticationError, Session, SessionChangedError, VolcanoClient
from volcano_sdk import auth as auth_module
from volcano_sdk._session_operations import SessionOperations
from volcano_sdk._transport import GeneratedTransport
from volcano_sdk.auth import Auth, AuthContext

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from volcano_sdk import User
    from volcano_sdk._transport import Transport, TransportResponse
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


_CAPTURED_SESSION_OPERATIONS: tuple[Callable[[Auth], object], ...] = (
    lambda auth: auth.convert_anonymous(email="new@example.com", password="password"),
    lambda auth: auth.request_email_change(new_email="new@example.com"),
    lambda auth: auth.cancel_email_change(),
    lambda auth: auth.confirm_email_change(token="token"),
    lambda auth: auth.delete_all_other_sessions(),
    lambda auth: auth.list_sessions(),
    lambda auth: auth.list_linked_oauth_providers(),
    lambda auth: auth.link_oauth_provider(provider="github"),
    lambda auth: auth.unlink_oauth_provider(provider="github"),
    lambda auth: auth.get_oauth_provider_token(provider="github"),
    lambda auth: auth.refresh_oauth_provider_token(provider="github"),
    lambda auth: auth.delete_session(session_id="other-session"),
    lambda auth: auth.get_user(),
    lambda auth: auth.update_user(metadata={"name": "new"}),
)


@pytest.mark.parametrize(
    "operation",
    _CAPTURED_SESSION_OPERATIONS,
    ids=(
        "convert-anonymous",
        "request-email-change",
        "cancel-email-change",
        "confirm-email-change",
        "delete-other-sessions",
        "list-sessions",
        "list-oauth-providers",
        "link-oauth",
        "unlink-oauth",
        "get-oauth-token",
        "refresh-oauth-token",
        "delete-session",
        "get-user",
        "update-user",
    ),
)
def test_auth_request_keeps_its_captured_session_when_transport_becomes_available(
    operation: Callable[[Auth], object],
) -> None:
    old_session = Session("old-access", "old-refresh", USER_A)
    new_session = Session("new-access", "new-refresh", "other-user")
    binding = (0, SessionOperations(old_session), old_session)
    replacement = (1, SessionOperations(new_session), new_session)
    current = binding
    requests: list[httpx.Request] = []

    def capture() -> tuple[int, SessionOperations, Session | None]:
        return current

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200, json={"user": {"id": new_session.user_id, "email": "new@example.com"}}
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    def replace_before_request() -> Transport:
        nonlocal current
        current = replacement
        return transport

    def unused(*_args: object, **_kwargs: object) -> Never:
        pytest.fail("the stale request must not reach another client operation")

    auth = Auth(
        AuthContext(
            transport=replace_before_request,
            current_session=unused,
            anon_token=unused,
            api_base_url=unused,
            set_session=unused,
            capture_session=unused,
            capture_session_binding=capture,
            update_session_user_if_current=unused,
            set_session_if_current=unused,
            clear_session_if_current=unused,
            subscribe_auth_state_change=unused,
        )
    )

    with pytest.raises(SessionChangedError):
        _ = operation(auth)

    assert requests == []
    assert current is replacement


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


def test_auth_facade_rejects_a_refresh_from_another_server_session() -> None:
    current = Session(access_token(SESSION_A), "refresh", USER_A)
    binding = (0, SessionOperations(current), current)
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return refreshed(SESSION_B)

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    def unused(*_args: object, **_kwargs: object) -> Never:
        pytest.fail("an invalid refresh must not reach the client state adapter")

    auth = Auth(
        AuthContext(
            transport=lambda: transport,
            current_session=unused,
            anon_token=lambda: "anon",
            api_base_url=unused,
            set_session=unused,
            capture_session=unused,
            capture_session_binding=lambda: binding,
            update_session_user_if_current=unused,
            set_session_if_current=unused,
            clear_session_if_current=unused,
            subscribe_auth_state_change=unused,
        )
    )

    with pytest.raises(AuthenticationError, match="session"):
        _ = auth.refresh_session()

    assert [request.url.path for request in requests] == ["/auth/refresh"]


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
