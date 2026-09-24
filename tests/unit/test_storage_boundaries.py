from __future__ import annotations

from datetime import UTC, datetime
from io import SEEK_END, BufferedReader, BytesIO, RawIOBase
from typing import TYPE_CHECKING, cast

import pytest
from transport_fixtures import RejectingTransport
from typing_extensions import override

from volcano_sdk import VolcanoClient
from volcano_sdk.storage import (
    _has_seekable_methods,
    _optional_datetime,
    _read_upload_part,
    _remaining_upload_bytes,
    _resumable_upload_source,
    _simple_upload_bytes,
    _spool_upload_source,
    _storage_object,
    _storage_page,
    _storage_paths,
    _upload_part,
    _upload_session,
    _upload_session_status,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from volcano_sdk.storage import StorageBucket


class EndOfUploadSource:
    """Record the terminal read and fail if an upload retries EOF."""

    def __init__(self) -> None:
        self.sizes: list[int] = []

    def read(self, size: int = -1, /) -> bytes:
        if self.sizes:
            message = "upload source read after end of stream"
            raise AssertionError(message)
        self.sizes.append(size)
        return b""


@pytest.mark.order(0)
def test_upload_part_stops_reading_at_end_of_stream() -> None:
    source = EndOfUploadSource()

    assert _read_upload_part(source, 4) == b""
    assert source.sizes == [4]


class UnavailableRawStream(RawIOBase):
    @override
    def readable(self) -> bool:
        return True

    @override
    def readinto(self, _buffer: object) -> int | None:
        return None


class EndSeekFailure(BytesIO):
    @override
    def seek(self, offset: int, whence: int = 0) -> int:
        if whence == SEEK_END:
            message = "size unavailable"
            raise OSError(message)
        return super().seek(offset, whence)


class SeekLookupFailure(BytesIO):
    @override
    def __getattribute__(self, name: str) -> object:
        if name in {"seekable", "tell", "seek"}:
            message = "seek capability unavailable"
            raise OSError(message)
        return cast("object", super().__getattribute__(name))


class ReadOnlyBinaryInput:
    def read(self, size: int = -1, /) -> bytes:
        del size
        return b""


_STORAGE_OPERATIONS: tuple[Callable[[StorageBucket], object], ...] = (
    lambda bucket: bucket.create_upload_session("file.bin", total_size=0),
    lambda bucket: bucket.upload_part(
        "file.bin", session_id="session", part_number=1, data=b"x"
    ),
    lambda bucket: bucket.complete_upload_session("file.bin", session_id="session"),
    lambda bucket: bucket.get_upload_session("file.bin", session_id="session"),
    lambda bucket: bucket.abort_upload_session("file.bin", session_id="session"),
    lambda bucket: bucket.list(),
    lambda bucket: bucket.remove("file.bin"),
    lambda bucket: bucket.move("file.bin", "moved.bin"),
    lambda bucket: bucket.copy("file.bin", "copied.bin"),
    lambda bucket: bucket.update_visibility("file.bin", is_public=True),
)


@pytest.mark.parametrize(
    "operation",
    _STORAGE_OPERATIONS,
    ids=(
        "create-session",
        "upload-part",
        "complete-session",
        "get-session",
        "abort-session",
        "list",
        "remove",
        "move",
        "copy",
        "update-visibility",
    ),
)
def test_optional_storage_operation_requires_transport_capability(
    operation: Callable[[StorageBucket], object],
) -> None:
    client = VolcanoClient(anon_key="anon", _transport=RejectingTransport())

    with pytest.raises(TypeError, match="requested storage operation"):
        _ = operation(client.storage.from_("assets"))


@pytest.mark.parametrize("payload", [None, [], "invalid", 1])
def test_storage_object_rejects_non_mapping_payloads(payload: object) -> None:
    with pytest.raises(TypeError, match="Expected a complete storage page"):
        _ = _storage_object(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("metadata", []),
        ("metadata", "invalid"),
        ("size", True),
        ("size", 1.5),
        ("size", "1"),
        ("is_public", 1),
        ("is_public", "false"),
    ],
)
def test_storage_object_rejects_invalid_field_types(field: str, value: object) -> None:
    payload: dict[str, object] = {
        "id": "object",
        "bucket_id": "assets",
        "name": "file.bin",
        "size": 1,
        "mime_type": "application/octet-stream",
        "is_public": False,
        "metadata": {},
    }
    payload[field] = value
    with pytest.raises(TypeError, match="Expected a complete storage page"):
        _ = _storage_object(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", 1),
        ("bucket_id", None),
        ("name", []),
        ("mime_type", False),
        ("owner_id", 3),
        ("etag", []),
        ("public_url", 7),
        ("metadata", {"nested": object()}),
        ("metadata", {"nested": {1: "bad key"}}),
        ("metadata", {"nested": ["valid", object()]}),
        ("metadata", {"nested": {"invalid": object()}}),
    ],
)
def test_storage_object_rejects_untyped_response_fields(
    field: str, value: object
) -> None:
    payload: dict[str, object] = {
        "id": "object",
        "bucket_id": "assets",
        "name": "file.bin",
        "size": 4,
        "mime_type": "application/octet-stream",
        "is_public": False,
    }
    payload[field] = value

    with pytest.raises(TypeError, match="Expected a complete storage page"):
        _ = _storage_object(payload)


