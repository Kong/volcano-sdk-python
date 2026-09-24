from __future__ import annotations

import base64
import json
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from threading import Event, Thread, current_thread
from typing import TYPE_CHECKING

import httpx
import pytest

from volcano_sdk import AuthenticationError, Session, SessionChangedError, VolcanoClient
from volcano_sdk._transport import GeneratedTransport
from volcano_sdk.errors import VolcanoError

if TYPE_CHECKING:
    from collections.abc import Callable
    from concurrent.futures import Future

    from volcano_sdk._session_operations import SessionOperations

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
        _ = client.auth.get_user()
    with pytest.raises(AuthenticationError):
        _ = client.database("main").from_("items").insert({"name": "example"}).execute()
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
        _ = client.auth.refresh_session()
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
                _ = client.auth.set_session(replacement)
            return refreshed(SESSION_A)
        return expired_session_response(request)

    client = client_for(handle)
    if replace:
        with pytest.raises(SessionChangedError):
            client.auth.sign_out()
    else:
        client.auth.sign_out()
    assert [r.method for r in requests] == ["DELETE", "POST", "DELETE"]
    assert client.current_session == (replacement if replace else None)


def test_sign_out_prevents_a_new_refresh_of_the_same_server_session() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            return refreshed(SESSION_A)
        with pytest.raises(SessionChangedError):
            _ = client.auth.refresh_session()
        return httpx.Response(204)

    client = client_for(handle)
    client.auth.sign_out()
    assert client.current_session is None
    assert [r.method for r in requests] == ["DELETE"]


@pytest.mark.parametrize("token", ["a.é.c", "a.☃.c", "a.!!!!.c"])
def test_sign_out_clears_malformed_bootstrap_tokens(token: str) -> None:
    client = VolcanoClient(anon_key="anon", access_token=token)
    client.auth.sign_out()
    assert client.current_session is None


@pytest.mark.parametrize("operation", ["refresh", "sign_out"])
def test_deeply_nested_access_claims_remain_untrusted(operation: str) -> None:
    payload = '{"extra":' + "[" * 2000 + "0" + "]" * 2000 + "}"
    encoded = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(204)

    client = client_for(handle)
    _ = client.auth.set_session(
        Session(f"header.{encoded}.signature", "unverified-refresh", USER_A)
    )
    if operation == "refresh":
        with pytest.raises(AuthenticationError, match="without a session identifier"):
            _ = client.auth.refresh_session()
        assert client.current_session is not None
    else:
        client = VolcanoClient(
            anon_key="anon", access_token=f"header.{encoded}.signature"
        )
        client.auth.sign_out()
        assert client.current_session is None
    assert not requests


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


@pytest.mark.parametrize("replace_session", [False, True])
def test_sign_out_joins_a_refresh_that_already_owns_the_rotating_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    replace_session: bool,
) -> None:
    refresh_entered, finish_refresh, sign_out_captured = Event(), Event(), Event()
    requests: list[httpx.Request] = []

    client = client_for(
        joined_refresh_handler(requests, refresh_entered, finish_refresh)
    )
    capture = client._capture_session_binding

    def capture_and_signal() -> tuple[int, SessionOperations, Session | None]:
        binding = capture()
        if current_thread().name.startswith("logout"):
            sign_out_captured.set()
        return binding

    monkeypatch.setattr(client, "_capture_session_binding", capture_and_signal)
    with (
        ThreadPoolExecutor(thread_name_prefix="refresh") as refresher,
        ThreadPoolExecutor(thread_name_prefix="logout") as logout,
    ):
        refreshing = refresher.submit(client.auth.refresh_session)
        assert refresh_entered.wait(2)
        signing_out = logout.submit(client.auth.sign_out)
        try:
            assert sign_out_captured.wait(2)
            assert not signing_out.done()
            if replace_session:
                _ = client.auth.set_session(
                    Session("replacement", "replacement-refresh", USER_B)
                )
        finally:
            finish_refresh.set()
        # Logout may clear the lineage before the refresh caller reads it.
        with suppress(SessionChangedError):
            _ = refreshing.result(timeout=2)
        if replace_session:
            with pytest.raises(SessionChangedError):
                signing_out.result(timeout=2)
        else:
            signing_out.result(timeout=2)
    assert client.current_session == (
        Session("replacement", "replacement-refresh", USER_B)
        if replace_session
        else None
    )
    assert [r.url.path for r in requests] == ["/auth/refresh", "/auth/logout"]
    assert json.loads(requests[-1].content) == {"refresh_token": "rotated-refresh"}


