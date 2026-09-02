"""Object storage facade."""

from __future__ import annotations

import base64
import binascii
import json
from collections.abc import Callable, Generator, Mapping, Sequence
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from datetime import datetime
from io import SEEK_END, BytesIO
from tempfile import TemporaryFile
from typing import Any, BinaryIO, Protocol, cast
from urllib.parse import quote

from ._transport import (
    StorageUploadPartRequest,
    StorageUploadSessionReference,
    StorageUploadSessionRequest,
    Transport,
    TransportResponse,
    invoke,
    response_payload,
)
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
_INVALID_STORAGE_PATH = "Storage path must be a non-empty string"
_INVALID_STORAGE_PATHS = "Storage paths must be non-empty strings"
_INVALID_STORAGE_VISIBILITY = "is_public must be a boolean"
_INVALID_STORAGE_ANON_KEY = "Anon key must contain a project ID"
_INVALID_PUBLIC_URL_PATH = "Public URL paths cannot contain dot segments"
_JWT_PART_COUNT = 3
_HTTP_PARTIAL_CONTENT = 206
_UPLOAD_SPOOL_READ_SIZE = 1_048_576
_UPLOAD_SOURCE_UNAVAILABLE = "Upload source is temporarily unavailable"


def _optional_datetime(value: object) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    raise TypeError(_INVALID_STORAGE_PAGE)


def _storage_object(payload: object) -> StorageObject:
    if not isinstance(payload, Mapping):
        raise TypeError(_INVALID_STORAGE_PAGE)
    values = cast("Mapping[str, object]", payload)
    raw_metadata = values.get("metadata")
    if raw_metadata is not None and not isinstance(raw_metadata, Mapping):
        raise TypeError(_INVALID_STORAGE_PAGE)
    size = values["size"]
    is_public = values["is_public"]
    if type(size) is not int or not isinstance(is_public, bool):
        raise TypeError(_INVALID_STORAGE_PAGE)
    return StorageObject(
        id=str(values["id"]),
        bucket_id=str(values["bucket_id"]),
        name=str(values["name"]),
        size=size,
        mime_type=str(values["mime_type"]),
        is_public=is_public,
        owner_id=None if values.get("owner_id") is None else str(values["owner_id"]),
        etag=None if values.get("etag") is None else str(values["etag"]),
        metadata=cast("Mapping[str, JSONValue] | None", raw_metadata),
        created_at=_optional_datetime(values.get("created_at")),
        updated_at=_optional_datetime(values.get("updated_at")),
        public_url=(
            None if values.get("public_url") is None else str(values["public_url"])
        ),
    )


def _storage_page(payload: object) -> StoragePage:
    if not isinstance(payload, Mapping):
        raise TypeError(_INVALID_STORAGE_PAGE)
    values = cast("Mapping[str, object]", payload)
    raw_objects = values.get("objects", [])
    if not isinstance(raw_objects, list):
        raise TypeError(_INVALID_STORAGE_PAGE)
    objects = cast("list[object]", raw_objects)
    next_cursor = values.get("next_cursor")
    return StoragePage(
        objects=tuple(_storage_object(item) for item in objects),
        next_cursor=(
            None if next_cursor is None or next_cursor == "" else str(next_cursor)
        ),
    )


def _upload_session(payload: object) -> UploadSession:
    values = cast("Mapping[str, object]", payload)
    raw_expires_at = values["expires_at"]
    expires_at = (
        datetime.fromisoformat(raw_expires_at)
        if isinstance(raw_expires_at, str)
        else cast("datetime", raw_expires_at)
    )
    return UploadSession(
        session_id=cast("str", values["session_id"]),
        part_size=cast("int", values["part_size"]),
        total_parts=cast("int", values["total_parts"]),
        expires_at=expires_at,
    )


def _upload_part(payload: object) -> UploadPart:
    values = cast("Mapping[str, object]", payload)
    return UploadPart(
        part_number=cast("int", values["part_number"]),
        etag=cast("str", values["etag"]),
        size=cast("int", values["size"]),
    )


