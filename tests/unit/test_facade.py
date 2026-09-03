from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from io import SEEK_END, BytesIO, StringIO
from typing import Any, BinaryIO, cast

import pytest

from volcano_sdk import (
    LockLease,
    ServerError,
    Session,
    StorageObject,
    StoragePage,
    UploadPart,
    UploadSession,
    UploadSessionStatus,
    VolcanoClient,
)


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
        self.range_download_status = 206
        self.include_upload_session_parts = True
        self.upload_session_part_size = 8_388_608
        self.upload_session_total_parts = 3
        self.fail_upload_part_number: int | None = None
        self.fail_abort_upload = False
        self.raise_abort_error = False

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
        status = self.range_download_status if kwargs.get("byte_range") else 200
        return FakeResponse(status, content=b"hello")

    def create_upload_session(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("createUploadSession", kwargs))
        return FakeResponse(
            201,
            {
                "session_id": "session-123",
                "part_size": self.upload_session_part_size,
                "total_parts": self.upload_session_total_parts,
                "expires_at": "2026-09-09T12:00:00Z",
            },
        )

    def upload_part(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("uploadPart", kwargs))
        request = kwargs["request"]
        if request.part_number == self.fail_upload_part_number:
            return FakeResponse(500, {"error": "part upload failed"})
        return FakeResponse(
            200,
            {
                "part_number": request.part_number,
                "etag": "etag-part-1",
                "size": len(request.data),
            },
        )

    def complete_upload_session(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("completeUploadSession", kwargs))
        request = kwargs["request"]
        return FakeResponse(
            200,
            {
                "object": {
                    "id": "00000000-0000-4000-8000-000000000020",
                    "bucket_id": "00000000-0000-4000-8000-000000000030",
                    "name": request.path,
                    "size": 20_000_000,
                    "mime_type": "video/mp4",
                    "is_public": False,
                    "etag": "etag-complete",
                }
            },
        )

    def get_upload_session(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("getUploadSession", kwargs))
        request = kwargs["request"]
        payload = {
            "session_id": request.session_id,
            "status": "uploading",
            "path": request.path,
            "content_type": "video/mp4",
            "total_size": 20_000_000,
            "part_size": 8_388_608,
            "total_parts": 3,
            "parts_uploaded": 1,
            "bytes_uploaded": 8_388_608,
            "expires_at": "2026-09-09T12:00:00Z",
            "created_at": "2026-09-02T12:00:00Z",
        }
        if self.include_upload_session_parts:
            payload["parts"] = [
                {
                    "part_number": 1,
                    "etag": "etag-part-1",
                    "size": 8_388_608,
                }
            ]
        return FakeResponse(200, payload)

    def abort_upload_session(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("abortUploadSession", kwargs))
        if self.raise_abort_error:
            msg = "abort transport failed"
            raise RuntimeError(msg)
        if self.fail_abort_upload:
            return FakeResponse(500, {"error": "abort failed"})
        return FakeResponse(200, {"message": "upload session aborted"})

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

    def get_project_lock(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("getProjectLock", kwargs))
        return FakeResponse(
            200,
            {
                "held": True,
                "expires_at": "2026-08-26T12:00:30Z",
                "fencing_token": 7,
            },
        )

    def renew_project_lock(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("renewProjectLock", kwargs))
        return FakeResponse(
            200,
            {"expires_at": "2026-08-26T12:01:00Z", "fencing_token": 7},
        )

    def force_release_project_lock(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("forceReleaseProjectLock", kwargs))
        return FakeResponse(204)


class BoundedBytesIO(BytesIO):
    def __init__(self, value: bytes) -> None:
        super().__init__(value)
        self.read_sizes: list[int] = []

    def read(self, size: int | None = -1) -> bytes:
        if size is None or size < 0:
            msg = "unbounded read"
            raise RuntimeError(msg)
        self.read_sizes.append(size)
        return super().read(size)


