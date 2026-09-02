"""Object storage facade."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Protocol, cast

from ._transport import Transport, TransportResponse, invoke, response_payload
from .models import JSONValue, StorageObject, StoragePage

_INVALID_STORAGE_PAGE = "Expected a complete storage page"
_INVALID_STORAGE_PATHS = "Storage paths must be non-empty strings"


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


class StorageContext(Protocol):
    """Client capabilities required by object storage."""

    _transport: Transport

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

    def download(self, path: str) -> bytes:
        """Download bytes from a path in this bucket."""
        response = invoke(
            self._client._transport.download_storage_object,
            authorization=self._client._session_token(),
            bucket_name=self._name,
            path=path,
        )
        response_payload(response, 200)
        return bytes(response.content)

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


class Storage:
    """Entry point for project object storage."""

    def __init__(self, client: StorageContext) -> None:
        """Create a storage facade backed by a client."""
        self._client = client

    def from_(self, bucket: str) -> StorageBucket:
        """Create a facade scoped to a bucket."""
        return StorageBucket(self._client, bucket)
