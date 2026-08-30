from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from volcano_sdk import Session, VolcanoClient


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
                "user": {"id": "user-123"},
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


def test_auth_facade_reads_an_empty_session_without_transport() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    assert client.auth.get_session() is None
    assert transport.authorizations == []


def test_auth_facade_reads_established_immutable_session_without_transport() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")
    calls_after_sign_in = list(transport.authorizations)

    current = client.auth.get_session()

    assert current is established
    assert current == Session(
        access_token="access-1",
        refresh_token="refresh-access-1",
        user_id="user-123",
    )
    assert transport.authorizations == calls_after_sign_in


def test_auth_facade_adopts_an_owned_session_without_transport() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    supplied = Session(
        access_token="adopted-access",
        refresh_token="adopted-refresh",
        user_id="adopted-user",
    )

    adopted = client.auth.set_session(supplied)

    assert adopted == supplied
    assert adopted is not supplied
    assert client.auth.get_session() is adopted
    assert transport.authorizations == []


def test_auth_facade_adoption_replaces_the_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    replacement = Session(
        access_token="replacement-access",
        refresh_token="replacement-refresh",
        user_id="replacement-user",
    )
    calls_after_sign_in = list(transport.authorizations)

    adopted = client.auth.set_session(replacement)

    assert client.auth.get_session() is adopted
    assert adopted == replacement
    assert transport.authorizations == calls_after_sign_in


@pytest.mark.parametrize(
    "invalid",
    [
        object(),
        Session(access_token=" ", refresh_token="refresh", user_id="user"),
        Session(access_token="access", refresh_token="\t", user_id="user"),
        Session(access_token="access", refresh_token="refresh", user_id="\n"),
    ],
)
def test_auth_facade_rejects_incomplete_adoption_without_mutation(invalid: Any) -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    previous = client.auth.sign_in(email="user@example.com", password="secret")
    calls_after_sign_in = list(transport.authorizations)

    with pytest.raises(ValueError, match="complete Session"):
        client.auth.set_session(invalid)

    assert client.auth.get_session() is previous
    assert transport.authorizations == calls_after_sign_in
