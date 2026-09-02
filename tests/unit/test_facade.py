from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import pytest

from volcano_sdk import LockLease, Session, StorageObject, StoragePage, VolcanoClient


@dataclass(frozen=True)
class FakeResponse:
    status_code: int
    payload: Any = None
    content: bytes = b""
    headers: dict[str, str] | None = None


class FakeTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.list_cursor = "cursor-2"

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

    def query_database_insert(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("queryDatabaseInsert", kwargs))
        return FakeResponse(200, {"data": [{"slug": "new"}], "count": 1})

    def query_database_update(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("queryDatabaseUpdate", kwargs))
        return FakeResponse(200, {"data": [{"slug": "updated"}], "count": 1})

    def query_database_delete(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("queryDatabaseDelete", kwargs))
        return FakeResponse(200, {"data": [{"slug": "updated"}], "count": 1})

    def upload_storage_object(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("uploadStorageObject", kwargs))
        return FakeResponse(201, {"name": "a.txt", "size": 5})

    def download_storage_object(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("downloadStorageObject", kwargs))
        return FakeResponse(200, content=b"hello")

    def list_storage_objects(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("listStorageObjects", kwargs))
        return FakeResponse(
            200,
            {
                "objects": [
                    {
                        "id": "00000000-0000-4000-8000-000000000020",
                        "bucket_id": "00000000-0000-4000-8000-000000000030",
                        "name": "avatars/a.png",
                        "size": 5,
                        "mime_type": "image/png",
                        "is_public": False,
                        "owner_id": "00000000-0000-4000-8000-000000000010",
                        "etag": "etag-1",
                        "metadata": {"width": 32, "labels": ["profile"]},
                        "created_at": "2026-08-26T12:00:00Z",
                        "updated_at": "2026-08-26T12:01:00Z",
                    }
                ],
                "next_cursor": self.list_cursor,
            },
        )

    def delete_storage_object(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("deleteStorageObject", kwargs))
        return FakeResponse(200)

    def move_storage_object(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("moveStorageObject", kwargs))
        return FakeResponse(
            200,
            {
                "id": "00000000-0000-4000-8000-000000000020",
                "bucket_id": "00000000-0000-4000-8000-000000000030",
                "name": kwargs["to_path"],
                "size": 5,
                "mime_type": "text/plain",
                "is_public": False,
            },
        )

    def copy_storage_object(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("copyStorageObject", kwargs))
        return FakeResponse(
            201,
            {
                "id": "00000000-0000-4000-8000-000000000021",
                "bucket_id": "00000000-0000-4000-8000-000000000030",
                "name": kwargs["to_path"],
                "size": 5,
                "mime_type": "text/plain",
                "is_public": False,
            },
        )

    def update_storage_object_visibility(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("updateStorageObjectVisibility", kwargs))
        return FakeResponse(
            200,
            {
                "id": "00000000-0000-4000-8000-000000000020",
                "bucket_id": "00000000-0000-4000-8000-000000000030",
                "name": kwargs["path"],
                "size": 5,
                "mime_type": "image/png",
                "is_public": kwargs["is_public"],
                "public_url": (
                    "https://api.test.volcano.dev/public/project/assets/avatars/a.png"
                    if kwargs["is_public"]
                    else None
                ),
            },
        )

    def acquire_project_lock(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("acquireProjectLock", kwargs))
        return FakeResponse(
            201,
            {"expires_at": "2026-08-26T12:00:30Z", "fencing_token": 7},
        )

    def release_project_lock(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("releaseProjectLock", kwargs))
        return FakeResponse(204)


def anon_key_with_project_id(project_id: str | None) -> str:
    payload = {} if project_id is None else {"project_id": project_id}
    encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b"=")
    return f"header.{encoded.decode()}.signature"


