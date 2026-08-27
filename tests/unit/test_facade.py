from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from volcano_sdk import LockLease, Session, VolcanoClient


@dataclass(frozen=True)
class FakeResponse:
    status_code: int
    payload: Any = None
    content: bytes = b""
    headers: dict[str, str] | None = None


class FakeTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def auth_signin(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("authSignin", kwargs))
        return FakeResponse(
            200,
            {
                "access_token": "access-token",
                "refresh_token": "refresh-token",
                "user": {"id": "user-123"},
            },
        )

    def query_database_select(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("queryDatabaseSelect", kwargs))
        return FakeResponse(200, {"data": [{"slug": "a"}], "count": 1})

    def upload_storage_object(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("uploadStorageObject", kwargs))
        return FakeResponse(201, {"name": "a.txt", "size": 5})

    def download_storage_object(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("downloadStorageObject", kwargs))
        return FakeResponse(200, content=b"hello")

    def acquire_project_lock(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("acquireProjectLock", kwargs))
        return FakeResponse(
            201,
            {"expires_at": "2026-08-26T12:00:30Z", "fencing_token": 7},
        )

    def release_project_lock(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("releaseProjectLock", kwargs))
        return FakeResponse(204)


def test_public_facade_delegates_to_the_six_contract_operations() -> None:
    transport = FakeTransport()
    client = VolcanoClient(
        api_url="https://api.test.volcano.dev",
        anon_key="anon-key",
        service_key="service-key",
        _transport=transport,
    )

    session = client.auth.sign_in(email="user@example.com", password="secret")
    rows = client.database("main").from_("items").select("*").eq("slug", "a").execute()
    uploaded = client.storage.from_("assets").upload("a.txt", b"hello")
    downloaded = client.storage.from_("assets").download("a.txt")
    lease = client.locks.acquire("build", ttl=30)
    client.locks.release("build", lease)

    assert session == Session(
        access_token="access-token",
        refresh_token="refresh-token",
        user_id="user-123",
    )
    assert client.current_session is session
    assert rows == [{"slug": "a"}]
    assert uploaded == {"name": "a.txt", "size": 5}
    assert downloaded == b"hello"
    assert lease == LockLease(
        key="build",
        token=lease.token,
        expires_at=datetime(2026, 8, 26, 12, 0, 30, tzinfo=UTC),
        fencing_token=7,
    )
    assert [name for name, _ in transport.calls] == [
        "authSignin",
        "queryDatabaseSelect",
        "uploadStorageObject",
        "downloadStorageObject",
        "acquireProjectLock",
        "releaseProjectLock",
    ]
    assert transport.calls[0][1] == {
        "authorization": "anon-key",
        "email": "user@example.com",
        "password": "secret",
    }
    assert transport.calls[1][1] == {
        "authorization": "access-token",
        "database_name": "main",
        "body": {
            "table": "items",
            "filters": [{"column": "slug", "operator": "eq", "value": "a"}],
        },
    }
    assert transport.calls[2][1] == {
        "authorization": "access-token",
        "bucket_name": "assets",
        "path": "a.txt",
        "data": b"hello",
    }
    assert transport.calls[3][1] == {
        "authorization": "access-token",
        "bucket_name": "assets",
        "path": "a.txt",
    }
    assert transport.calls[4][1]["authorization"] == "service-key"
    assert transport.calls[4][1]["key"] == "build"
    assert transport.calls[4][1]["ttl"] == 30
    assert transport.calls[4][1]["token"] == lease.token
    assert transport.calls[5][1]["authorization"] == "service-key"
    assert transport.calls[5][1]["key"] == "build"
    assert transport.calls[5][1]["token"] == lease.token
