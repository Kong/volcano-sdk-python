from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ProjectSourceExportSkip")



@_attrs_define
class ProjectSourceExportSkip:
    """ 
        Attributes:
            kind (str): The kind of resource, "function" or "frontend". Deliberately not an enum: the generated constants
                would collide with an existing resource-type enum and rename its members.
            name (str):
            reason (str):
     """

    kind: str
    name: str
    reason: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        kind = self.kind

        name = self.name

        reason = self.reason


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "kind": kind,
            "name": name,
            "reason": reason,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = d.pop("kind")

        name = d.pop("name")

        reason = d.pop("reason")

        project_source_export_skip = cls(
            kind=kind,
            name=name,
            reason=reason,
        )


        project_source_export_skip.additional_properties = d
        return project_source_export_skip

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
