from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import pytest

from volcano_sdk import (
    AuthenticationError,
    Session,
    SessionChangedError,
    TransportError,
    VolcanoClient,
    VolcanoError,
)
from volcano_sdk._transport import GeneratedTransport

if TYPE_CHECKING:
    from collections.abc import Callable


def make_client(handler: Callable[[httpx.Request], httpx.Response]) -> VolcanoClient:
    client = VolcanoClient(
        anon_key="anon",
        _transport=GeneratedTransport(
            api_url="https://api.test.volcano.dev",
            httpx_transport=httpx.MockTransport(handler),
        ),
    )
    client.auth.set_session(Session("old-access", "old-refresh", "user"))
    return client


def read_logs(client: VolcanoClient, operation: str) -> None:
    method = client.logs.search if operation == "search" else client.logs.activity
    result = method(
        "00000000-0000-4000-8000-000000000001",
        {"resource": {"type": "function"}},
    )
    assert result.data == ()


def refresh_response() -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "access_token": "new-access",
            "refresh_token": "new-refresh",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": {
                "id": "00000000-0000-4000-8000-000000000001",
                "email": "user@example.com",
                "status": "active",
            },
        },
    )


@pytest.mark.parametrize("operation", ["search", "activity"])
def test_logs_refresh_and_replay_the_same_request(operation: str) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            return refresh_response()
        if request.headers["authorization"] == "Bearer old-access":
            return httpx.Response(401, json={"error": "expired"})
        return httpx.Response(
            200, json={"data": [], "limit": 100, "has_more": False, "total": 0}
        )

    read_logs(make_client(handle), operation)

    assert [request.headers["authorization"] for request in requests] == [
        "Bearer old-access",
        "Bearer anon",
        "Bearer new-access",
    ]
    assert requests[0].url == requests[2].url
    assert requests[0].content == requests[2].content


@pytest.mark.parametrize("operation", ["search", "activity"])
@pytest.mark.parametrize("refresh_status", [200, 503])
def test_logs_bound_retries_and_preserve_the_original_failure(
    operation: str, refresh_status: int
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            if refresh_status == 200:
                return refresh_response()
            return httpx.Response(refresh_status, json={"error": "refresh failed"})
        return httpx.Response(401, json={"error": "logs denied"})

    with pytest.raises(AuthenticationError, match="logs denied"):
        read_logs(make_client(handle), operation)
    assert len(requests) == (3 if refresh_status == 200 else 2)


@pytest.mark.parametrize("operation", ["search", "activity"])
def test_logs_never_retry_under_a_replacement_session(operation: str) -> None:
    requests: list[httpx.Request] = []
    replacement = Session("replacement", "replacement-refresh", "other")

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            client.auth.set_session(replacement)
            return refresh_response()
        return httpx.Response(401, json={"error": "expired"})

    client = make_client(handle)
    with pytest.raises(SessionChangedError):
        read_logs(client, operation)
    assert client.current_session == replacement
    assert len(requests) == 2


@pytest.mark.parametrize("operation", ["search", "activity"])
@pytest.mark.parametrize("status", [403, 503])
def test_logs_do_not_refresh_other_http_failures(operation: str, status: int) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(status, json={"error": "logs unavailable"})

    with pytest.raises(VolcanoError, match="logs unavailable") as caught:
        read_logs(make_client(handle), operation)
    assert caught.value.status == status
    assert len(requests) == 1


@pytest.mark.parametrize("operation", ["search", "activity"])
def test_logs_do_not_refresh_transport_failures(operation: str) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        message = "response lost"
        raise httpx.ReadTimeout(message, request=request)

    with pytest.raises(TransportError):
        read_logs(make_client(handle), operation)
    assert len(requests) == 1