class ShortReadBytesIO(BoundedBytesIO):
    def read(self, size: int | None = -1) -> bytes:
        if size is None or size < 0:
            msg = "unbounded read"
            raise RuntimeError(msg)
        return super().read(min(size, 2))


class BoundedNonSeekableReader:
    def __init__(self, value: bytes) -> None:
        self._value = value
        self._offset = 0
        self.read_sizes: list[int] = []

    def read(self, size: int = -1) -> bytes:
        if size < 0:
            msg = "unbounded read"
            raise RuntimeError(msg)
        self.read_sizes.append(size)
        chunk = self._value[self._offset : self._offset + size]
        self._offset += len(chunk)
        return chunk

    def seekable(self) -> bool:
        return False


class TemporarilyUnavailableReader:
    def __init__(self) -> None:
        self.read_sizes: list[int] = []

    def read(self, size: int = -1) -> bytes | None:
        if not self.read_sizes:
            self.read_sizes.append(size)
            return None
        return b""

    def seekable(self) -> bool:
        return False


class ReadOnlyStream:
    def __init__(self, value: bytes) -> None:
        self._source = BytesIO(value)

    def read(self, size: int = -1) -> bytes:
        return self._source.read(size)


class FailingSeekableReader(BoundedBytesIO):
    def read(self, size: int | None = -1) -> bytes:
        if self.tell() >= 4:
            msg = "reader failed"
            raise RuntimeError(msg)
        return super().read(size)


class RestoreFailingBytesIO(BytesIO):
    def __init__(self, value: bytes) -> None:
        super().__init__(value)
        self._end_was_probed = False

    def seek(self, offset: int, whence: int = 0) -> int:
        if self._end_was_probed and whence == 0:
            msg = "restore failed"
            raise OSError(msg)
        position = super().seek(offset, whence)
        if whence == SEEK_END:
            self._end_was_probed = True
        return position


def anon_key_with_project_id(project_id: str | None) -> str:
    payload = {} if project_id is None else {"project_id": project_id}
    encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b"=")
    return f"header.{encoded.decode()}.signature"


def signed_in_client(transport: FakeTransport) -> VolcanoClient:
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    return client


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
    downloaded = client.storage.from_("assets").download(
        "a.txt",
        byte_range="bytes=0-4",
    )
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
        "byte_range": "bytes=0-4",
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


def test_storage_upload_reads_a_caller_owned_binary_stream_from_its_position() -> None:
    transport = FakeTransport()
    client = signed_in_client(transport)
    source = BytesIO(b"skip-uploaded")
    source.seek(5)

    client.storage.from_("assets").upload("a.txt", source)

    assert not source.closed
    assert source.tell() == len(b"skip-uploaded")
    assert transport.calls[-1] == (
        "uploadStorageObject",
        {
            "authorization": "access-token",
            "bucket_name": "assets",
            "path": "a.txt",
            "data": b"uploaded",
        },
    )


def test_storage_upload_rejects_text_streams_before_transport() -> None:
    transport = FakeTransport()
    client = signed_in_client(transport)

    with pytest.raises(TypeError, match="binary"):
        client.storage.from_("assets").upload(
            "a.txt",
            cast("BinaryIO", StringIO("text")),
        )

    assert all(operation != "uploadStorageObject" for operation, _ in transport.calls)


def test_storage_upload_reports_temporarily_unavailable_streams() -> None:
    transport = FakeTransport()
    client = signed_in_client(transport)

    with pytest.raises(BlockingIOError, match="temporarily unavailable"):
        client.storage.from_("assets").upload(
            "a.txt",
            cast("BinaryIO", TemporarilyUnavailableReader()),
        )

    assert all(operation != "uploadStorageObject" for operation, _ in transport.calls)


def test_storage_list_normalizes_an_empty_terminal_cursor() -> None:
    transport = FakeTransport()
    transport.list_cursor = ""
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    assert client.storage.from_("assets").list().next_cursor is None


