from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="LavaflowGlobalSkillAppliesTo")



@_attrs_define
class LavaflowGlobalSkillAppliesTo:
    """ Where a global skill applies. Empty lists apply it to every project.

        Attributes:
            runtimes (list[str]):
            frameworks (list[str]):
            resource_types (list[str]):
     """

    runtimes: list[str]
    frameworks: list[str]
    resource_types: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        runtimes = self.runtimes



        frameworks = self.frameworks



        resource_types = self.resource_types




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "runtimes": runtimes,
            "frameworks": frameworks,
            "resource_types": resource_types,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        runtimes = cast(list[str], d.pop("runtimes"))


        frameworks = cast(list[str], d.pop("frameworks"))


        resource_types = cast(list[str], d.pop("resource_types"))


        lavaflow_global_skill_applies_to = cls(
            runtimes=runtimes,
            frameworks=frameworks,
            resource_types=resource_types,
        )


        lavaflow_global_skill_applies_to.additional_properties = d
        return lavaflow_global_skill_applies_to

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