def _upload_session_status(payload: object) -> UploadSessionStatus:
    values = cast("Mapping[str, object]", payload)
    raw_parts = cast("list[object]", values.get("parts", []))
    return UploadSessionStatus(
        session_id=cast("str", values["session_id"]),
        status=cast("UploadSessionState", values["status"]),
        path=cast("str", values["path"]),
        content_type=cast("str", values["content_type"]),
        total_size=cast("int", values["total_size"]),
        part_size=cast("int", values["part_size"]),
        total_parts=cast("int", values["total_parts"]),
        parts_uploaded=cast("int", values["parts_uploaded"]),
        bytes_uploaded=cast("int", values["bytes_uploaded"]),
        parts=tuple(_upload_part(part) for part in raw_parts),
        expires_at=cast("datetime", _optional_datetime(values["expires_at"])),
        created_at=cast("datetime", _optional_datetime(values["created_at"])),
    )


def _storage_paths(paths: object) -> tuple[str, ...]:
    if isinstance(paths, str):
        raw_paths: tuple[object, ...] = (paths,)
    elif isinstance(paths, Sequence):
        raw_paths = tuple(cast("Sequence[object]", paths))
    else:
        raise TypeError(_INVALID_STORAGE_PATHS)
    if not raw_paths or any(
        not isinstance(path, str) or not path for path in raw_paths
    ):
        raise ValueError(_INVALID_STORAGE_PATHS)
    return cast("tuple[str, ...]", raw_paths)


def _storage_path(path: object) -> str:
    if not isinstance(path, str):
        raise TypeError(_INVALID_STORAGE_PATH)
    if not path:
        raise ValueError(_INVALID_STORAGE_PATH)
    return path


def _storage_visibility(value: object) -> bool:
    if not isinstance(value, bool):
        raise TypeError(_INVALID_STORAGE_VISIBILITY)
    return value


def _project_id_from_anon_key(anon_key: str) -> str:
    parts = anon_key.split(".")
    if len(parts) != _JWT_PART_COUNT:
        raise ValueError(_INVALID_STORAGE_ANON_KEY)
    try:
        encoded = parts[1].encode("ascii")
        padded = encoded + (b"=" * (-len(encoded) % 4))
        payload = json.loads(
            base64.b64decode(padded, altchars=b"-_", validate=True).decode(),
        )
    except (binascii.Error, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(_INVALID_STORAGE_ANON_KEY) from error
    claims: Mapping[str, object] = {}
    if isinstance(payload, Mapping):
        claims = cast("Mapping[str, object]", payload)
    project_id = claims.get("project_id")
    if not isinstance(project_id, str) or not project_id.strip():
        raise ValueError(_INVALID_STORAGE_ANON_KEY)
    return project_id


def _encoded_storage_path(path: str) -> str:
    segments = path.split("/")
    if any(segment in {".", ".."} for segment in segments):
        raise ValueError(_INVALID_PUBLIC_URL_PATH)
    return "/".join(quote(segment, safe="") for segment in segments)


def _remaining_upload_bytes(source: BinaryIO) -> int | None:
    try:
        if not source.seekable():
            return None
        position = source.tell()
    except (AttributeError, OSError, ValueError):
        return None
    try:
        try:
            source.seek(0, SEEK_END)
            remaining = max(0, source.tell() - position)
        except (OSError, ValueError):
            remaining = None
    finally:
        source.seek(position)
    return remaining


def _spool_upload_source(source: BinaryIO, target: BinaryIO) -> None:
    while True:
        chunk = cast("bytes | None", source.read(_UPLOAD_SPOOL_READ_SIZE))
        if chunk is None:
            raise BlockingIOError(_UPLOAD_SOURCE_UNAVAILABLE)
        if chunk == b"":
            return
        target.write(chunk)


def _read_upload_part(source: BinaryIO, part_size: int) -> bytes:
    part = bytearray()
    while len(part) < part_size:
        chunk = cast("bytes | None", source.read(part_size - len(part)))
        if chunk is None:
            raise BlockingIOError(_UPLOAD_SOURCE_UNAVAILABLE)
        if chunk == b"":
            break
        part.extend(chunk)
    return bytes(part)


@contextmanager
def _resumable_upload_source(
    data: bytes | BinaryIO,
) -> Generator[tuple[BinaryIO, int], None, None]:
    if isinstance(data, bytes):
        with BytesIO(data) as source:
            yield source, len(data)
        return
    remaining = _remaining_upload_bytes(data)
    if remaining is not None:
        yield data, remaining
        return
    with TemporaryFile(mode="w+b") as source:
        _spool_upload_source(data, source)
        total_size = source.tell()
        source.seek(0)
        yield source, total_size


class StorageContext(Protocol):
    """Client capabilities required by object storage."""

    _transport: Transport

    def _anon_token(self) -> str: ...

    def _api_base_url(self) -> str: ...

    def _session_token(self) -> str: ...


class StorageListTransport(Protocol):
    """Transport capability required to list storage objects."""

    def list_storage_objects(
        self,
        *,
        authorization: str,
        bucket_name: str,
        prefix: str,
        limit: int | None,
        cursor: str | None,
    ) -> TransportResponse:
        """Request one page of objects from a bucket."""
        ...


class StorageDeleteTransport(Protocol):
    """Transport capability required to delete storage objects."""

    def delete_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
    ) -> TransportResponse:
        """Delete one object from a bucket."""
        ...


