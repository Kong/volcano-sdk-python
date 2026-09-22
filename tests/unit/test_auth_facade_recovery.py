from __future__ import annotations

import base64
import json
from copy import deepcopy
from dataclasses import dataclass
from typing import TYPE_CHECKING

import httpx
import pytest
from session_fixtures import access_token

from volcano_sdk import Session, SessionChangedError, VolcanoClient, VolcanoError
from volcano_sdk import auth as auth_module
from volcano_sdk._transport import GeneratedTransport

if TYPE_CHECKING:
    from collections.abc import Callable

    from volcano_sdk.models import JSONValue

USER = "00000000-0000-4000-8000-000000000001"
SESSION = "00000000-0000-4000-8000-000000000009"


@dataclass(frozen=True)
class AuthCase:
    name: str
    invoke: Callable[[VolcanoClient], object]
    status: int = 200
    body: dict[str, JSONValue] | None = None


CASES = [
    AuthCase(
        "request_email",
        lambda c: c.auth.request_email_change(new_email="new@example.com"),
        body={},
    ),
    AuthCase("cancel_email", lambda c: c.auth.cancel_email_change(), body={}),
    AuthCase(
        "list_sessions",
        lambda c: c.auth.list_sessions(page=2, limit=10),
        body={"sessions": [], "total": 0, "page": 2, "limit": 10, "total_pages": 0},
    ),
    AuthCase("delete_others", lambda c: c.auth.delete_all_other_sessions(), status=204),
    AuthCase(
        "delete_session",
        lambda c: c.auth.delete_session(session_id=SESSION),
        status=204,
    ),
    AuthCase(
        "providers",
        lambda c: c.auth.list_linked_oauth_providers(),
        body={"providers": []},
    ),
    AuthCase(
        "link",
        lambda c: c.auth.link_oauth_provider(provider="github"),
        body={"authorization_url": "https://provider.example/authorize"},
    ),
    AuthCase(
        "unlink", lambda c: c.auth.unlink_oauth_provider(provider="github"), status=204
    ),
    AuthCase(
        "token",
        lambda c: c.auth.get_oauth_provider_token(provider="github"),
        body={"message": "valid", "provider": "github", "expires_in": 30},
    ),
    AuthCase(
        "refresh_token",
        lambda c: c.auth.refresh_oauth_provider_token(provider="github"),
        body={"message": "valid", "provider": "github", "expires_in": 30},
    ),
    AuthCase(
        "provider_api",
        lambda c: c.auth.call_oauth_api(
            provider="github",
            endpoint="/user",
            method="POST",
            body={"name": "original"},
        ),
        body={
            "provider": "github",
            "endpoint": "/user",
            "status_code": 200,
            "data": {"ok": True},
        },
    ),
]


def refresh_response(access: str = access_token("rotated")) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "access_token": access,
            "refresh_token": "refresh-2",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": {"id": USER, "email": "u@example.com", "status": "active"},
        },
    )


def client_for(handler: Callable[[httpx.Request], httpx.Response]) -> VolcanoClient:
    client = VolcanoClient(
        anon_key="anon",
        _transport=GeneratedTransport(
            api_url="https://api.test.volcano.dev",
            httpx_transport=httpx.MockTransport(handler),
        ),
    )
    client.auth.set_session(Session(access_token("original"), "refresh-1", USER))
    return client


