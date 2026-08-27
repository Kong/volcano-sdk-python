"""Object storage facade."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from ._transport import Transport, invoke, response_payload


class StorageContext(Protocol):
    """Client capabilities required by object storage."""

    _transport: Transport

    def _session_token(self) -> str: ...


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


class Storage:
    """Entry point for project object storage."""

    def __init__(self, client: StorageContext) -> None:
        """Create a storage facade backed by a client."""
        self._client = client

    def from_(self, bucket: str) -> StorageBucket:
        """Create a facade scoped to a bucket."""
        return StorageBucket(self._client, bucket)
