from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.upload_session_status_response_status import check_upload_session_status_response_status
from ..models.upload_session_status_response_status import UploadSessionStatusResponseStatus
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.upload_session_part import UploadSessionPart





T = TypeVar("T", bound="UploadSessionStatusResponse")



@_attrs_define
class UploadSessionStatusResponse:
    """ Status of an upload session

        Attributes:
            session_id (str | Unset): Upload session ID
            status (UploadSessionStatusResponseStatus | Unset): Current status of the upload
            path (str | Unset): Target file path
            content_type (str | Unset): MIME type
            total_size (int | Unset): Total file size in bytes
            part_size (int | Unset): Size of each part (except last)
            total_parts (int | Unset): Total number of parts
            parts_uploaded (int | Unset): Number of parts uploaded
            bytes_uploaded (int | Unset): Total bytes uploaded so far
            parts (list[UploadSessionPart] | Unset): List of uploaded parts (for resume)
            expires_at (datetime.datetime | Unset): Session expiry time
            created_at (datetime.datetime | Unset): Session creation time
     """

    session_id: str | Unset = UNSET
    status: UploadSessionStatusResponseStatus | Unset = UNSET
    path: str | Unset = UNSET
    content_type: str | Unset = UNSET
    total_size: int | Unset = UNSET
    part_size: int | Unset = UNSET
    total_parts: int | Unset = UNSET
    parts_uploaded: int | Unset = UNSET
    bytes_uploaded: int | Unset = UNSET
    parts: list[UploadSessionPart] | Unset = UNSET
    expires_at: datetime.datetime | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.upload_session_part import UploadSessionPart
        session_id = self.session_id

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status


        path = self.path

        content_type = self.content_type

        total_size = self.total_size

        part_size = self.part_size

        total_parts = self.total_parts

        parts_uploaded = self.parts_uploaded

        bytes_uploaded = self.bytes_uploaded

        parts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.parts, Unset):
            parts = []
            for parts_item_data in self.parts:
                parts_item = parts_item_data.to_dict()
                parts.append(parts_item)



        expires_at: str | Unset = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if status is not UNSET:
            field_dict["status"] = status
        if path is not UNSET:
            field_dict["path"] = path
        if content_type is not UNSET:
            field_dict["content_type"] = content_type
        if total_size is not UNSET:
            field_dict["total_size"] = total_size
        if part_size is not UNSET:
            field_dict["part_size"] = part_size
        if total_parts is not UNSET:
            field_dict["total_parts"] = total_parts
        if parts_uploaded is not UNSET:
            field_dict["parts_uploaded"] = parts_uploaded
        if bytes_uploaded is not UNSET:
            field_dict["bytes_uploaded"] = bytes_uploaded
        if parts is not UNSET:
            field_dict["parts"] = parts
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.upload_session_part import UploadSessionPart
        d = dict(src_dict)
        session_id = d.pop("session_id", UNSET)

        _status = d.pop("status", UNSET)
        status: UploadSessionStatusResponseStatus | Unset
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = check_upload_session_status_response_status(_status)




        path = d.pop("path", UNSET)

        content_type = d.pop("content_type", UNSET)

        total_size = d.pop("total_size", UNSET)

        part_size = d.pop("part_size", UNSET)

        total_parts = d.pop("total_parts", UNSET)

        parts_uploaded = d.pop("parts_uploaded", UNSET)

        bytes_uploaded = d.pop("bytes_uploaded", UNSET)

        _parts = d.pop("parts", UNSET)
        parts: list[UploadSessionPart] | Unset = UNSET
        if _parts is not UNSET:
            parts = []
            for parts_item_data in _parts:
                parts_item = UploadSessionPart.from_dict(parts_item_data)



                parts.append(parts_item)


        _expires_at = d.pop("expires_at", UNSET)
        expires_at: datetime.datetime | Unset
        if isinstance(_expires_at,  Unset):
            expires_at = UNSET
        else:
            expires_at = datetime.datetime.fromisoformat(_expires_at)




        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)




        upload_session_status_response = cls(
            session_id=session_id,
            status=status,
            path=path,
            content_type=content_type,
            total_size=total_size,
            part_size=part_size,
            total_parts=total_parts,
            parts_uploaded=parts_uploaded,
            bytes_uploaded=bytes_uploaded,
            parts=parts,
            expires_at=expires_at,
            created_at=created_at,
        )


        upload_session_status_response.additional_properties = d
        return upload_session_status_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