def test_storage_object_rejects_non_string_response_keys() -> None:
    payload: dict[object, object] = {
        "id": "object",
        "bucket_id": "assets",
        "name": "file.bin",
        "size": 4,
        "mime_type": "application/octet-stream",
        "is_public": False,
        1: "unexpected",
    }

    with pytest.raises(TypeError, match="Expected a complete storage page"):
        _ = _storage_object(payload)


def test_storage_object_preserves_nested_json_metadata() -> None:
    value = _storage_object(
        {
            "id": "object",
            "bucket_id": "assets",
            "name": "file.bin",
            "size": 4,
            "mime_type": "application/octet-stream",
            "is_public": False,
            "metadata": {"nested": {"values": (True, 3.5, None)}},
        }
    )

    assert value.metadata == {"nested": {"values": (True, 3.5, None)}}


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("session_id", None),
        ("part_size", "4"),
        ("total_parts", True),
        ("expires_at", None),
        ("expires_at", []),
    ],
)
def test_upload_session_rejects_untyped_response_fields(
    field: str, value: object
) -> None:
    payload: dict[str, object] = {
        "session_id": "session",
        "part_size": 4,
        "total_parts": 2,
        "expires_at": "2026-09-23T12:00:00Z",
    }
    payload[field] = value

    with pytest.raises(TypeError, match="Expected a complete storage page"):
        _ = _upload_session(payload)


def test_upload_session_accepts_a_datetime_from_a_typed_transport() -> None:
    expires_at = datetime(2026, 9, 23, tzinfo=UTC)
    value = _upload_session(
        {
            "session_id": "session",
            "part_size": 4,
            "total_parts": 2,
            "expires_at": expires_at,
        }
    )

    assert value.expires_at is expires_at


@pytest.mark.parametrize(
    ("field", "value"),
    [("part_number", False), ("etag", None), ("size", "4")],
)
def test_upload_part_rejects_untyped_response_fields(field: str, value: object) -> None:
    payload: dict[str, object] = {"part_number": 1, "etag": "part", "size": 4}
    payload[field] = value

    with pytest.raises(TypeError, match="Expected a complete storage page"):
        _ = _upload_part(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("status", "unknown"),
        ("status", 1),
        ("parts", {}),
        ("parts", [None]),
        ("bytes_uploaded", True),
        ("created_at", None),
    ],
)
def test_upload_status_rejects_untyped_response_fields(
    field: str, value: object
) -> None:
    payload: dict[str, object] = {
        "session_id": "session",
        "status": "uploading",
        "path": "file.bin",
        "content_type": "application/octet-stream",
        "total_size": 4,
        "part_size": 4,
        "total_parts": 1,
        "parts_uploaded": 0,
        "bytes_uploaded": 0,
        "expires_at": "2026-09-23T12:00:00Z",
        "created_at": "2026-09-23T11:00:00Z",
    }
    payload[field] = value

    with pytest.raises(TypeError, match="Expected a complete storage page"):
        _ = _upload_session_status(payload)