def test_locks_gets_immutable_current_state() -> None:
    transport = FakeTransport()
    client = VolcanoClient(
        anon_key="anon-key",
        service_key="service-key",
        _transport=transport,
    )

    state = client.locks.get("build")

    assert type(state).__name__ == "LockState"
    assert (state.held, state.expires_at, state.fencing_token) == (
        True,
        datetime(2026, 8, 26, 12, 0, 30, tzinfo=UTC),
        7,
    )
    assert transport.calls == [
        (
            "getProjectLock",
            {"authorization": "service-key", "key": "build"},
        )
    ]


def test_locks_renews_a_lease_without_mutating_the_original() -> None:
    transport = FakeTransport()
    client = VolcanoClient(
        anon_key="anon-key",
        service_key="service-key",
        _transport=transport,
    )
    lease = LockLease(
        key="build",
        token="00000000-0000-4000-8000-000000000001",
        expires_at=datetime(2026, 8, 26, 12, 0, 30, tzinfo=UTC),
        fencing_token=7,
    )

    renewed = client.locks.renew("build", lease, ttl=60)

    assert renewed == LockLease(
        key="build",
        token=lease.token,
        expires_at=datetime(2026, 8, 26, 12, 1, tzinfo=UTC),
        fencing_token=7,
    )
    assert lease.expires_at == datetime(2026, 8, 26, 12, 0, 30, tzinfo=UTC)
    assert transport.calls == [
        (
            "renewProjectLock",
            {
                "authorization": "service-key",
                "key": "build",
                "ttl": 60,
                "token": lease.token,
            },
        )
    ]


@pytest.mark.parametrize("ttl", [4, 7_776_001, 5.5, "5", True])
def test_locks_rejects_invalid_acquisition_ttl(ttl: object) -> None:
    transport = FakeTransport()
    client = VolcanoClient(
        anon_key="anon-key",
        service_key="service-key",
        _transport=transport,
    )

    with pytest.raises(ValueError, match="between 5 seconds and 90 days"):
        client.locks.acquire("build", ttl=cast("int", ttl))

    assert transport.calls == []


@pytest.mark.parametrize("ttl", [4, 7_776_001, 5.5, "5", True])
def test_locks_rejects_invalid_renewal_ttl(ttl: object) -> None:
    transport = FakeTransport()
    client = VolcanoClient(
        anon_key="anon-key",
        service_key="service-key",
        _transport=transport,
    )
    lease = LockLease(
        key="build",
        token="00000000-0000-4000-8000-000000000001",
        expires_at=datetime(2026, 8, 26, 12, 0, 30, tzinfo=UTC),
        fencing_token=7,
    )

    with pytest.raises(ValueError, match="between 5 seconds and 90 days"):
        client.locks.renew("build", lease, ttl=cast("int", ttl))

    assert transport.calls == []


def test_locks_force_releases_without_an_ownership_token() -> None:
    transport = FakeTransport()
    client = VolcanoClient(
        anon_key="anon-key",
        service_key="service-key",
        _transport=transport,
    )

    client.locks.force_release("build")

    assert transport.calls == [
        (
            "forceReleaseProjectLock",
            {"authorization": "service-key", "key": "build"},
        )
    ]


def test_storage_remove_accepts_one_path() -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    assert client.storage.from_("assets").remove("archive/a.txt") == ("archive/a.txt",)


def test_storage_download_accepts_a_full_response_when_range_is_ignored() -> None:
    transport = FakeTransport()
    transport.range_download_status = 200
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    downloaded = client.storage.from_("assets").download(
        "a.txt",
        byte_range="bytes=0-4",
    )

    assert downloaded == b"hello"


def test_storage_creates_an_immutable_upload_session() -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    session = client.storage.from_("assets").create_upload_session(
        "videos/demo.mp4",
        total_size=20_000_000,
        content_type="video/mp4",
        part_size=8_388_608,
    )

    assert session == UploadSession(
        session_id="session-123",
        part_size=8_388_608,
        total_parts=3,
        expires_at=datetime(2026, 9, 9, 12, 0, tzinfo=UTC),
    )
    operation, arguments = transport.calls[-1]
    assert operation == "createUploadSession"
    assert arguments["authorization"] == "access-token"
    assert arguments["bucket_name"] == "assets"
    request = arguments["request"]
    assert (
        request.path,
        request.content_type,
        request.total_size,
        request.part_size,
    ) == ("videos/demo.mp4", "video/mp4", 20_000_000, 8_388_608)


