"""Storage wire values and bounded binary stream adapters."""

from __future__ import annotations

import base64
import binascii
import json
from collections.abc import Callable, Generator, Mapping, Sequence
from contextlib import contextmanager
from datetime import datetime
from io import SEEK_END, SEEK_SET, BytesIO
from tempfile import TemporaryFile
from typing import (
    BinaryIO,
    Protocol,
    TypeGuard,
    cast,
    runtime_checkable,
)
from urllib.parse import quote

from typing_extensions import TypeIs

from .models import (
    JSONValue,
    StorageObject,
    StoragePage,
    UploadPart,
    UploadSession,
    UploadSessionState,
    UploadSessionStatus,
)

_INVALID_STORAGE_PAGE = "Expected a complete storage page"

_INVALID_CONTENT_TYPE = "content_type must be a non-blank printable ASCII string"

_INVALID_STORAGE_PATH = "Storage path must be a non-empty string"

_INVALID_STORAGE_PATHS = "Storage paths must be non-empty strings"

_INVALID_STORAGE_VISIBILITY = "is_public must be a boolean"

_INVALID_STORAGE_ANON_KEY = "Anon key must contain a project ID"

_INVALID_PUBLIC_URL_PATH = "Public URL paths cannot contain dot segments"

_JWT_PART_COUNT = 3

_HTTP_PARTIAL_CONTENT = 206

_UPLOAD_SPOOL_READ_SIZE = 1_048_576

_UPLOAD_SOURCE_UNAVAILABLE = "Upload source is temporarily unavailable"

_INVALID_SIMPLE_UPLOAD = "Upload data must be bytes or a readable binary stream"

_INVALID_UPLOAD_RESPONSE = "Expected a storage upload response object"

_INVALID_STORAGE_TRANSPORT = (
    "Transport does not support the requested storage operation"
)

_JSON_DECODE: Callable[[str], object] = json.loads


class BinaryReader(Protocol):
    """Binary input required by upload operations, including read-only streams."""

    def read(self, size: int = -1, /) -> bytes | None:
        """Return bytes, or None when the source is temporarily unavailable."""
        ...


@runtime_checkable
class SeekableBinaryReader(BinaryReader, Protocol):
    """Optional stream capabilities used to avoid spooling seekable inputs."""

    def seekable(self) -> bool:
        """Report whether seeking is supported."""
        ...

    def tell(self) -> int:
        """Return the current byte position."""
        ...

    def seek(self, offset: int, whence: int = SEEK_SET, /) -> int:
        """Move to a byte position and return it."""
        ...


def optional_datetime(value: object) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    raise TypeError(_INVALID_STORAGE_PAGE)


def storage_mapping(value: object) -> Mapping[str, object]:
    if not is_string_keyed_mapping(value):
        raise TypeError(_INVALID_STORAGE_PAGE)
    return value


def required_string(values: Mapping[str, object], key: str) -> str:
    value = values.get(key)
    if not isinstance(value, str):
        raise TypeError(_INVALID_STORAGE_PAGE)
    return value


