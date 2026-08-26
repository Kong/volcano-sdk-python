from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="CreateUploadSessionResponse")



@_attrs_define
class CreateUploadSessionResponse:
    """ Response when creating an upload session

        Attributes:
            session_id (str | Unset): Upload session ID Example: session-abc123.
            part_size (int | Unset): Actual part size to use Example: 26214400.
            total_parts (int | Unset): Number of parts to upload Example: 52.
            expires_at (datetime.datetime | Unset): When the session expires (7 days from creation) Example:
                2024-01-22T10:30:00Z.
     """

    session_id: str | Unset = UNSET
    part_size: int | Unset = UNSET
    total_parts: int | Unset = UNSET
    expires_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        session_id = self.session_id

        part_size = self.part_size

        total_parts = self.total_parts

        expires_at: str | Unset = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if part_size is not UNSET:
            field_dict["part_size"] = part_size
        if total_parts is not UNSET:
            field_dict["total_parts"] = total_parts
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        session_id = d.pop("session_id", UNSET)

        part_size = d.pop("part_size", UNSET)

        total_parts = d.pop("total_parts", UNSET)

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: datetime.datetime | Unset
        if isinstance(_expires_at,  Unset):
            expires_at = UNSET
        else:
            expires_at = datetime.datetime.fromisoformat(_expires_at)




        create_upload_session_response = cls(
            session_id=session_id,
            part_size=part_size,
            total_parts=total_parts,
            expires_at=expires_at,
        )


        create_upload_session_response.additional_properties = d
        return create_upload_session_response

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