def test_public_facade_delegates_to_the_contract_operations() -> None:
    transport = FakeTransport()
    client = VolcanoClient(
        api_url="https://api.test.volcano.dev",
        anon_key="anon-key",
        service_key="service-key",
        _transport=transport,
    )

    session = client.auth.sign_in(email="user@example.com", password="secret")
    rows = client.database("main").from_("items").select("*").eq("slug", "a").execute()
    inserted = client.database("main").from_("items").insert({"slug": "new"}).execute()
    updated = (
        client.database("main")
        .from_("items")
        .update({"slug": "updated"})
        .eq("slug", "new")
        .execute()
    )
    deleted = (
        client.database("main").from_("items").delete().eq("slug", "updated").execute()
    )
    uploaded = client.storage.from_("assets").upload("a.txt", b"hello")
    downloaded = client.storage.from_("assets").download("a.txt")
    page = client.storage.from_("assets").list(
        "avatars",
        limit=25,
        cursor="cursor-1",
    )
    removed = client.storage.from_("assets").remove(["archive/a.txt", "archive/b.txt"])
    lease = client.locks.acquire("build", ttl=30)
    client.locks.release("build", lease)

    assert session == Session(
        access_token="access-token",
        refresh_token="refresh-token",
        user_id="user-123",
    )
    assert client.current_session is session
    assert rows == [{"slug": "a"}]
    assert inserted == [{"slug": "new"}]
    assert updated == [{"slug": "updated"}]
    assert deleted == [{"slug": "updated"}]
    assert uploaded == {"name": "a.txt", "size": 5}
    assert downloaded == b"hello"
    assert page == StoragePage(
        objects=(
            StorageObject(
                id="00000000-0000-4000-8000-000000000020",
                bucket_id="00000000-0000-4000-8000-000000000030",
                name="avatars/a.png",
                size=5,
                mime_type="image/png",
                is_public=False,
                owner_id="00000000-0000-4000-8000-000000000010",
                etag="etag-1",
                metadata={"width": 32, "labels": ["profile"]},
                created_at=datetime(2026, 8, 26, 12, 0, tzinfo=UTC),
                updated_at=datetime(2026, 8, 26, 12, 1, tzinfo=UTC),
            ),
        ),
        next_cursor="cursor-2",
    )
    assert page.objects[0].metadata == {"width": 32, "labels": ("profile",)}
    assert removed == ("archive/a.txt", "archive/b.txt")
    assert lease == LockLease(
        key="build",
        token=lease.token,
        expires_at=datetime(2026, 8, 26, 12, 0, 30, tzinfo=UTC),
        fencing_token=7,
    )
    assert [name for name, _ in transport.calls] == [
        "authSignin",
        "queryDatabaseSelect",
        "queryDatabaseInsert",
        "queryDatabaseUpdate",
        "queryDatabaseDelete",
        "uploadStorageObject",
        "downloadStorageObject",
        "listStorageObjects",
        "deleteStorageObject",
        "deleteStorageObject",
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
        "database_name": "main",
        "body": {"table": "items", "values": {"slug": "new"}},
    }
    assert transport.calls[3][1] == {
        "authorization": "access-token",
        "database_name": "main",
        "body": {
            "table": "items",
            "values": {"slug": "updated"},
            "filters": [{"column": "slug", "operator": "eq", "value": "new"}],
        },
    }
    assert transport.calls[4][1] == {
        "authorization": "access-token",
        "database_name": "main",
        "body": {
            "table": "items",
            "filters": [{"column": "slug", "operator": "eq", "value": "updated"}],
        },
    }
    assert transport.calls[5][1] == {
        "authorization": "access-token",
        "bucket_name": "assets",
        "path": "a.txt",
        "data": b"hello",
    }
    assert transport.calls[6][1] == {
        "authorization": "access-token",
        "bucket_name": "assets",
        "path": "a.txt",
    }
    assert transport.calls[7][1] == {
        "authorization": "access-token",
        "bucket_name": "assets",
        "prefix": "avatars",
        "limit": 25,
        "cursor": "cursor-1",
    }
    assert [call[1] for call in transport.calls[8:10]] == [
        {
            "authorization": "access-token",
            "bucket_name": "assets",
            "path": "archive/a.txt",
        },
        {
            "authorization": "access-token",
            "bucket_name": "assets",
            "path": "archive/b.txt",
        },
    ]
    assert transport.calls[10][1]["authorization"] == "service-key"
    assert transport.calls[10][1]["key"] == "build"
    assert transport.calls[10][1]["ttl"] == 30
    assert transport.calls[10][1]["token"] == lease.token
    assert transport.calls[11][1]["authorization"] == "service-key"
    assert transport.calls[11][1]["key"] == "build"
    assert transport.calls[11][1]["token"] == lease.token


def test_storage_list_normalizes_an_empty_terminal_cursor() -> None:
    transport = FakeTransport()
    transport.list_cursor = ""
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    assert client.storage.from_("assets").list().next_cursor is None