def optional_string(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(_INVALID_STORAGE_PAGE)
    return value


def required_integer(values: Mapping[str, object], key: str) -> int:
    value = values.get(key)
    if type(value) is not int:
        raise TypeError(_INVALID_STORAGE_PAGE)
    return value


def required_datetime(values: Mapping[str, object], key: str) -> datetime:
    value = optional_datetime(values.get(key))
    if value is None:
        raise TypeError(_INVALID_STORAGE_PAGE)
    return value


def is_json_value(value: object) -> TypeGuard[JSONValue]:
    if value is None or isinstance(value, (str, int, float, bool)):
        return True
    if isinstance(value, (list, tuple)):
        items = cast("Sequence[object]", value)
        return all(is_json_value(item) for item in items)
    if isinstance(value, Mapping):
        entries = cast("Mapping[object, object]", value)
        return all(
            isinstance(key, str) and is_json_value(item)
            for key, item in entries.items()
        )
    return False


def is_json_record(value: object) -> TypeGuard[Mapping[str, JSONValue]]:
    if not isinstance(value, Mapping):
        return False
    entries = cast("Mapping[object, object]", value)
    return all(
        isinstance(key, str) and is_json_value(item) for key, item in entries.items()
    )


def storage_metadata(value: object) -> Mapping[str, JSONValue] | None:
    if value is None:
        return None
    if not is_json_record(value):
        raise TypeError(_INVALID_STORAGE_PAGE)
    return value


def storage_object(payload: object) -> StorageObject:
    values = storage_mapping(payload)
    is_public = values.get("is_public")
    if not isinstance(is_public, bool):
        raise TypeError(_INVALID_STORAGE_PAGE)
    return StorageObject(
        id=required_string(values, "id"),
        bucket_id=required_string(values, "bucket_id"),
        name=required_string(values, "name"),
        size=required_integer(values, "size"),
        mime_type=required_string(values, "mime_type"),
        is_public=is_public,
        owner_id=optional_string(values.get("owner_id")),
        etag=optional_string(values.get("etag")),
        metadata=storage_metadata(values.get("metadata")),
        created_at=optional_datetime(values.get("created_at")),
        updated_at=optional_datetime(values.get("updated_at")),
        public_url=optional_string(values.get("public_url")),
    )


def storage_page(payload: object) -> StoragePage:
    values = storage_mapping(payload)
    raw_objects = values.get("objects", [])
    if not isinstance(raw_objects, list):
        raise TypeError(_INVALID_STORAGE_PAGE)
    objects = cast("list[object]", raw_objects)
    next_cursor = values.get("next_cursor")
    return StoragePage(
        objects=tuple(storage_object(item) for item in objects),
        next_cursor=(
            None
            if next_cursor is None or (isinstance(next_cursor, str) and not next_cursor)
            else str(next_cursor)
        ),
    )


def upload_session(payload: object) -> UploadSession:
    values = storage_mapping(payload)
    return UploadSession(
        session_id=required_string(values, "session_id"),
        part_size=required_integer(values, "part_size"),
        total_parts=required_integer(values, "total_parts"),
        expires_at=required_datetime(values, "expires_at"),
    )


def upload_part(payload: object) -> UploadPart:
    values = storage_mapping(payload)
    return UploadPart(
        part_number=required_integer(values, "part_number"),
        etag=required_string(values, "etag"),
        size=required_integer(values, "size"),
    )


def is_upload_session_state(value: object) -> TypeGuard[UploadSessionState]:
    return isinstance(value, str) and value in {
        "pending",
        "uploading",
        "completing",
        "completed",
        "aborted",
    }


def upload_session_status(payload: object) -> UploadSessionStatus:
    values = storage_mapping(payload)
    raw_parts = values.get("parts", [])
    if not isinstance(raw_parts, list):
        raise TypeError(_INVALID_STORAGE_PAGE)
    parts = cast("list[object]", raw_parts)
    status = values.get("status")
    if not is_upload_session_state(status):
        raise TypeError(_INVALID_STORAGE_PAGE)
    return UploadSessionStatus(
        session_id=required_string(values, "session_id"),
        status=status,
        path=required_string(values, "path"),
        content_type=required_string(values, "content_type"),
        total_size=required_integer(values, "total_size"),
        part_size=required_integer(values, "part_size"),
        total_parts=required_integer(values, "total_parts"),
        parts_uploaded=required_integer(values, "parts_uploaded"),
        bytes_uploaded=required_integer(values, "bytes_uploaded"),
        parts=tuple(upload_part(part) for part in parts),
        expires_at=required_datetime(values, "expires_at"),
        created_at=required_datetime(values, "created_at"),
    )


def is_object_sequence(value: object) -> TypeGuard[Sequence[object]]:
    return isinstance(value, Sequence)


def storage_paths(paths: object) -> tuple[str, ...]:
    if isinstance(paths, str):
        raw_paths: tuple[object, ...] = (paths,)
    elif is_object_sequence(paths):
        raw_paths = tuple(paths)
    else:
        raise TypeError(_INVALID_STORAGE_PATHS)
    if not raw_paths or any(
        not isinstance(path, str) or not path for path in raw_paths
    ):
        raise ValueError(_INVALID_STORAGE_PATHS)
    return cast("tuple[str, ...]", raw_paths)


def storage_path(path: object) -> str:
    if not isinstance(path, str):
        raise TypeError(_INVALID_STORAGE_PATH)
    if not path:
        raise ValueError(_INVALID_STORAGE_PATH)
    return path


def storage_visibility(value: object) -> bool:
    if not isinstance(value, bool):
        raise TypeError(_INVALID_STORAGE_VISIBILITY)
    return value


def project_id_from_anon_key(anon_key: str) -> str:
    parts = anon_key.split(".")
    if len(parts) != _JWT_PART_COUNT:
        raise ValueError(_INVALID_STORAGE_ANON_KEY)
    try:
        encoded = parts[1].encode()
        padded = encoded + (b"=" * (-len(encoded) % 4))
        decoded = base64.b64decode(padded, altchars=b"-_", validate=True).decode()
        if not is_string_keyed_mapping(payload := _JSON_DECODE(decoded)):
            raise ValueError(_INVALID_STORAGE_ANON_KEY)
    except (binascii.Error, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(_INVALID_STORAGE_ANON_KEY) from error
    project_id = payload.get("project_id")
    if not isinstance(project_id, str) or not project_id.strip():
        raise ValueError(_INVALID_STORAGE_ANON_KEY)
    return project_id


def encoded_storage_path(path: str) -> str:
    segments = path.split("/")
    if any(segment in {".", ".."} for segment in segments):
        raise ValueError(_INVALID_PUBLIC_URL_PATH)
    return "/".join(quote(segment) for segment in segments)


def encoded_storage_component(value: str) -> str:
    return quote(value).replace("/", "%2F")


def has_seekable_methods(source: BinaryReader) -> TypeIs[SeekableBinaryReader]:
    try:
        if not isinstance(source, SeekableBinaryReader):
            return False
        return all(
            callable(method) for method in (source.seekable, source.tell, source.seek)
        )
    except (AttributeError, OSError, ValueError):
        return False


def remaining_upload_bytes(source: BinaryReader) -> int | None:
    if not has_seekable_methods(source):
        return None
    try:
        if not source.seekable():
            return None
        position = source.tell()
    except (AttributeError, OSError, ValueError):
        return None
    try:
        try:
            _ = source.seek(0, SEEK_END)
            remaining = max(0, source.tell() - position)
        except (OSError, ValueError):
            remaining = None
    finally:
        _ = source.seek(position)
    return remaining


def spool_upload_source(source: BinaryReader, target: BinaryIO) -> None:
    while True:
        chunk = source.read(_UPLOAD_SPOOL_READ_SIZE)
        if chunk is None:
            raise BlockingIOError(_UPLOAD_SOURCE_UNAVAILABLE)
        if not chunk:
            return
        _ = target.write(chunk)


def read_upload_part(source: BinaryReader, part_size: int) -> bytes:
    part = bytearray()
    while len(part) < part_size:
        chunk = source.read(part_size - len(part))
        if chunk is None:
            raise BlockingIOError(_UPLOAD_SOURCE_UNAVAILABLE)
        if not chunk:
            break
        part.extend(chunk)
    return bytes(part)


def simple_upload_bytes(data: object) -> bytes:
    if isinstance(data, bytes):
        return data
    read = getattr(data, "read", None)
    if not callable(read):
        raise TypeError(_INVALID_SIMPLE_UPLOAD)
    value = read()
    if value is None:
        raise BlockingIOError(_UPLOAD_SOURCE_UNAVAILABLE)
    if not isinstance(value, bytes):
        raise TypeError(_INVALID_SIMPLE_UPLOAD)
    return value


@contextmanager
def resumable_upload_source(
    data: bytes | BinaryReader,
) -> Generator[tuple[BinaryReader, int], None, None]:
    if isinstance(data, bytes):
        with BytesIO(data) as source:
            yield source, len(data)
        return
    remaining = remaining_upload_bytes(data)
    if remaining is not None:
        yield data, remaining
        return
    with TemporaryFile(mode="w+b") as source:
        spool_upload_source(data, source)
        total_size = source.tell()
        _ = source.seek(0)
        yield source, total_size


def upload_content_type(value: object) -> str:
    if value is None:
        return "application/octet-stream"
    if (
        not isinstance(value, str)
        or not value.strip()
        or not value.isascii()
        or not value.isprintable()
    ):
        raise ValueError(_INVALID_CONTENT_TYPE)
    return value


def is_object_mapping(value: object) -> TypeGuard[Mapping[object, object]]:
    return isinstance(value, Mapping)


def is_string_keyed_mapping(value: object) -> TypeGuard[Mapping[str, object]]:
    if not is_object_mapping(value):
        return False
    return all(isinstance(key, str) for key in value)