def test_storage_uploads_a_part_and_returns_immutable_metadata() -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    part = client.storage.from_("assets").upload_part(
        "videos/demo.mp4",
        session_id="session-123",
        part_number=1,
        data=b"chunk\x00",
    )

    assert part == UploadPart(part_number=1, etag="etag-part-1", size=6)
    operation, arguments = transport.calls[-1]
    assert operation == "uploadPart"
    request = arguments["request"]
    assert (request.path, request.session_id, request.part_number, request.data) == (
        "videos/demo.mp4",
        "session-123",
        1,
        b"chunk\x00",
    )


def test_storage_completes_an_upload_session_and_returns_the_object() -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    object_ = client.storage.from_("assets").complete_upload_session(
        "videos/demo.mp4",
        session_id="session-123",
    )

    assert object_ == StorageObject(
        id="00000000-0000-4000-8000-000000000020",
        bucket_id="00000000-0000-4000-8000-000000000030",
        name="videos/demo.mp4",
        size=20_000_000,
        mime_type="video/mp4",
        is_public=False,
        etag="etag-complete",
    )
    operation, arguments = transport.calls[-1]
    assert operation == "completeUploadSession"
    assert arguments["authorization"] == "access-token"
    assert arguments["bucket_name"] == "assets"
    request = arguments["request"]
    assert (request.path, request.session_id) == (
        "videos/demo.mp4",
        "session-123",
    )


def test_storage_gets_immutable_upload_session_status() -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    status = client.storage.from_("assets").get_upload_session(
        "videos/demo.mp4",
        session_id="session-123",
    )

    assert status == UploadSessionStatus(
        session_id="session-123",
        status="uploading",
        path="videos/demo.mp4",
        content_type="video/mp4",
        total_size=20_000_000,
        part_size=8_388_608,
        total_parts=3,
        parts_uploaded=1,
        bytes_uploaded=8_388_608,
        parts=(UploadPart(part_number=1, etag="etag-part-1", size=8_388_608),),
        expires_at=datetime(2026, 9, 9, 12, 0, tzinfo=UTC),
        created_at=datetime(2026, 9, 2, 12, 0, tzinfo=UTC),
    )
    operation, arguments = transport.calls[-1]
    assert operation == "getUploadSession"
    assert arguments["authorization"] == "access-token"
    assert arguments["bucket_name"] == "assets"
    request = arguments["request"]
    assert (request.path, request.session_id) == (
        "videos/demo.mp4",
        "session-123",
    )


def test_storage_defaults_omitted_upload_parts_to_an_empty_snapshot() -> None:
    transport = FakeTransport()
    transport.include_upload_session_parts = False
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    status = client.storage.from_("assets").get_upload_session(
        "videos/demo.mp4",
        session_id="session-123",
    )

    assert status.parts == ()


def test_storage_aborts_an_upload_session() -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    client.storage.from_("assets").abort_upload_session(
        "videos/demo.mp4",
        session_id="session-123",
    )

    operation, arguments = transport.calls[-1]
    assert operation == "abortUploadSession"
    assert arguments["authorization"] == "access-token"
    assert arguments["bucket_name"] == "assets"
    request = arguments["request"]
    assert (request.path, request.session_id) == (
        "videos/demo.mp4",
        "session-123",
    )


