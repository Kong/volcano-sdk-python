from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from volcano_sdk import Session, User, VolcanoClient


@dataclass(frozen=True)
class Response:
    status_code: int
    payload: Any = None
    content: bytes = b""
    headers: dict[str, str] | None = None


class StateTransport:
    def __init__(self) -> None:
        self.next_access_token = "access-1"
        self.query_calls: list[dict[str, Any]] = []
        self.authorizations: list[tuple[str, str]] = []

    def auth_signin(self, **kwargs: Any) -> Response:
        self.authorizations.append(("auth", kwargs["authorization"]))
        return Response(
            200,
            {
                "access_token": self.next_access_token,
                "refresh_token": f"refresh-{self.next_access_token}",
                "user": {
                    "id": "user-123",
                    "email": "user@example.com",
                },
            },
        )

    def query_database_select(self, **kwargs: Any) -> Response:
        self.authorizations.append(("query", kwargs["authorization"]))
        self.query_calls.append(kwargs["body"])
        return Response(200, {"data": [kwargs["body"]], "count": 1})

    def upload_storage_object(self, **kwargs: Any) -> Response:
        self.authorizations.append(("upload", kwargs["authorization"]))
        return Response(201, {"name": kwargs["path"]})

    def download_storage_object(self, **kwargs: Any) -> Response:
        self.authorizations.append(("download", kwargs["authorization"]))
        return Response(200, content=b"bytes")

    def acquire_project_lock(self, **kwargs: Any) -> Response:
        self.authorizations.append(("acquire", kwargs["authorization"]))
        return Response(201, {"expires_at": None, "fencing_token": 1})

    def release_project_lock(self, **kwargs: Any) -> Response:
        self.authorizations.append(("release", kwargs["authorization"]))
        return Response(204)


def test_constructor_accepts_an_access_token_only() -> None:
    client = VolcanoClient(anon_key="anon", access_token="access-token")

    assert client.current_session == Session(access_token="access-token")
    assert client.current_user is None


def test_constructor_accepts_an_access_and_refresh_token() -> None:
    client = VolcanoClient(
        anon_key="anon",
        access_token="access-token",
        refresh_token="refresh-token",
    )

    assert client.current_session == Session(
        access_token="access-token",
        refresh_token="refresh-token",
    )
    assert client.current_user is None


def test_session_preserves_the_original_positional_argument_order() -> None:
    session = Session("access-token", "refresh-token", "user-123")

    assert session.user_id == "user-123"
    assert session.expires_in is None


def test_constructor_rejects_a_refresh_token_without_an_access_token() -> None:
    with pytest.raises(
        ValueError,
        match="refresh_token requires access_token",
    ):
        VolcanoClient(anon_key="anon", refresh_token="refresh-token")


def test_constructor_rejects_unknown_authentication_keywords() -> None:
    with pytest.raises(TypeError, match="acess_token"):
        VolcanoClient(anon_key="anon", acess_token="misspelled")  # type: ignore[call-arg]


def test_auth_state_can_be_replaced_and_cleared() -> None:
    client = VolcanoClient(anon_key="anon")
    session = Session(
        access_token="access-token",
        refresh_token="refresh-token",
        expires_in=3600,
        user_id="user-123",
    )
    user = User(id="user-123", email="user@example.com")

    client._commit_auth(session, user)

    assert client.current_session is session
    assert client.current_user is user

    replacement = User(id="user-123", email="updated@example.com")
    client._set_user(replacement)

    assert client.current_session is session
    assert client.current_user is replacement

    client._clear_auth()

    assert client.current_session is None
    assert client.current_user is None


def test_query_builder_chains_are_immutable() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    base = client.database("main").from_("items")
    selected = base.select("*")
    first = selected.eq("slug", "a")
    second = selected.eq("slug", "b")

    first.execute()
    second.execute()

    assert transport.query_calls == [
        {
            "table": "items",
            "filters": [{"column": "slug", "operator": "eq", "value": "a"}],
        },
        {
            "table": "items",
            "filters": [{"column": "slug", "operator": "eq", "value": "b"}],
        },
    ]


def test_each_request_reads_the_current_credentials() -> None:
    transport = StateTransport()
    client = VolcanoClient(
        anon_key="anon-1",
        service_key="service-1",
        _transport=transport,
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    query = client.database("main").from_("items").select("*")
    bucket = client.storage.from_("assets")

    transport.next_access_token = "access-2"
    client._anon_key = "anon-2"
    client.auth.sign_in(email="user@example.com", password="secret")
    query.execute()
    bucket.upload("a.txt", b"bytes")
    bucket.download("a.txt")
    lease = client.locks.acquire("build", ttl=30)
    client._service_key = "service-2"
    client.locks.release("build", lease)

    assert transport.authorizations == [
        ("auth", "anon-1"),
        ("auth", "anon-2"),
        ("query", "access-2"),
        ("upload", "access-2"),
        ("download", "access-2"),
        ("acquire", "service-1"),
        ("release", "service-2"),
    ]
