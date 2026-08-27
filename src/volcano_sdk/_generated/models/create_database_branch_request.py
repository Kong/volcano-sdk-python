from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateDatabaseBranchRequest")



@_attrs_define
class CreateDatabaseBranchRequest:
    """ 
        Attributes:
            name (str): Branch name (must be unique within the parent database) Example: feature_checkout.
            ttl_seconds (int | Unset): How long the branch should live, between one hour and 30 days.
                Defaults to 7 days when omitted.
                 Example: 86400.
     """

    name: str
    ttl_seconds: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        ttl_seconds = self.ttl_seconds


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
        })
        if ttl_seconds is not UNSET:
            field_dict["ttl_seconds"] = ttl_seconds

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        ttl_seconds = d.pop("ttl_seconds", UNSET)

        create_database_branch_request = cls(
            name=name,
            ttl_seconds=ttl_seconds,
        )


        create_database_branch_request.additional_properties = d
        return create_database_branch_request

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