@pytest.mark.parametrize("case", CASES, ids=lambda case: case.name)
@pytest.mark.parametrize(
    "rejection", [b'{"error":"expired"}', b"", b"<h1>Unauthorized</h1>"]
)
def test_auth_facade_replays_only_the_captured_request_after_401(
    case: AuthCase, rejection: bytes
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            return refresh_response()
        if len(requests) == 1:
            return httpx.Response(401, content=rejection)
        return httpx.Response(case.status, json=case.body)

    client = client_for(handle)
    case.invoke(client)
    assert [request.headers["authorization"] for request in requests] == [
        f"Bearer {access_token('original')}",
        "Bearer anon",
        f"Bearer {access_token('rotated')}",
    ]
    assert requests[0].url == requests[2].url
    assert requests[0].method == requests[2].method
    assert requests[0].content == requests[2].content
    assert client.current_session is not None
    assert client.current_session.access_token == access_token("rotated")


@pytest.mark.parametrize("case", CASES, ids=lambda case: case.name)
def test_auth_facade_bounds_repeated_auth_rejection(case: AuthCase) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return (
            refresh_response()
            if request.url.path == "/auth/refresh"
            else httpx.Response(401, json={"error": "expired"})
        )

    with pytest.raises(VolcanoError) as caught:
        case.invoke(client_for(handle))
    assert caught.value.status == 401
    assert len(requests) == 3


@pytest.mark.parametrize("case", CASES, ids=lambda case: case.name)
@pytest.mark.parametrize("failure", ["transport", "503"])
def test_auth_facade_does_not_replay_ambiguous_failure(
    case: AuthCase, failure: str
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if failure == "transport":
            message = "response lost"
            raise httpx.ReadError(message, request=request)
        return httpx.Response(503, json={"error": "unavailable"})

    with pytest.raises(VolcanoError):
        case.invoke(client_for(handle))
    assert len(requests) == 1


@pytest.mark.parametrize("case", CASES, ids=lambda case: case.name)
def test_auth_facade_preserves_replacement_without_replaying(case: AuthCase) -> None:
    requests: list[httpx.Request] = []
    replacement = Session("other", "other-refresh", "other-user")

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        client.auth.set_session(replacement)
        return httpx.Response(401, json={"error": "expired"})

    client = client_for(handle)
    with pytest.raises(SessionChangedError):
        case.invoke(client)
    assert len(requests) == 1
    assert client.current_session == replacement


def session_token(*, renewed: bool = False) -> str:
    payload = (
        base64.urlsafe_b64encode(
            json.dumps({"session_id": SESSION, "renewed": renewed}).encode()
        )
        .decode()
        .rstrip("=")
    )
    return f"header.{payload}.signature"


def test_oauth_recovery_replays_a_snapshot_of_the_nested_body() -> None:
    body: dict[str, JSONValue] = {"names": ["original"]}
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            return refresh_response()
        if len(requests) == 1:
            body["names"] = ["changed"]
            return httpx.Response(401)
        return httpx.Response(
            200,
            json={
                "provider": "github",
                "endpoint": "/user",
                "status_code": 200,
                "data": {},
            },
        )

    client_for(handle).auth.call_oauth_api(
        provider="github", endpoint="/user", method="POST", body=body
    )
    assert requests[0].content == requests[2].content
    assert json.loads(requests[2].content)["body"] == {"names": ["original"]}


def test_oauth_captures_ownership_before_copying_the_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests: list[httpx.Request] = []
    replacement = Session("other", "other-refresh", "other-user")

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200)

    client = client_for(handle)

    def replace_while_copying(value: dict[str, JSONValue]) -> dict[str, JSONValue]:
        client.auth.set_session(replacement)
        return deepcopy(value)

    monkeypatch.setattr(auth_module, "deepcopy", replace_while_copying)
    with pytest.raises(SessionChangedError):
        client.auth.call_oauth_api(provider="github", endpoint="/user", body={"x": 1})
    assert client.current_session == replacement
    assert not requests


@pytest.mark.parametrize(
    "case",
    [case for case in CASES if case.name in {"token", "refresh_token", "provider_api"}],
    ids=lambda case: case.name,
)
@pytest.mark.parametrize(
    "payload", [b"", b"not-json", b"null", b"42", b"true", b"\xff"]
)
def test_malformed_oauth_response_preserves_session_without_retry(
    case: AuthCase, payload: bytes
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, content=payload)

    client = client_for(handle)
    original = client.current_session
    message = (
        "Expected OAuth provider API response data"
        if case.name == "provider_api"
        else "Expected complete OAuth provider token status"
    )

    with pytest.raises(VolcanoError, match=message) as error:
        case.invoke(client)

    assert error.value.__cause__ is not None
    assert client.current_session is original
    assert len(requests) == 1
    assert requests[0].headers["authorization"] == f"Bearer {access_token('original')}"


def test_oauth_get_without_a_body_preserves_the_provider_response() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "provider": "github",
                "endpoint": "/user",
                "status_code": 200,
                "data": {"name": "reader"},
            },
        )

    result = client_for(handle).auth.call_oauth_api(provider="github", endpoint="/user")

    assert result == {"name": "reader"}
    assert len(requests) == 1
    assert json.loads(requests[0].content) == {"endpoint": "/user", "method": "GET"}


@pytest.mark.parametrize("timing", ["401", "during_delete"])
@pytest.mark.parametrize("failure", [False, True])
def test_delete_current_session_clears_refreshed_descendant(
    timing: str, *, failure: bool
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            return refresh_response(session_token(renewed=True))
        if len(requests) == 1:
            if timing == "401":
                return httpx.Response(401)
            client.auth.refresh_session()
        return deletion_response(request, failure=failure)

    client = client_for(handle)
    client.auth.set_session(Session(session_token(), "refresh-1", USER))
    delete_current_session(client, failure=failure)
    assert client.current_session is None
    assert len(requests) == (3 if timing == "401" else 2)


@pytest.mark.parametrize("failure", [False, True])
def test_delete_current_session_preserves_explicit_replacement(
    *, failure: bool
) -> None:
    replacement = Session("other", "other-refresh", "other-user")

    def handle(request: httpx.Request) -> httpx.Response:
        client.auth.set_session(replacement)
        return deletion_response(request, failure=failure)

    client = client_for(handle)
    client.auth.set_session(Session(session_token(), "refresh-1", USER))
    with pytest.raises(SessionChangedError):
        client.auth.delete_session(session_id=SESSION)
    assert client.current_session == replacement


@pytest.mark.parametrize("clearing", ["sign_out", "rejected_refresh"])
def test_delete_other_session_rejects_completion_after_local_clear(
    clearing: str,
) -> None:
    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/auth/refresh":
            return httpx.Response(401, json={"error": "expired refresh"})
        if request.url.path.endswith(SESSION):
            if clearing == "sign_out":
                client.auth.sign_out()
            else:
                with pytest.raises(VolcanoError, match="expired refresh"):
                    client.auth.refresh_session()
        return httpx.Response(204)

    client = client_for(handle)
    with pytest.raises(SessionChangedError):
        client.auth.delete_session(session_id=SESSION)
    assert client.current_session is None


def deletion_response(request: httpx.Request, *, failure: bool) -> httpx.Response:
    if failure:
        message = "response lost"
        raise httpx.ReadError(message, request=request)
    return httpx.Response(204)


def delete_current_session(client: VolcanoClient, *, failure: bool) -> None:
    if failure:
        with pytest.raises(VolcanoError, match="response lost"):
            client.auth.delete_session(session_id=SESSION)
        return
    client.auth.delete_session(session_id=SESSION)
