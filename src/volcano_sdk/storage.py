"""Object storage facade."""

from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Protocol,
    runtime_checkable,
)

from ._storage_values import (
    BinaryReader,
    SeekableBinaryReader,
    encoded_storage_component,
    encoded_storage_path,
    is_string_keyed_mapping,
    project_id_from_anon_key,
    read_upload_part,
    resumable_upload_source,
    simple_upload_bytes,
    storage_mapping,
    storage_object,
    storage_page,
    storage_path,
    storage_paths,
    storage_visibility,
    upload_content_type,
    upload_part,
    upload_session,
    upload_session_status,
)
from ._transport import (
    StorageUploadPartRequest,
    StorageUploadSessionReference,
    StorageUploadSessionRequest,
    Transport,
    TransportResponse,
    invoke,
    response_payload,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from ._auth_requests import AuthRequests
    from ._session_operations import SessionOperations
    from .models import (
        Session,
        StorageObject,
        StoragePage,
        UploadPart,
        UploadSession,
        UploadSessionStatus,
    )


_HTTP_PARTIAL_CONTENT = 206

_INVALID_UPLOAD_RESPONSE = "Expected a storage upload response object"

_INVALID_STORAGE_TRANSPORT = (
    "Transport does not support the requested storage operation"
)


__all__ = [
    "BinaryReader",
    "SeekableBinaryReader",
    "Storage",
    "StorageAbortUploadTransport",
    "StorageBucket",
    "StorageCompleteUploadTransport",
    "StorageContext",
    "StorageCopyTransport",
    "StorageDeleteTransport",
    "StorageListTransport",
    "StorageMoveTransport",
    "StorageUploadPartTransport",
    "StorageUploadSessionTransport",
    "StorageUploadStatusTransport",
    "StorageVisibilityTransport",
]


class StorageContext(Protocol):
    """Client capabilities required by object storage."""

    def transport(self) -> Transport:
        """Return the active typed transport."""
        ...

    def auth(self) -> AuthRequests:
        """Return the shared session request coordinator."""
        ...

    def anon_token(self) -> str:
        """Return the configured anonymous credential."""
        ...

    def api_base_url(self) -> str:
        """Return the API base URL."""
        ...

    def session_token(self) -> str:
        """Return the active session credential."""
        ...

    def capture_session_binding(
        self,
    ) -> tuple[int, SessionOperations, Session | None]:
        """Capture session ownership and credentials together."""
        ...


@runtime_checkable
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


@runtime_checkable
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


@runtime_checkable
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


@runtime_checkable
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


@runtime_checkable
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


@runtime_checkable
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


@runtime_checkable
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


@runtime_checkable
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


@runtime_checkable
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


@runtime_checkable
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

    def upload(
        self,
        path: str,
        data: bytes | BinaryReader,
        *,
        content_type: str | None = None,
    ) -> dict[str, object]:
        """Upload bytes or the remaining contents of a binary stream.

        Returns:
            Server response fields describing the uploaded object.

        Raises:
            TypeError: The upload response is not an object.

        """
        mime_type = upload_content_type(content_type)
        binding = self._client.capture_session_binding()
        _ = self._client.session_token()
        content = simple_upload_bytes(data)
        response = self._client.auth().request(
            lambda token: invoke(
                self._client.transport().upload_storage_object,
                authorization=token,
                bucket_name=self._name,
                path=path,
                data=content,
                content_type=mime_type,
            ),
            binding=binding,
        )
        payload = response_payload(response, 201)
        if not is_string_keyed_mapping(payload):
            raise TypeError(_INVALID_UPLOAD_RESPONSE)
        return dict(payload)

    def download(self, path: str, *, byte_range: str | None = None) -> bytes:
        """Download bytes from a path in this bucket.

        Returns:
            Downloaded bytes, without text decoding.

        """
        response = self._client.auth().request(
            lambda token: invoke(
                self._client.transport().download_storage_object,
                authorization=token,
                bucket_name=self._name,
                path=path,
                byte_range=byte_range,
            )
        )
        expected_status = (
            _HTTP_PARTIAL_CONTENT
            if byte_range is not None and response.status_code == _HTTP_PARTIAL_CONTENT
            else 200
        )
        _ = response_payload(response, expected_status)
        return bytes(response.content)

    def create_upload_session(
        self,
        path: str,
        *,
        total_size: int,
        content_type: str = "application/octet-stream",
        part_size: int | None = None,
    ) -> UploadSession:
        """Create server state for a resumable upload.

        Returns:
            Session ID, server-selected part size and count, and expiry.

        Raises:
            TypeError: The transport does not support this storage operation.

        """
        transport = self._client.transport()
        if not isinstance(transport, StorageUploadSessionTransport):
            raise TypeError(_INVALID_STORAGE_TRANSPORT)
        response = self._client.auth().request(
            lambda token: invoke(
                transport.create_upload_session,
                authorization=token,
                bucket_name=self._name,
                request=StorageUploadSessionRequest(
                    path=storage_path(path),
                    content_type=content_type,
                    total_size=total_size,
                    part_size=part_size,
                ),
            )
        )
        return upload_session(response_payload(response, 201))

    def upload_part(
        self,
        path: str,
        *,
        session_id: str,
        part_number: int,
        data: bytes,
    ) -> UploadPart:
        """Upload one part of a resumable upload session.

        Returns:
            The accepted part number, ETag, and byte count.

        Raises:
            TypeError: The transport does not support this storage operation.

        """
        transport = self._client.transport()
        if not isinstance(transport, StorageUploadPartTransport):
            raise TypeError(_INVALID_STORAGE_TRANSPORT)
        response = self._client.auth().request(
            lambda token: invoke(
                transport.upload_part,
                authorization=token,
                bucket_name=self._name,
                request=StorageUploadPartRequest(
                    path=storage_path(path),
                    session_id=session_id,
                    part_number=part_number,
                    data=data,
                ),
            )
        )
        return upload_part(response_payload(response, 200))

    def complete_upload_session(
        self,
        path: str,
        *,
        session_id: str,
    ) -> StorageObject:
        """Complete a resumable upload and return the stored object.

        Returns:
            Metadata for the object assembled from the uploaded parts.

        Raises:
            TypeError: The transport does not support this storage operation.

        """
        transport = self._client.transport()
        if not isinstance(transport, StorageCompleteUploadTransport):
            raise TypeError(_INVALID_STORAGE_TRANSPORT)
        response = self._client.auth().request(
            lambda token: invoke(
                transport.complete_upload_session,
                authorization=token,
                bucket_name=self._name,
                request=StorageUploadSessionReference(
                    path=storage_path(path),
                    session_id=session_id,
                ),
            )
        )
        payload = storage_mapping(response_payload(response, 200))
        return storage_object(payload["object"])

    def get_upload_session(
        self,
        path: str,
        *,
        session_id: str,
    ) -> UploadSessionStatus:
        """Get resumable upload progress and uploaded part metadata.

        Returns:
            Session state, byte and part counts, uploaded parts, and timestamps.

        Raises:
            TypeError: The transport does not support this storage operation.

        """
        transport = self._client.transport()
        if not isinstance(transport, StorageUploadStatusTransport):
            raise TypeError(_INVALID_STORAGE_TRANSPORT)
        response = self._client.auth().request(
            lambda token: invoke(
                transport.get_upload_session,
                authorization=token,
                bucket_name=self._name,
                request=StorageUploadSessionReference(
                    path=storage_path(path),
                    session_id=session_id,
                ),
            )
        )
        return upload_session_status(response_payload(response, 200))

    def abort_upload_session(
        self,
        path: str,
        *,
        session_id: str,
    ) -> None:
        """Abort a resumable upload and discard its uploaded parts.

        Raises:
            TypeError: The transport does not support this storage operation.

        """
        transport = self._client.transport()
        if not isinstance(transport, StorageAbortUploadTransport):
            raise TypeError(_INVALID_STORAGE_TRANSPORT)
        response = self._client.auth().request(
            lambda token: invoke(
                transport.abort_upload_session,
                authorization=token,
                bucket_name=self._name,
                request=StorageUploadSessionReference(
                    path=storage_path(path),
                    session_id=session_id,
                ),
            )
        )
        _ = response_payload(response, 200)

    def upload_resumable(
        self,
        path: str,
        data: bytes | BinaryReader,
        *,
        content_type: str = "application/octet-stream",
        part_size: int | None = None,
        on_progress: Callable[[int, int], None] | None = None,
    ) -> StorageObject:
        """Upload bytes or a binary stream through a resumable session.

        Returns:
            Metadata for the completed object.

        """
        path = storage_path(path)
        _ = self._client.session_token()
        with resumable_upload_source(data) as (source, total_size):
            session = self.create_upload_session(
                path,
                total_size=total_size,
                content_type=content_type,
                part_size=part_size,
            )
            try:
                self._upload_session_parts(
                    path,
                    source,
                    session,
                    total_size,
                    on_progress,
                )
            except BaseException:
                self._abort_failed_upload(path, session.session_id)
                raise
            return self.complete_upload_session(path, session_id=session.session_id)

    def _upload_session_parts(
        self,
        path: str,
        source: BinaryReader,
        session: UploadSession,
        total_size: int,
        on_progress: Callable[[int, int], None] | None,
    ) -> None:
        uploaded = 0
        for part_index in range(session.total_parts):
            part = read_upload_part(source, session.part_size)
            _ = self.upload_part(
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
        """List objects under a prefix and return the next-page cursor.

        Returns:
            An immutable object page whose next_cursor is None on the last page.

        Raises:
            TypeError: The transport does not support this storage operation.

        """
        transport = self._client.transport()
        if not isinstance(transport, StorageListTransport):
            raise TypeError(_INVALID_STORAGE_TRANSPORT)
        response = self._client.auth().request(
            lambda token: invoke(
                transport.list_storage_objects,
                authorization=token,
                bucket_name=self._name,
                prefix=prefix,
                limit=limit,
                cursor=cursor,
            )
        )
        return storage_page(response_payload(response, 200))

    def remove(self, paths: str | Sequence[str]) -> tuple[str, ...]:
        """Delete one or more object paths and return their immutable snapshot.

        Returns:
            The deleted paths as a tuple, in the supplied order.

        """
        path_list = storage_paths(paths)
        binding = self._client.capture_session_binding()
        for path in path_list:
            self._remove_path(path, binding)
        return path_list

    def _remove_path(
        self, path: str, binding: tuple[int, SessionOperations, Session | None]
    ) -> None:
        transport = self._client.transport()
        if not isinstance(transport, StorageDeleteTransport):
            raise TypeError(_INVALID_STORAGE_TRANSPORT)
        response = self._client.auth().request(
            lambda token: invoke(
                transport.delete_storage_object,
                authorization=token,
                bucket_name=self._name,
                path=path,
            ),
            binding=binding,
        )
        _ = response_payload(response, 200)

    def move(self, from_path: str, to_path: str) -> StorageObject:
        """Move or rename an object within this bucket.

        Returns:
            Metadata for the object at its destination path.

        Raises:
            TypeError: The transport does not support this storage operation.

        """
        source, destination = storage_paths((from_path, to_path))
        transport = self._client.transport()
        if not isinstance(transport, StorageMoveTransport):
            raise TypeError(_INVALID_STORAGE_TRANSPORT)
        response = self._client.auth().request(
            lambda token: invoke(
                transport.move_storage_object,
                authorization=token,
                bucket_name=self._name,
                from_path=source,
                to_path=destination,
            )
        )
        return storage_object(response_payload(response, 200))

    def copy(self, from_path: str, to_path: str) -> StorageObject:
        """Copy an object to another path within this bucket.

        Returns:
            Metadata for the new copy at its destination path.

        Raises:
            TypeError: The transport does not support this storage operation.

        """
        source, destination = storage_paths((from_path, to_path))
        transport = self._client.transport()
        if not isinstance(transport, StorageCopyTransport):
            raise TypeError(_INVALID_STORAGE_TRANSPORT)
        response = self._client.auth().request(
            lambda token: invoke(
                transport.copy_storage_object,
                authorization=token,
                bucket_name=self._name,
                from_path=source,
                to_path=destination,
            )
        )
        return storage_object(response_payload(response, 201))

    def update_visibility(self, path: str, *, is_public: bool) -> StorageObject:
        """Set an object's public visibility and return its server state.

        Returns:
            Object metadata reflecting the updated visibility.

        Raises:
            TypeError: The transport does not support this storage operation.

        """
        object_path = storage_paths(path)[0]
        visibility = storage_visibility(is_public)
        transport = self._client.transport()
        if not isinstance(transport, StorageVisibilityTransport):
            raise TypeError(_INVALID_STORAGE_TRANSPORT)
        response = self._client.auth().request(
            lambda token: invoke(
                transport.update_storage_object_visibility,
                authorization=token,
                bucket_name=self._name,
                path=object_path,
                is_public=visibility,
            )
        )
        return storage_object(response_payload(response, 200))

    def get_public_url(self, path: str) -> str:
        """Construct this object's public URL without making a request.

        Returns:
            The encoded public URL; this does not check existence or visibility.

        """
        object_path = storage_path(path)
        project_id = project_id_from_anon_key(self._client.anon_token())
        return (
            f"{self._client.api_base_url()}/public/"
            f"{encoded_storage_component(project_id)}/"
            f"{encoded_storage_component(self._name)}/"
            f"{encoded_storage_path(object_path)}"
        )


class Storage:
    """Entry point for project object storage."""

    def __init__(self, client: StorageContext) -> None:
        """Create a storage facade backed by a client."""
        self._client: StorageContext = client

    def from_(self, bucket: str) -> StorageBucket:
        """Create a facade scoped to a bucket.

        Returns:
            A storage facade bound to the supplied bucket name.

        """
        return StorageBucket(self._client, bucket)
