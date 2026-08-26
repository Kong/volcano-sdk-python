from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_import_destination_mode import check_project_import_destination_mode
from ..models.project_import_destination_mode import ProjectImportDestinationMode
from ..models.project_import_target import check_project_import_target
from ..models.project_import_target import ProjectImportTarget
from typing import cast






T = TypeVar("T", bound="ProjectImportDestination")



@_attrs_define
class ProjectImportDestination:
    """ 
        Attributes:
            mode (ProjectImportDestinationMode):
            project_name (str):
            target (ProjectImportTarget):
     """

    mode: ProjectImportDestinationMode
    project_name: str
    target: ProjectImportTarget
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        mode: str = self.mode

        project_name = self.project_name

        target: str = self.target


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "mode": mode,
            "project_name": project_name,
            "target": target,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = check_project_import_destination_mode(d.pop("mode"))




        project_name = d.pop("project_name")

        target = check_project_import_target(d.pop("target"))




        project_import_destination = cls(
            mode=mode,
            project_name=project_name,
            target=target,
        )


        project_import_destination.additional_properties = d
        return project_import_destination

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
