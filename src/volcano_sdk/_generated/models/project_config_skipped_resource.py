from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_config_skipped_resource_type import check_project_config_skipped_resource_type
from ..models.project_config_skipped_resource_type import ProjectConfigSkippedResourceType
from typing import cast






T = TypeVar("T", bound="ProjectConfigSkippedResource")



@_attrs_define
class ProjectConfigSkippedResource:
    """ 
        Attributes:
            type_ (ProjectConfigSkippedResourceType):
            name (str):
            reason (str):
     """

    type_: ProjectConfigSkippedResourceType
    name: str
    reason: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        name = self.name

        reason = self.reason


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "name": name,
            "reason": reason,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_project_config_skipped_resource_type(d.pop("type"))




        name = d.pop("name")

        reason = d.pop("reason")

        project_config_skipped_resource = cls(
            type_=type_,
            name=name,
            reason=reason,
        )


        project_config_skipped_resource.additional_properties = d
        return project_config_skipped_resource

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