def test_storage_uploads_bytes_with_server_selected_chunks() -> None:
    transport = FakeTransport()
    transport.upload_session_part_size = 4
    transport.upload_session_total_parts = 3
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    object_ = client.storage.from_("assets").upload_resumable(
        "videos/demo.mp4",
        b"abcdefghij",
        content_type="video/mp4",
        part_size=6,
    )

    storage_calls = transport.calls[1:]
    assert [operation for operation, _ in storage_calls] == [
        "createUploadSession",
        "uploadPart",
        "uploadPart",
        "uploadPart",
        "completeUploadSession",
    ]
    create_request = storage_calls[0][1]["request"]
    assert (create_request.total_size, create_request.part_size) == (10, 6)
    assert [call[1]["request"].data for call in storage_calls[1:4]] == [
        b"abcd",
        b"efgh",
        b"ij",
    ]
    assert object_.name == "videos/demo.mp4"


def test_storage_reports_progress_after_each_uploaded_part() -> None:
    transport = FakeTransport()
    transport.upload_session_part_size = 4
    transport.upload_session_total_parts = 3
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    progress: list[tuple[int, int]] = []

    client.storage.from_("assets").upload_resumable(
        "file.bin",
        b"abcdefghij",
        on_progress=lambda uploaded, total: progress.append((uploaded, total)),
    )

    assert progress == [(4, 10), (8, 10), (10, 10)]


def test_storage_aborts_when_a_progress_callback_fails() -> None:
    transport = FakeTransport()
    transport.upload_session_part_size = 4
    transport.upload_session_total_parts = 2
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    def fail_progress(_uploaded: int, _total: int) -> None:
        message = "progress failed"
        raise RuntimeError(message)

    with pytest.raises(RuntimeError, match="progress failed"):
        client.storage.from_("assets").upload_resumable(
            "file.bin",
            b"abcdefgh",
            on_progress=fail_progress,
        )

    assert [operation for operation, _ in transport.calls[-2:]] == [
        "uploadPart",
        "abortUploadSession",
    ]


def test_storage_aborts_after_part_failure_without_masking_the_error() -> None:
    transport = FakeTransport()
    transport.upload_session_part_size = 4
    transport.upload_session_total_parts = 2
    transport.fail_upload_part_number = 2
    transport.fail_abort_upload = True
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    with pytest.raises(ServerError, match="part upload failed") as raised:
        client.storage.from_("assets").upload_resumable("file.bin", b"abcdefgh")

    assert getattr(raised.value, "status", None) == 500
    assert [operation for operation, _ in transport.calls[1:]] == [
        "createUploadSession",
        "uploadPart",
        "uploadPart",
        "abortUploadSession",
    ]


def test_storage_streams_seekable_uploads_with_server_selected_reads() -> None:
    transport = FakeTransport()
    transport.upload_session_part_size = 4
    transport.upload_session_total_parts = 3
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    source = BoundedBytesIO(b"abcdefghij")

    client.storage.from_("assets").upload_resumable("file.bin", source)

    assert source.read_sizes
    assert max(source.read_sizes) <= 4
    upload_calls = [call for call in transport.calls if call[0] == "uploadPart"]
    assert [call[1]["request"].data for call in upload_calls] == [
        b"abcd",
        b"efgh",
        b"ij",
    ]


def test_storage_clamps_a_seekable_source_positioned_past_eof() -> None:
    transport = FakeTransport()
    transport.upload_session_total_parts = 0
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    source = BytesIO(b"a")
    source.seek(2)

    client.storage.from_("assets").upload_resumable("file.bin", source)

    create_call = next(
        call for call in transport.calls if call[0] == "createUploadSession"
    )
    assert create_call[1]["request"].total_size == 0


def test_storage_surfaces_a_failed_seekable_position_restore() -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    with pytest.raises(OSError, match="restore failed"):
        client.storage.from_("assets").upload_resumable(
            "file.bin",
            RestoreFailingBytesIO(b"abcdefgh"),
        )

    assert all(operation != "createUploadSession" for operation, _ in transport.calls)