class StorageMoveTransport(Protocol):
    """Transport capability required to move a storage object."""

    def move_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        from_path: str,
        to_path: str,
    ) -> TransportResponse:
        """Move one object within a bucket."""
        ...


class StorageCopyTransport(Protocol):
    """Transport capability required to copy a storage object."""

    def copy_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        from_path: str,
        to_path: str,
    ) -> TransportResponse:
        """Copy one object within a bucket."""
        ...


class StorageVisibilityTransport(Protocol):
    """Transport capability required to update object visibility."""

    def update_storage_object_visibility(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
        is_public: bool,
    ) -> TransportResponse:
        """Update one object's visibility."""
        ...


class StorageUploadSessionTransport(Protocol):
    """Transport capability required to create resumable upload sessions."""

    def create_upload_session(
        self,
        *,
        authorization: str,
        bucket_name: str,
        request: StorageUploadSessionRequest,
    ) -> TransportResponse:
        """Create one resumable upload session."""
        ...


class StorageUploadPartTransport(Protocol):
    """Transport capability required to upload resumable storage parts."""

    def upload_part(
        self,
        *,
        authorization: str,
        bucket_name: str,
        request: StorageUploadPartRequest,
    ) -> TransportResponse:
        """Upload one resumable storage part."""
        ...


class StorageCompleteUploadTransport(Protocol):
    """Transport capability required to complete resumable storage uploads."""

    def complete_upload_session(
        self,
        *,
        authorization: str,
        bucket_name: str,
        request: StorageUploadSessionReference,
    ) -> TransportResponse:
        """Complete one resumable storage upload session."""
        ...


class StorageUploadStatusTransport(Protocol):
    """Transport capability required to inspect resumable storage uploads."""

    def get_upload_session(
        self,
        *,
        authorization: str,
        bucket_name: str,
        request: StorageUploadSessionReference,
    ) -> TransportResponse:
        """Get one resumable storage upload session."""
        ...


class StorageAbortUploadTransport(Protocol):
    """Transport capability required to abort resumable storage uploads."""

    def abort_upload_session(
        self,
        *,
        authorization: str,
        bucket_name: str,
        request: StorageUploadSessionReference,
    ) -> TransportResponse:
        """Abort one resumable storage upload session."""
        ...


