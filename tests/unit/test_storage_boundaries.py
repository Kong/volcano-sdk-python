from __future__ import annotations

from datetime import UTC, datetime
from io import SEEK_END, BufferedReader, BytesIO, RawIOBase

import pytest
from typing_extensions import override

from volcano_sdk import VolcanoClient
from volcano_sdk.storage import (
    _optional_datetime,
    _read_upload_part,
    _remaining_upload_bytes,
    _simple_upload_bytes,
    _spool_upload_source,
    _storage_object,
    _storage_page,
    _storage_paths,
)


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


@pytest.mark.parametrize("payload", [None, [], "invalid", 1])
def test_storage_object_rejects_non_mapping_payloads(payload: object) -> None:
    with pytest.raises(TypeError, match="Expected a complete storage page"):
        _storage_object(payload)


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
    payload: dict[str, object] = {"metadata": {}, "size": 1, "is_public": False}
    payload[field] = value
    with pytest.raises(TypeError, match="Expected a complete storage page"):
        _storage_object(payload)


@pytest.mark.parametrize("payload", [None, [], 1, {"objects": {}}, {"objects": None}])
def test_storage_page_rejects_invalid_collections(payload: object) -> None:
    with pytest.raises(TypeError, match="Expected a complete storage page"):
        _storage_page(payload)


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
        _optional_datetime(value)


@pytest.mark.parametrize("paths", [None, 1, {"path": "file.bin"}])
def test_storage_paths_reject_non_sequences(paths: object) -> None:
    with pytest.raises(TypeError, match="Storage paths must be non-empty strings"):
        _storage_paths(paths)


def test_upload_size_probe_restores_position_after_end_seek_fails() -> None:
    with EndSeekFailure(b"prefix-payload") as source:
        source.seek(7)
        assert _remaining_upload_bytes(source) is None
        assert source.tell() == 7
        assert source.read() == b"payload"


def test_spooling_reports_a_temporarily_unavailable_binary_source() -> None:
    with BufferedReader(UnavailableRawStream()) as source, BytesIO() as target:
        with pytest.raises(BlockingIOError, match="temporarily unavailable"):
            _spool_upload_source(source, target)
        assert target.getvalue() == b""
        assert not source.closed


def test_part_read_reports_a_temporarily_unavailable_binary_source() -> None:
    with BufferedReader(UnavailableRawStream()) as source:
        with pytest.raises(BlockingIOError, match="temporarily unavailable"):
            _read_upload_part(source, 4)
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
        client.storage.from_("assets").get_public_url("file.bin")


@pytest.mark.parametrize("data", [None, "text", bytearray(b"binary")])
def test_simple_upload_rejects_values_without_a_binary_read_method(
    data: object,
) -> None:
    with pytest.raises(TypeError, match="bytes or a readable binary stream"):
        _simple_upload_bytes(data)
