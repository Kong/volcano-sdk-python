from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="FunctionRegion")



@_attrs_define
class FunctionRegion:
    """ 
        Attributes:
            code (str): Region identifier accepted by function APIs. Example: us-east-1.
            label (str): Human-readable region label suitable for display in pickers. Example: NA-East.
            flag (str): Country flag emoji associated with the region's geography. Example: 🇺🇸.
     """

    code: str
    label: str
    flag: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        code = self.code

        label = self.label

        flag = self.flag


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "code": code,
            "label": label,
            "flag": flag,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        label = d.pop("label")

        flag = d.pop("flag")

        function_region = cls(
            code=code,
            label=label,
            flag=flag,
        )


        function_region.additional_properties = d
        return function_region

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