@pytest.mark.parametrize(
    "state", ["pending", "uploading", "completing", "completed", "aborted"]
)
def test_upload_status_preserves_each_server_state(state: str) -> None:
    status = _upload_session_status(
        {
            "session_id": "session",
            "status": state,
            "path": "file.bin",
            "content_type": "application/octet-stream",
            "total_size": 4,
            "part_size": 4,
            "total_parts": 1,
            "parts_uploaded": 0,
            "bytes_uploaded": 0,
            "expires_at": "2026-09-23T12:00:00Z",
            "created_at": "2026-09-23T11:00:00Z",
        }
    )
    assert status.status == state


@pytest.mark.parametrize("payload", [None, [], 1, {"objects": {}}, {"objects": None}])
def test_storage_page_rejects_invalid_collections(payload: object) -> None:
    with pytest.raises(TypeError, match="Expected a complete storage page"):
        _ = _storage_page(payload)


def test_storage_page_defaults_to_an_empty_terminal_page() -> None:
    page = _storage_page({})
    assert page.objects == ()
    assert page.next_cursor is None


def test_optional_storage_timestamp_preserves_a_datetime() -> None:
    value = datetime(2026, 9, 22, tzinfo=UTC)
    assert _optional_datetime(value) is value


@pytest.mark.parametrize("value", [False, 1, [], {}])
def test_optional_storage_timestamp_rejects_non_string_values(value: object) -> None:
    with pytest.raises(TypeError, match="Expected a complete storage page"):
        _ = _optional_datetime(value)


@pytest.mark.parametrize("paths", [None, 1, {"path": "file.bin"}])
def test_storage_paths_reject_non_sequences(paths: object) -> None:
    with pytest.raises(TypeError, match="Storage paths must be non-empty strings"):
        _ = _storage_paths(paths)


def test_upload_size_probe_restores_position_after_end_seek_fails() -> None:
    with EndSeekFailure(b"prefix-payload") as source:
        _ = source.seek(7)
        assert _remaining_upload_bytes(source) is None
        assert source.tell() == 7
        assert source.read() == b"payload"


def test_upload_size_probe_measures_remaining_bytes_from_current_position() -> None:
    with BytesIO(b"prefix-payload") as source:
        _ = source.seek(7)
        assert _remaining_upload_bytes(source) == len(b"payload")
        assert source.tell() == 7


def test_seek_capability_probe_rejects_lookup_failures() -> None:
    with SeekLookupFailure(b"payload") as source:
        assert not _has_seekable_methods(source)


def test_seek_capability_probe_rejects_read_only_inputs() -> None:
    assert not _has_seekable_methods(ReadOnlyBinaryInput())


def test_upload_spools_when_seek_capability_lookup_raises() -> None:
    with SeekLookupFailure(b"prefix-\x00\xffpayload") as source:
        _ = source.read(7)
        with _resumable_upload_source(source) as (upload, size):
            assert size == len(b"\x00\xffpayload")
            assert upload.read() == b"\x00\xffpayload"
        assert not source.closed


def test_spooling_reports_a_temporarily_unavailable_binary_source() -> None:
    with BufferedReader(UnavailableRawStream()) as source, BytesIO() as target:
        with pytest.raises(BlockingIOError, match="temporarily unavailable"):
            _spool_upload_source(source, target)
        assert target.getvalue() == b""
        assert not source.closed


def test_part_read_reports_a_temporarily_unavailable_binary_source() -> None:
    with BufferedReader(UnavailableRawStream()) as source:
        with pytest.raises(BlockingIOError, match="temporarily unavailable"):
            _ = _read_upload_part(source, 4)
        assert not source.closed


@pytest.mark.parametrize("payload", [b"", b"a", b"\x00\xff"])
def test_part_read_preserves_a_short_final_part(payload: bytes) -> None:
    with BytesIO(payload) as source:
        assert _read_upload_part(source, 4) == payload
        assert source.read() == b""
        assert not source.closed


def test_public_url_rejects_non_object_project_claims() -> None:
    client = VolcanoClient(anon_key="header.W10.signature")
    with pytest.raises(ValueError, match="Anon key must contain a project ID"):
        _ = client.storage.from_("assets").get_public_url("file.bin")


@pytest.mark.parametrize("data", [None, "text", bytearray(b"binary")])
def test_simple_upload_rejects_values_without_a_binary_read_method(
    data: object,
) -> None:
    with pytest.raises(TypeError, match="bytes or a readable binary stream"):
        _ = _simple_upload_bytes(data)
