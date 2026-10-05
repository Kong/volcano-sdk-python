from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ProjectSourceExportOmission")



@_attrs_define
class ProjectSourceExportOmission:
    """ 
        Attributes:
            kind (str): What was left out: migrations Volcano stores no copy of, variable values, a credential-shaped file,
                installed dependencies, or an archive entry a repository cannot carry.
            resource (str): The resource it came from, empty when project-wide.
            path (str):
     """

    kind: str
    resource: str
    path: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        kind = self.kind

        resource = self.resource

        path = self.path


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "kind": kind,
            "resource": resource,
            "path": path,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = d.pop("kind")

        resource = d.pop("resource")

        path = d.pop("path")

        project_source_export_omission = cls(
            kind=kind,
            resource=resource,
            path=path,
        )


        project_source_export_omission.additional_properties = d
        return project_source_export_omission

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
