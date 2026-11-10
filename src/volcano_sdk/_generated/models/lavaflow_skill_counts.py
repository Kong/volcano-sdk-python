from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowSkillCounts")



@_attrs_define
class LavaflowSkillCounts:
    """ 
        Attributes:
            helpful (int): Fixes that used the skill and merged as LavaFlow left them.
            harmful (int): Fixes that used the skill and a writer corrected or closed, or whose issue came back.
            used (int): Runs that loaded the skill's body.
     """

    helpful: int
    harmful: int
    used: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        helpful = self.helpful

        harmful = self.harmful

        used = self.used


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "helpful": helpful,
            "harmful": harmful,
            "used": used,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        helpful = d.pop("helpful")

        harmful = d.pop("harmful")

        used = d.pop("used")

        lavaflow_skill_counts = cls(
            helpful=helpful,
            harmful=harmful,
            used=used,
        )


        lavaflow_skill_counts.additional_properties = d
        return lavaflow_skill_counts

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
