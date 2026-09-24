from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import pytest
from test_function_refresh import make_client, refreshed_response

from volcano_sdk import AuthenticationError, Session, VolcanoClient
from volcano_sdk._session import validate_refresh_identity
from volcano_sdk._transport import GeneratedTransport
from volcano_sdk.client import (
    _bootstrap_session,
    _BootstrapCredentials,
    _CallbackOutcome,
)

if TYPE_CHECKING:
    from volcano_sdk.models import AuthChangeEvent, AuthStateCallback


class ExtraCredentials(_BootstrapCredentials):
    misspelled_token: str


class SubscriberAbortError(BaseException):
    pass


def failing_subscriber(
    error: SubscriberAbortError,
    received: list[SubscriberAbortError],
) -> AuthStateCallback:
    def receive(event: AuthChangeEvent, _session: Session | None) -> None:
        if event == "SIGNED_IN":
            received.append(error)
            raise error

    return receive


def test_bootstrap_rejects_extra_keys_in_a_structural_credentials_subtype() -> None:
    credentials = ExtraCredentials(misspelled_token="access")
    with pytest.raises(
        TypeError, match="Unexpected keyword argument: misspelled_token"
    ):
        _ = _bootstrap_session(credentials)


def test_lock_requests_require_a_service_key_before_transport() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"held": False})

    client = VolcanoClient(
        anon_key="anon",
        _transport=GeneratedTransport(
            api_url="https://api.test.volcano.dev",
            httpx_transport=httpx.MockTransport(handle),
        ),
    )
    with pytest.raises(RuntimeError, match="No service key configured"):
        _ = client.locks.get("build")
    assert requests == []


def test_profile_update_cannot_populate_an_absent_session() -> None:
    client = VolcanoClient(anon_key="anon")
    generation, session = client._capture_session()
    assert isinstance(generation, int)
    assert session is None

    assert not client._update_session_user_if_current({"id": "user"}, generation)
    assert client.current_session is None


def test_refresh_identity_without_a_previous_session_has_no_constraint() -> None:
    refreshed = Session("access", "refresh", "user")
    validate_refresh_identity(None, refreshed)


def test_callback_dispatch_state_has_boolean_ownership_and_empty_failure() -> None:
    outcome = _CallbackOutcome()
    assert outcome.error is None

    client = make_client(lambda _request: refreshed_response())
    assert client._dispatching_auth_notifications is False
    events: list[str] = []
    _ = client.auth.on_auth_state_change(lambda event, _session: events.append(event))
    _ = client.auth.sign_in(email="user@example.com", password="example")
    assert events == ["INITIAL_SESSION", "SIGNED_IN"]
    assert client._dispatching_auth_notifications is False


def test_refresh_commit_rejects_a_changed_user_before_replacing_credentials() -> None:
    client = VolcanoClient(anon_key="anon")
    original = client.auth.set_session(Session("access", "refresh", "user-a"))
    generation, captured = client._capture_session()
    assert captured is original

    with pytest.raises(AuthenticationError, match="different user"):
        _ = client._set_session_if_current(
            Session("new-access", "new-refresh", "user-b"),
            generation,
            event="TOKEN_REFRESHED",
        )

    assert client.current_session is original
    assert client._capture_session()[0] == generation


def test_reentrant_subscription_receives_initial_state_after_current_dispatch() -> None:
    client = make_client(lambda _request: refreshed_response())
    received: list[tuple[str, str, Session | None]] = []

    def late(event: AuthChangeEvent, session: Session | None) -> None:
        received.append(("late", event, session))

    def first(event: AuthChangeEvent, session: Session | None) -> None:
        received.append(("first", event, session))
        if event == "SIGNED_IN":
            _ = client.auth.on_auth_state_change(late)
            received.append(("subscribed", event, session))

    _ = client.auth.on_auth_state_change(first)
    _ = client.auth.on_auth_state_change(
        lambda event, session: received.append(("second", event, session))
    )
    received.clear()

    session = client.auth.sign_in(email="user@example.com", password="example")

    assert received == [
        ("first", "SIGNED_IN", session),
        ("subscribed", "SIGNED_IN", session),
        ("second", "SIGNED_IN", session),
        ("late", "INITIAL_SESSION", session),
    ]


def test_dispatch_removes_all_aborted_subscribers_and_preserves_the_first_failure() -> (
    None
):
    client = make_client(lambda _request: refreshed_response())
    first_error = SubscriberAbortError("first")
    second_error = SubscriberAbortError("second")
    failures: list[SubscriberAbortError] = []
    events: list[tuple[str, Session | None]] = []
    _ = client.auth.on_auth_state_change(failing_subscriber(first_error, failures))
    _ = client.auth.on_auth_state_change(failing_subscriber(second_error, failures))
    _ = client.auth.on_auth_state_change(
        lambda event, session: events.append((event, session))
    )
    events.clear()

    with pytest.raises(SubscriberAbortError) as caught:
        _ = client.auth.sign_in(email="user@example.com", password="example")

    first_session = client.current_session
    assert caught.value is first_error
    assert failures == [first_error, second_error]
    assert events == [("SIGNED_IN", first_session)]
    second_session = client.auth.sign_in(email="user@example.com", password="example")
    assert failures == [first_error, second_error]
    assert events == [("SIGNED_IN", first_session), ("SIGNED_IN", second_session)]
