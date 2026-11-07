from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowCodeQualitySettings")



@_attrs_define
class LavaflowCodeQualitySettings:
    """ LavaFlow Code Quality: whether LavaFlow reviews the code each production deploy changes and opens pull requests that
    fix what it confirms.

        Attributes:
            enabled (bool): Whether Code Quality reviews the project's deploys. Off by default. It reads as off while the
                project points at another repository than the one it was turned on for, and works only while LavaFlow is on.
     """

    enabled: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "enabled": enabled,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        lavaflow_code_quality_settings = cls(
            enabled=enabled,
        )


        lavaflow_code_quality_settings.additional_properties = d
        return lavaflow_code_quality_settings

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