@pytest.mark.parametrize("identifier", ["not-a-uuid", "../other-session", "", "  "])
def test_sign_out_uses_refresh_logout_for_an_invalid_session_claim(
    identifier: str,
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(204)

    client = client_for(handle)
    client._current_session = Session(access_token(identifier), "refresh", None)
    client.auth.sign_out()
    assert [r.url.path for r in requests] == ["/auth/logout"]
    assert client.current_session is None


@pytest.mark.parametrize("known_pair", [False, True])
@pytest.mark.parametrize("status", [401, 403, 429, 503])
def test_sign_out_surfaces_the_refresh_it_joined_without_claiming_replacement(
    monkeypatch: pytest.MonkeyPatch, status: int, *, known_pair: bool
) -> None:
    entered, release, claimed = Event(), Event(), Event()
    requests: list[httpx.Request] = []

    client = client_for(rejected_refresh_handler(requests, entered, release, status))
    if known_pair:
        _ = client.auth.sign_in(email="user@example.com", password="synthetic")
        requests.clear()
    original = client.auth._sign_out_captured

    def notify_claim(
        binding: tuple[int, SessionOperations, Session | None],
        preceding: Future[Session] | None,
        notifications: list[Callable[[], None]],
        *,
        pending: bool,
    ) -> None:
        claimed.set()
        original(binding, preceding, notifications, pending=pending)

    monkeypatch.setattr(client.auth, "_sign_out_captured", notify_claim)
    with ThreadPoolExecutor(max_workers=2) as pool:
        refreshing = pool.submit(client.auth.refresh_session)
        assert entered.wait(2)
        signing_out = pool.submit(client.auth.sign_out)
        try:
            assert claimed.wait(2)
        finally:
            release.set()
        with suppress(VolcanoError):
            _ = refreshing.result(timeout=2)
        if known_pair and status == 429:
            assert signing_out.result(timeout=2) is None
        else:
            with pytest.raises(VolcanoError) as caught:
                signing_out.result(timeout=2)
            assert not isinstance(caught.value, SessionChangedError)
            assert caught.value.status == status
    assert [r.method for r in requests] == [
        "POST",
        "POST" if known_pair and status == 429 else "DELETE",
    ]
    assert client.current_session is None


def test_rejection_between_logout_capture_and_claim_is_not_replacement(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    entered, release, finished = Event(), Event(), Event()

    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/auth/refresh" and not entered.is_set():
            entered.set()
            assert release.wait(2)
        return httpx.Response(401, json={"error": "rejected"})

    client = client_for(handle)
    capture = client._capture_session_binding

    def capture_before_rejection() -> tuple[int, SessionOperations, Session | None]:
        binding = capture()
        if current_thread().name == "MainThread":
            release.set()
            assert finished.wait(2)
        return binding

    with ThreadPoolExecutor(max_workers=1) as pool:
        refreshing = pool.submit(client.auth.refresh_session)
        refreshing.add_done_callback(lambda _: finished.set())
        assert entered.wait(2)
        monkeypatch.setattr(
            client, "_capture_session_binding", capture_before_rejection
        )
        with pytest.raises(VolcanoError) as caught:
            client.auth.sign_out()
    assert not isinstance(caught.value, SessionChangedError)
    assert client.current_session is None


@pytest.mark.parametrize("refresh_first", [False, True])
def test_sign_out_revokes_a_server_issued_pair_without_access_renewal(
    *, refresh_first: bool
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return verified_pair_response(request)

    client = client_for(handle)
    _ = client.auth.sign_in(email="user@example.com", password="synthetic")
    if refresh_first:
        with pytest.raises(VolcanoError) as caught:
            _ = client.auth.refresh_session()
        assert caught.value.status == 429
    owner = client._capture_session_binding()[1]
    client.auth.sign_out()
    expected = (
        ["/auth/signin"]
        + (["/auth/refresh"] if refresh_first else [])
        + ["/auth/logout"]
    )
    assert [r.url.path for r in requests] == expected
    assert owner._verified_pair is None
    assert owner.refreshing is None


@pytest.mark.parametrize("hosted", [False, True])
def test_explicit_adoption_does_not_inherit_server_pair_provenance(
    *, hosted: bool
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/signin":
            return refreshed(SESSION_A)
        return httpx.Response(204)

    client = client_for(handle)
    original = client.auth.sign_in(email="user@example.com", password="synthetic")
    supplied = Session(access_token(SESSION_B), original.refresh_token, USER_B)
    if hosted:
        _ = client.auth.adopt_hosted_auth_session(
            supplied, state="nonce", expected_state="nonce"
        )
    else:
        _ = client.auth.set_session(supplied)
    client.auth.sign_out()
    assert [r.url.path for r in requests] == [
        "/auth/signin",
        f"/auth/user/sessions/{SESSION_B}",
    ]


@pytest.mark.parametrize("status", [204, 503])
def test_concurrent_sign_out_shares_revocation_outcome(
    monkeypatch: pytest.MonkeyPatch, status: int
) -> None:
    entered, release, captured = Event(), Event(), Event()
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        entered.set()
        assert release.wait(2)
        return httpx.Response(status, json={"error": "unavailable"})

    client = client_for(handle)
    capture = client._capture_session_binding

    def notify_capture() -> tuple[int, SessionOperations, Session | None]:
        binding = capture()
        captured.set()
        return binding

    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(client.auth.sign_out)
        assert entered.wait(2)
        monkeypatch.setattr(client, "_capture_session_binding", notify_capture)
        second = pool.submit(client.auth.sign_out)
        try:
            assert captured.wait(2)
        finally:
            release.set()
        for operation in (first, second):
            if status == 204:
                assert operation.result(timeout=2) is None
            else:
                with pytest.raises(VolcanoError) as caught:
                    operation.result(timeout=2)
                assert caught.value.status == status
    assert len(requests) == 1
    assert client.current_session is None


@pytest.mark.parametrize("status", [204, 503])
def test_sign_out_joins_an_outcome_after_local_clearing(
    monkeypatch: pytest.MonkeyPatch, status: int
) -> None:
    cleared, release, joined = Event(), Event(), Event()
    client = client_for(lambda _: httpx.Response(status, json={"error": "unavailable"}))
    owner = client._capture_session_binding()[1]
    original = client.auth._sign_out_captured

    def pause_after_clear(
        binding: tuple[int, SessionOperations, Session | None],
        preceding: Future[Session] | None,
        notifications: list[Callable[[], None]],
        *,
        pending: bool,
    ) -> None:
        try:
            original(binding, preceding, notifications, pending=pending)
        finally:
            cleared.set()
            assert release.wait(2)

    monkeypatch.setattr(client.auth, "_sign_out_captured", pause_after_clear)
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(client.auth.sign_out)
        assert cleared.wait(2)
        assert owner.signing_out is not None
        result = owner.signing_out.result

        def observe_join(timeout: float | None = None) -> BaseException | None:
            joined.set()
            return result(timeout)

        monkeypatch.setattr(owner.signing_out, "result", observe_join)
        second = pool.submit(client.auth.sign_out)
        try:
            assert joined.wait(2)
        finally:
            release.set()
        for operation in (first, second):
            if status == 204:
                assert operation.result(timeout=2) is None
            else:
                with pytest.raises(VolcanoError) as caught:
                    operation.result(timeout=2)
                assert caught.value.status == status
    client.auth.sign_out()


@pytest.mark.parametrize("enriched", [False, True])
def test_supplied_profile_does_not_authorize_refresh_without_sid(
    *, enriched: bool
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
        return refreshed(SESSION_B)

    client = client_for(handle)
    _ = client.auth.set_session(Session("opaque", "foreign-refresh", USER_A))
    if enriched:
        _ = client.auth.get_user()
        requests.clear()
    with pytest.raises(AuthenticationError, match="session identifier"):
        _ = client.auth.refresh_session()
    assert not requests
    assert client.current_session is not None
    assert client.current_session.access_token == "opaque"


@pytest.mark.parametrize("fails", [False, True])
def test_delete_current_session_discards_retained_credentials(*, fails: bool) -> None:
    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.path in {"/auth/signin", "/auth/refresh"}:
            return refreshed(SESSION_A)
        if fails:
            message = "response lost"
            raise httpx.ReadError(message, request=request)
        return httpx.Response(204)

    client = client_for(handle)
    _ = client.auth.sign_in(email="u@example.com", password="synthetic")
    _ = client.auth.refresh_session()
    _, owner, session = client._capture_session_binding()
    assert session is not None
    if fails:
        with pytest.raises(VolcanoError, match="response lost"):
            client.auth.delete_session(session_id=SESSION_A)
    else:
        client.auth.delete_session(session_id=SESSION_A)
    assert client.current_session is None
    assert not owner.has_verified_pair(session)
    assert owner.refreshing is None
    client.auth.sign_out()


def test_deletion_does_not_retain_a_later_refresh_result() -> None:
    entered, release = Event(), Event()

    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/auth/refresh":
            entered.set()
            assert release.wait(2)
            return refreshed(SESSION_A)
        return httpx.Response(204)

    client = client_for(handle)
    owner = client._capture_session_binding()[1]
    with ThreadPoolExecutor(max_workers=1) as pool:
        refreshing = pool.submit(client.auth.refresh_session)
        try:
            assert entered.wait(2)
            client.auth.delete_session(session_id=SESSION_A)
        finally:
            release.set()
        with pytest.raises(SessionChangedError):
            _ = refreshing.result(2)
    assert client.current_session is None
    assert owner.refreshing is None
    assert owner._verified_pair is None


def test_local_clear_before_refresh_claim_prevents_io(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    entered, release = Event(), Event()
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        message = "delete response lost"
        raise httpx.ReadError(message, request=request)

    client = client_for(handle)
    owner = client._capture_session_binding()[1]
    claim = owner.refresh

    def delayed_claim(operation: Callable[[], Session]) -> Session:
        entered.set()
        assert release.wait(2)
        return claim(operation)

    monkeypatch.setattr(owner, "refresh", delayed_claim)
    with ThreadPoolExecutor(max_workers=1) as pool:
        refreshing = pool.submit(client.auth.refresh_session)
        try:
            assert entered.wait(2)
            with pytest.raises(VolcanoError, match="delete response lost"):
                client.auth.delete_session(session_id=SESSION_A)
        finally:
            release.set()
        with pytest.raises(SessionChangedError):
            _ = refreshing.result(2)
    assert len(requests) == 1
    assert requests[0].url.path == f"/auth/user/sessions/{SESSION_A}"
    assert client.current_session is None


def _refresh_until_session_changes(
    client: VolcanoClient, finished: Event, outcomes: list[str]
) -> None:
    try:
        _ = client.auth.refresh_session()
    except SessionChangedError:
        outcomes.append("changed")
    finally:
        finished.set()


@pytest.mark.parametrize("action", ["sign_out", "replace"])
def test_refresh_rechecks_ownership_after_notifying_subscribers(action: str) -> None:
    def handle(request: httpx.Request) -> httpx.Response:
        return (
            refreshed(SESSION_A)
            if request.url.path == "/auth/refresh"
            else httpx.Response(204)
        )

    client = client_for(handle)
    replacement = Session(access_token(SESSION_B), "other-refresh", USER_B)

    def on_change(event: str, _session: Session | None) -> None:
        if event == "TOKEN_REFRESHED":
            if action == "sign_out":
                client.auth.sign_out()
            else:
                _ = client.auth.set_session(replacement)

    _ = client.auth.on_auth_state_change(on_change)
    finished = Event()
    outcomes: list[str] = []
    worker = Thread(
        target=_refresh_until_session_changes,
        args=(client, finished, outcomes),
        daemon=True,
    )
    worker.start()
    assert finished.wait(2), "refresh callback blocked the session owner"
    worker.join(timeout=0)
    assert outcomes == ["changed"]
    assert client.current_session == (None if action == "sign_out" else replacement)


def test_failed_sign_out_does_not_store_a_credential_bearing_traceback() -> None:
    def handle(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            503, json={"error": "revocation unavailable", "code": "unavailable"}
        )

    client = client_for(handle)
    owner = client._capture_session_binding()[1]
    with pytest.raises(VolcanoError, match="revocation unavailable") as caught:
        client.auth.sign_out()
    assert caught.value.status == 503
    assert caught.value.code == "unavailable"
    assert owner.signing_out is not None
    assert owner.signing_out.exception() is None
    failure = owner.signing_out.result()
    assert isinstance(failure, VolcanoError)
    assert failure.__traceback__ is None
    assert failure.__context__ is None
    assert failure.__cause__ is None


def expired_session_response(request: httpx.Request) -> httpx.Response:
    assert request.url.path == f"/auth/user/sessions/{SESSION_A}"
    if request.headers["authorization"] == f"Bearer {access_token(SESSION_A)}":
        return httpx.Response(401, json={"error": "expired"})
    assert (
        request.headers["authorization"]
        == f"Bearer {access_token(SESSION_A, renewed=True)}"
    )
    return httpx.Response(204)


def joined_refresh_handler(
    requests: list[httpx.Request], refresh_entered: Event, finish_refresh: Event
) -> Callable[[httpx.Request], httpx.Response]:
    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            if refresh_entered.is_set():
                return httpx.Response(401, json={"error": "refresh token consumed"})
            refresh_entered.set()
            assert finish_refresh.wait(2)
            return refreshed(SESSION_A)
        if request.headers["authorization"] == f"Bearer {access_token(SESSION_A)}":
            return httpx.Response(401, json={"error": "expired"})
        return httpx.Response(204)

    return handle


def rejected_refresh_handler(
    requests: list[httpx.Request], entered: Event, release: Event, status: int
) -> Callable[[httpx.Request], httpx.Response]:
    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/signin":
            return refreshed(SESSION_A)
        if request.url.path == "/auth/logout":
            return httpx.Response(204)
        if request.url.path == "/auth/refresh":
            entered.set()
            assert release.wait(2)
            return httpx.Response(status, json={"error": "refresh rejected"})
        return httpx.Response(401, json={"error": "expired access"})

    return handle


def verified_pair_response(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/auth/signin":
        return refreshed(SESSION_A)
    if request.url.path == "/auth/logout":
        return httpx.Response(204)
    if request.url.path == "/auth/refresh":
        return httpx.Response(429, json={"error": "rate limited"})
    return httpx.Response(401, json={"error": "expired"})