@dataclass(frozen=True, slots=True)
class StorageBucket:
    """Operations scoped to one storage bucket."""

    _client: StorageContext
    _name: str

    def upload(self, path: str, data: bytes) -> dict[str, Any]:
        """Upload bytes to a path in this bucket."""
        response = invoke(
            self._client._transport.upload_storage_object,
            authorization=self._client._session_token(),
            bucket_name=self._name,
            path=path,
            data=data,
        )
        payload = response_payload(response, 201)
        return dict(payload)

    def download(self, path: str, *, byte_range: str | None = None) -> bytes:
        """Download bytes from a path in this bucket."""
        response = invoke(
            self._client._transport.download_storage_object,
            authorization=self._client._session_token(),
            bucket_name=self._name,
            path=path,
            byte_range=byte_range,
        )
        expected_status = (
            _HTTP_PARTIAL_CONTENT
            if byte_range is not None and response.status_code == _HTTP_PARTIAL_CONTENT
            else 200
        )
        response_payload(response, expected_status)
        return bytes(response.content)

    def create_upload_session(
        self,
        path: str,
        *,
        total_size: int,
        content_type: str = "application/octet-stream",
        part_size: int | None = None,
    ) -> UploadSession:
        """Create server state for a resumable upload."""
        transport = cast("StorageUploadSessionTransport", self._client._transport)
        response = invoke(
            transport.create_upload_session,
            authorization=self._client._session_token(),
            bucket_name=self._name,
            request=StorageUploadSessionRequest(
                path=_storage_path(path),
                content_type=content_type,
                total_size=total_size,
                part_size=part_size,
            ),
        )
        return _upload_session(response_payload(response, 201))

    def upload_part(
        self,
        path: str,
        *,
        session_id: str,
        part_number: int,
        data: bytes,
    ) -> UploadPart:
        """Upload one part of a resumable upload session."""
        transport = cast("StorageUploadPartTransport", self._client._transport)
        response = invoke(
            transport.upload_part,
            authorization=self._client._session_token(),
            bucket_name=self._name,
            request=StorageUploadPartRequest(
                path=_storage_path(path),
                session_id=session_id,
                part_number=part_number,
                data=data,
            ),
        )
        return _upload_part(response_payload(response, 200))

    def complete_upload_session(
        self,
        path: str,
        *,
        session_id: str,
    ) -> StorageObject:
        """Complete a resumable upload and return the stored object."""
        transport = cast("StorageCompleteUploadTransport", self._client._transport)
        response = invoke(
            transport.complete_upload_session,
            authorization=self._client._session_token(),
            bucket_name=self._name,
            request=StorageUploadSessionReference(
                path=_storage_path(path),
                session_id=session_id,
            ),
        )
        payload = cast("Mapping[str, object]", response_payload(response, 200))
        return _storage_object(payload["object"])

    def get_upload_session(
        self,
        path: str,
        *,
        session_id: str,
    ) -> UploadSessionStatus:
        """Get resumable upload progress and uploaded part metadata."""
        transport = cast("StorageUploadStatusTransport", self._client._transport)
        response = invoke(
            transport.get_upload_session,
            authorization=self._client._session_token(),
            bucket_name=self._name,
            request=StorageUploadSessionReference(
                path=_storage_path(path),
                session_id=session_id,
            ),
        )
        return _upload_session_status(response_payload(response, 200))

    def abort_upload_session(
        self,
        path: str,
        *,
        session_id: str,
    ) -> None:
        """Abort a resumable upload and discard its uploaded parts."""
        transport = cast("StorageAbortUploadTransport", self._client._transport)
        response = invoke(
            transport.abort_upload_session,
            authorization=self._client._session_token(),
            bucket_name=self._name,
            request=StorageUploadSessionReference(
                path=_storage_path(path),
                session_id=session_id,
            ),
        )
        response_payload(response, 200)

    def upload_resumable(
        self,
        path: str,
        data: bytes | BinaryIO,
        *,
        content_type: str = "application/octet-stream",
        part_size: int | None = None,
        on_progress: Callable[[int, int], None] | None = None,
    ) -> StorageObject:
        """Upload bytes or a binary stream through a resumable session."""
        path = _storage_path(path)
        self._client._session_token()
        with _resumable_upload_source(data) as (source, total_size):
            session = self.create_upload_session(
                path,
                total_size=total_size,
                content_type=content_type,
                part_size=part_size,
            )
            upload_succeeded = False
            try:
                self._upload_session_parts(
                    path,
                    source,
                    session,
                    total_size,
                    on_progress,
                )
                upload_succeeded = True
            finally:
                if not upload_succeeded:
                    self._abort_failed_upload(path, session.session_id)
            return self.complete_upload_session(path, session_id=session.session_id)

    def _upload_session_parts(
        self,
        path: str,
        source: BinaryIO,
        session: UploadSession,
        total_size: int,
        on_progress: Callable[[int, int], None] | None,
    ) -> None:
        uploaded = 0
        for part_index in range(session.total_parts):
            part = _read_upload_part(source, session.part_size)
            self.upload_part(
                path,
                session_id=session.session_id,
                part_number=part_index + 1,
                data=part,
            )
            uploaded += len(part)
            if on_progress is not None:
                on_progress(uploaded, total_size)

    def _abort_failed_upload(self, path: str, session_id: str) -> None:
        with suppress(Exception):
            self.abort_upload_session(path, session_id=session_id)

    def list(
        self,
        prefix: str = "",
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> StoragePage:
        """List objects under a prefix and return the next-page cursor."""
        transport = cast("StorageListTransport", self._client._transport)
        response = invoke(
            transport.list_storage_objects,
            authorization=self._client._session_token(),
            bucket_name=self._name,
            prefix=prefix,
            limit=limit,
            cursor=cursor,
        )
        return _storage_page(response_payload(response, 200))

    def remove(self, paths: str | Sequence[str]) -> tuple[str, ...]:
        """Delete one or more object paths and return their immutable snapshot."""
        path_list = _storage_paths(paths)
        transport = cast("StorageDeleteTransport", self._client._transport)
        authorization = self._client._session_token()
        for path in path_list:
            response = invoke(
                transport.delete_storage_object,
                authorization=authorization,
                bucket_name=self._name,
                path=path,
            )
            response_payload(response, 200)
        return path_list

    def move(self, from_path: str, to_path: str) -> StorageObject:
        """Move or rename an object within this bucket."""
        source, destination = _storage_paths((from_path, to_path))
        transport = cast("StorageMoveTransport", self._client._transport)
        response = invoke(
            transport.move_storage_object,
            authorization=self._client._session_token(),
            bucket_name=self._name,
            from_path=source,
            to_path=destination,
        )
        return _storage_object(response_payload(response, 200))

    def copy(self, from_path: str, to_path: str) -> StorageObject:
        """Copy an object to another path within this bucket."""
        source, destination = _storage_paths((from_path, to_path))
        transport = cast("StorageCopyTransport", self._client._transport)
        response = invoke(
            transport.copy_storage_object,
            authorization=self._client._session_token(),
            bucket_name=self._name,
            from_path=source,
            to_path=destination,
        )
        return _storage_object(response_payload(response, 201))

    def update_visibility(self, path: str, *, is_public: bool) -> StorageObject:
        """Set an object's public visibility and return its server state."""
        object_path = _storage_paths(path)[0]
        visibility = _storage_visibility(is_public)
        transport = cast("StorageVisibilityTransport", self._client._transport)
        response = invoke(
            transport.update_storage_object_visibility,
            authorization=self._client._session_token(),
            bucket_name=self._name,
            path=object_path,
            is_public=visibility,
        )
        return _storage_object(response_payload(response, 200))

    def get_public_url(self, path: str) -> str:
        """Construct this object's public URL without making a request."""
        object_path = _storage_path(path)
        project_id = _project_id_from_anon_key(self._client._anon_token())
        return (
            f"{self._client._api_base_url()}/public/"
            f"{quote(project_id, safe='')}/{quote(self._name, safe='')}/"
            f"{_encoded_storage_path(object_path)}"
        )


class Storage:
    """Entry point for project object storage."""

    def __init__(self, client: StorageContext) -> None:
        """Create a storage facade backed by a client."""
        self._client = client

    def from_(self, bucket: str) -> StorageBucket:
        """Create a facade scoped to a bucket."""
        return StorageBucket(self._client, bucket)
