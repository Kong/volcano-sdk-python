from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="CreateStorageBucketRequest")



@_attrs_define
class CreateStorageBucketRequest:
    """ 
        Attributes:
            name (str): Bucket name (alphanumeric, dashes, underscores)
            file_size_limit (int | Unset): Maximum file size in bytes
            allowed_mime_types (list[str] | Unset): Allowed MIME types (e.g., ["image/png", "image/jpeg"])
     """

    name: str
    file_size_limit: int | Unset = UNSET
    allowed_mime_types: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        file_size_limit = self.file_size_limit

        allowed_mime_types: list[str] | Unset = UNSET
        if not isinstance(self.allowed_mime_types, Unset):
            allowed_mime_types = self.allowed_mime_types




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
        })
        if file_size_limit is not UNSET:
            field_dict["file_size_limit"] = file_size_limit
        if allowed_mime_types is not UNSET:
            field_dict["allowed_mime_types"] = allowed_mime_types

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        file_size_limit = d.pop("file_size_limit", UNSET)

        allowed_mime_types = cast(list[str], d.pop("allowed_mime_types", UNSET))


        create_storage_bucket_request = cls(
            name=name,
            file_size_limit=file_size_limit,
            allowed_mime_types=allowed_mime_types,
        )


        create_storage_bucket_request.additional_properties = d
        return create_storage_bucket_request

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
