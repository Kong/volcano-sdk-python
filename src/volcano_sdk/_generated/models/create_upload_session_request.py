from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateUploadSessionRequest")



@_attrs_define
class CreateUploadSessionRequest:
    """ Request to create a resumable upload session

        Attributes:
            object_path (str): Target file path within the bucket Example: videos/large-file.mp4.
            content_type (str): MIME type of the file Example: video/mp4.
            total_size (int): Total file size in bytes (max 5TB) Example: 5368709120.
            part_size (int | Unset): Part size in bytes (default: 25MB, min: 5MB, max: 25MB) Example: 26214400.
     """

    object_path: str
    content_type: str
    total_size: int
    part_size: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        object_path = self.object_path

        content_type = self.content_type

        total_size = self.total_size

        part_size = self.part_size


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "object_path": object_path,
            "content_type": content_type,
            "total_size": total_size,
        })
        if part_size is not UNSET:
            field_dict["part_size"] = part_size

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        object_path = d.pop("object_path")

        content_type = d.pop("content_type")

        total_size = d.pop("total_size")

        part_size = d.pop("part_size", UNSET)

        create_upload_session_request = cls(
            object_path=object_path,
            content_type=content_type,
            total_size=total_size,
            part_size=part_size,
        )


        create_upload_session_request.additional_properties = d
        return create_upload_session_request

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