def test_storage_remove_accepts_one_path() -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    assert client.storage.from_("assets").remove("archive/a.txt") == ("archive/a.txt",)


@pytest.mark.parametrize("invalid_paths", [[], [""], b"abc"])
def test_storage_remove_rejects_invalid_paths_before_transport(
    invalid_paths: Any,
) -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    calls_after_sign_in = transport.calls.copy()

    with pytest.raises((TypeError, ValueError), match="non-empty strings"):
        client.storage.from_("assets").remove(invalid_paths)

    assert transport.calls == calls_after_sign_in


def test_storage_move_returns_the_destination_object() -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    moved = client.storage.from_("assets").move(
        "drafts/a.txt",
        "published/a.txt",
    )

    assert moved.name == "published/a.txt"
    assert transport.calls[-1] == (
        "moveStorageObject",
        {
            "authorization": "access-token",
            "bucket_name": "assets",
            "from_path": "drafts/a.txt",
            "to_path": "published/a.txt",
        },
    )


def test_storage_copy_returns_the_destination_object() -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    copied = client.storage.from_("assets").copy(
        "templates/a.txt",
        "drafts/a.txt",
    )

    assert copied.name == "drafts/a.txt"
    assert transport.calls[-1][0] == "copyStorageObject"
    assert transport.calls[-1][1]["from_path"] == "templates/a.txt"
    assert transport.calls[-1][1]["to_path"] == "drafts/a.txt"


def test_storage_update_visibility_returns_server_confirmed_metadata() -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    updated = client.storage.from_("assets").update_visibility(
        "avatars/a.png",
        is_public=True,
    )

    assert updated.is_public is True
    assert updated.public_url == (
        "https://api.test.volcano.dev/public/project/assets/avatars/a.png"
    )
    assert transport.calls[-1] == (
        "updateStorageObjectVisibility",
        {
            "authorization": "access-token",
            "bucket_name": "assets",
            "path": "avatars/a.png",
            "is_public": True,
        },
    )


@pytest.mark.parametrize(
    ("path", "is_public"),
    [("", True), ("avatars/a.png", 1), ("avatars/a.png", "true")],
)
def test_storage_update_visibility_rejects_invalid_input_before_transport(
    path: str,
    is_public: Any,
) -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    calls_after_sign_in = transport.calls.copy()

    with pytest.raises((TypeError, ValueError)):
        client.storage.from_("assets").update_visibility(
            path,
            is_public=is_public,
        )

    assert transport.calls == calls_after_sign_in


def test_storage_get_public_url_encodes_path_segments_without_a_request() -> None:
    transport = FakeTransport()
    client = VolcanoClient(
        api_url="https://api.test.volcano.dev/",
        anon_key=anon_key_with_project_id("project-123"),
        _transport=transport,
    )

    public_url = client.storage.from_("assets").get_public_url(
        "avatars/Ada photo.png",
    )

    assert public_url == (
        "https://api.test.volcano.dev/public/project-123/assets/avatars/Ada%20photo.png"
    )
    assert transport.calls == []


@pytest.mark.parametrize(
    "anon_key",
    ["not-a-jwt", anon_key_with_project_id(None), "header.%%%.signature"],
)
def test_storage_get_public_url_rejects_invalid_anon_keys(anon_key: str) -> None:
    client = VolcanoClient(anon_key=anon_key, _transport=FakeTransport())

    with pytest.raises(ValueError, match="project ID"):
        client.storage.from_("assets").get_public_url("avatars/a.png")


def test_storage_get_public_url_rejects_an_empty_path() -> None:
    transport = FakeTransport()
    client = VolcanoClient(
        anon_key=anon_key_with_project_id("project-123"),
        _transport=transport,
    )

    with pytest.raises(ValueError, match="non-empty strings"):
        client.storage.from_("assets").get_public_url("")

    assert transport.calls == []


@pytest.mark.parametrize("path", [".", "avatars/../secret.txt"])
def test_storage_get_public_url_rejects_dot_segments(path: str) -> None:
    transport = FakeTransport()
    client = VolcanoClient(
        anon_key=anon_key_with_project_id("project-123"),
        _transport=transport,
    )

    with pytest.raises(ValueError, match="dot segments"):
        client.storage.from_("assets").get_public_url(path)

    assert transport.calls == []
