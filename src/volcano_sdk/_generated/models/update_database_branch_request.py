from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="UpdateDatabaseBranchRequest")



@_attrs_define
class UpdateDatabaseBranchRequest:
    """ Replace the branch's lifetime and restart its countdown from now.

        Attributes:
            ttl_seconds (int): The new lifetime, between one hour and 30 days. Example: 86400.
     """

    ttl_seconds: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        ttl_seconds = self.ttl_seconds


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "ttl_seconds": ttl_seconds,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ttl_seconds = d.pop("ttl_seconds")

        update_database_branch_request = cls(
            ttl_seconds=ttl_seconds,
        )


        update_database_branch_request.additional_properties = d
        return update_database_branch_request

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
