from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import httpx
import pytest

from volcano_sdk import Session, SessionChangedError, VolcanoClient, VolcanoError
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


def refresh_response() -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "access_token": "access-2",
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
    client.auth.set_session(Session("access-1", "refresh-1", USER))
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
        "Bearer access-1",
        "Bearer anon",
        "Bearer access-2",
    ]
    assert requests[0].url == requests[2].url
    assert requests[0].method == requests[2].method
    assert requests[0].content == requests[2].content
    assert client.current_session is not None
    assert client.current_session.access_token == "access-2"


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
