from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UploadSessionPart")



@_attrs_define
class UploadSessionPart:
    """ Information about an uploaded part

        Attributes:
            part_number (int | Unset): Part number (1-10000)
            etag (str | Unset): ETag of the uploaded part
            size (int | Unset): Size of the part in bytes
     """

    part_number: int | Unset = UNSET
    etag: str | Unset = UNSET
    size: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        part_number = self.part_number

        etag = self.etag

        size = self.size


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if part_number is not UNSET:
            field_dict["part_number"] = part_number
        if etag is not UNSET:
            field_dict["etag"] = etag
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        part_number = d.pop("part_number", UNSET)

        etag = d.pop("etag", UNSET)

        size = d.pop("size", UNSET)

        upload_session_part = cls(
            part_number=part_number,
            etag=etag,
            size=size,
        )


        upload_session_part.additional_properties = d
        return upload_session_part

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
