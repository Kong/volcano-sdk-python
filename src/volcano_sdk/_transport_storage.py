"""Generated storage operation adapters."""

from __future__ import annotations

from io import BytesIO
from pathlib import PurePosixPath
from typing import TYPE_CHECKING

from ._generated.api.storage_objects import (
    copy_storage_object,
    delete_storage_object,
    download_storage_object,
    list_storage_objects,
    move_storage_object,
    update_storage_object_visibility,
    upload_part,
    upload_storage_object,
)
from ._generated.models.create_upload_session_request import CreateUploadSessionRequest
from ._generated.models.storage_copy_request import StorageCopyRequest
from ._generated.models.storage_move_request import StorageMoveRequest
from ._generated.models.storage_visibility_request import StorageVisibilityRequest
from ._generated.models.upload_storage_object_files_body import (
    UploadStorageObjectFilesBody,
)
from ._generated.types import UNSET, File
from ._transport_base import TransportBase
from ._transport_response import (
    parsed_response,
    unparsed_response,
)

if TYPE_CHECKING:
    from ._transport_types import (
        StorageUploadPartRequest,
        StorageUploadSessionReference,
        StorageUploadSessionRequest,
        TransportResponse,
    )


class StorageTransport(TransportBase):
    """Adapt generated storage operations to the SDK transport."""

    def upload_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> TransportResponse:
        file_name = PurePosixPath(path).name or "file"
        body = UploadStorageObjectFilesBody(
            file=File(
                payload=BytesIO(data),
                file_name=file_name,
                mime_type=content_type,
            )
        )
        with self._client(authorization) as client:
            response = upload_storage_object.sync_detailed(
                bucket_name,
                path,
                client=client,
                body=body,
            )
        return parsed_response(response)

    def create_upload_session(
        self,
        *,
        authorization: str,
        bucket_name: str,
        request: StorageUploadSessionRequest,
    ) -> TransportResponse:
        body = CreateUploadSessionRequest(
            object_path=request.path,
            content_type=request.content_type,
            total_size=request.total_size,
            part_size=request.part_size if request.part_size is not None else UNSET,
        )
        with self._client(authorization) as client:
            response = upload_storage_object.sync_detailed(
                bucket_name,
                request.path,
                client=client,
                body=body,
            )
        return parsed_response(response)

    def upload_part(
        self,
        *,
        authorization: str,
        bucket_name: str,
        request: StorageUploadPartRequest,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = upload_part.sync_detailed(
                bucket_name,
                request.path,
                client=client,
                body=File(payload=BytesIO(request.data)),
                x_upload_session=request.session_id,
                x_part_number=request.part_number,
            )
        return parsed_response(response)

    def complete_upload_session(
        self,
        *,
        authorization: str,
        bucket_name: str,
        request: StorageUploadSessionReference,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = upload_storage_object.sync_detailed(
                bucket_name,
                request.path,
                client=client,
                x_upload_session=request.session_id,
                x_upload_complete="true",
            )
        return parsed_response(response)

    def get_upload_session(
        self,
        *,
        authorization: str,
        bucket_name: str,
        request: StorageUploadSessionReference,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = download_storage_object.sync_detailed(
                bucket_name,
                request.path,
                client=client,
                x_upload_session=request.session_id,
            )
        return unparsed_response(response)

    def abort_upload_session(
        self,
        *,
        authorization: str,
        bucket_name: str,
        request: StorageUploadSessionReference,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = delete_storage_object.sync_detailed(
                bucket_name,
                request.path,
                client=client,
                x_upload_session=request.session_id,
            )
        return parsed_response(response)

    def download_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
        byte_range: str | None = None,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = download_storage_object.sync_detailed(
                bucket_name,
                path,
                client=client,
                range_=byte_range if byte_range is not None else UNSET,
            )
        return parsed_response(response)

    def list_storage_objects(
        self,
        *,
        authorization: str,
        bucket_name: str,
        prefix: str,
        limit: int | None,
        cursor: str | None,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = list_storage_objects.sync_detailed(
                bucket_name,
                client=client,
                prefix=prefix or UNSET,
                limit=limit if limit is not None else UNSET,
                cursor=cursor if cursor is not None else UNSET,
            )
        return parsed_response(response)

    def delete_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = delete_storage_object.sync_detailed(
                bucket_name,
                path,
                client=client,
            )
        return parsed_response(response)

    def move_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        from_path: str,
        to_path: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = move_storage_object.sync_detailed(
                bucket_name,
                client=client,
                body=StorageMoveRequest(from_=from_path, to=to_path),
            )
        return parsed_response(response)

    def copy_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        from_path: str,
        to_path: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = copy_storage_object.sync_detailed(
                bucket_name,
                client=client,
                body=StorageCopyRequest(from_=from_path, to=to_path),
            )
        return parsed_response(response)

    def update_storage_object_visibility(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
        is_public: bool,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = update_storage_object_visibility.sync_detailed(
                bucket_name,
                path,
                client=client,
                body=StorageVisibilityRequest(is_public=is_public),
            )
        return parsed_response(response)