def test_storage_fills_parts_when_a_seekable_source_returns_short_reads() -> None:
    transport = FakeTransport()
    transport.upload_session_part_size = 4
    transport.upload_session_total_parts = 3
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    client.storage.from_("assets").upload_resumable(
        "file.bin",
        ShortReadBytesIO(b"abcdefghij"),
    )

    upload_calls = [call for call in transport.calls if call[0] == "uploadPart"]
    assert [call[1]["request"].data for call in upload_calls] == [
        b"abcd",
        b"efgh",
        b"ij",
    ]


def test_storage_spools_non_seekable_uploads_with_bounded_reads() -> None:
    transport = FakeTransport()
    transport.upload_session_part_size = 4
    transport.upload_session_total_parts = 3
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    source = BoundedNonSeekableReader(b"abcdefghij")

    client.storage.from_("assets").upload_resumable(
        "file.bin",
        cast("BinaryIO", source),
    )

    assert source.read_sizes
    assert max(source.read_sizes) <= 1_048_576
    upload_calls = [call for call in transport.calls if call[0] == "uploadPart"]
    assert [call[1]["request"].data for call in upload_calls] == [
        b"abcd",
        b"efgh",
        b"ij",
    ]


def test_storage_spools_read_only_streams_without_a_seekability_probe() -> None:
    transport = FakeTransport()
    transport.upload_session_part_size = 4
    transport.upload_session_total_parts = 2
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    client.storage.from_("assets").upload_resumable(
        "file.bin",
        cast("BinaryIO", ReadOnlyStream(b"abcdefgh")),
    )

    upload_calls = [call for call in transport.calls if call[0] == "uploadPart"]
    assert [call[1]["request"].data for call in upload_calls] == [b"abcd", b"efgh"]


def test_storage_aborts_when_a_stream_reader_raises_an_unexpected_error() -> None:
    transport = FakeTransport()
    transport.upload_session_part_size = 4
    transport.upload_session_total_parts = 2
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    with pytest.raises(RuntimeError, match="reader failed"):
        client.storage.from_("assets").upload_resumable(
            "file.bin",
            FailingSeekableReader(b"abcdefgh"),
        )

    assert [operation for operation, _ in transport.calls[-2:]] == [
        "uploadPart",
        "abortUploadSession",
    ]


def test_storage_preserves_reader_error_when_abort_cleanup_raises() -> None:
    transport = FakeTransport()
    transport.upload_session_part_size = 4
    transport.upload_session_total_parts = 2
    transport.raise_abort_error = True
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    with pytest.raises(RuntimeError, match="reader failed"):
        client.storage.from_("assets").upload_resumable(
            "file.bin",
            FailingSeekableReader(b"abcdefgh"),
        )


def test_storage_rejects_temporarily_unavailable_nonblocking_sources() -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    source = TemporarilyUnavailableReader()

    with pytest.raises(BlockingIOError, match="temporarily unavailable"):
        client.storage.from_("assets").upload_resumable(
            "file.bin",
            cast("BinaryIO", source),
        )

    assert all(operation != "createUploadSession" for operation, _ in transport.calls)


def test_storage_validates_authentication_before_spooling() -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    source = BoundedNonSeekableReader(b"abcdefghij")

    with pytest.raises(RuntimeError, match="active session"):
        client.storage.from_("assets").upload_resumable(
            "file.bin",
            cast("BinaryIO", source),
        )

    assert source.read_sizes == []


def test_storage_validates_path_before_spooling() -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    source = BoundedNonSeekableReader(b"abcdefghij")

    with pytest.raises(ValueError, match="non-empty string"):
        client.storage.from_("assets").upload_resumable(
            "",
            cast("BinaryIO", source),
        )

    assert source.read_sizes == []


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

    with pytest.raises(ValueError, match="non-empty string"):
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


def test_storage_get_public_url_rejects_multiple_paths() -> None:
    transport = FakeTransport()
    client = VolcanoClient(
        anon_key=anon_key_with_project_id("project-123"),
        _transport=transport,
    )
    paths: Any = ["first.txt", "second.txt"]

    with pytest.raises(TypeError, match="non-empty string"):
        client.storage.from_("assets").get_public_url(paths)

    assert transport.calls == []
