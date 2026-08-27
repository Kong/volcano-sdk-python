from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="StorageStats")



@_attrs_define
class StorageStats:
    """ Aggregate storage statistics for a project

        Attributes:
            bucket_count (int): Number of storage buckets
            object_count (int): Total number of stored files
            total_size (int): Total storage used in bytes
     """

    bucket_count: int
    object_count: int
    total_size: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        bucket_count = self.bucket_count

        object_count = self.object_count

        total_size = self.total_size


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "bucket_count": bucket_count,
            "object_count": object_count,
            "total_size": total_size,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bucket_count = d.pop("bucket_count")

        object_count = d.pop("object_count")

        total_size = d.pop("total_size")

        storage_stats = cls(
            bucket_count=bucket_count,
            object_count=object_count,
            total_size=total_size,
        )


        storage_stats.additional_properties = d
        return storage_stats

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
