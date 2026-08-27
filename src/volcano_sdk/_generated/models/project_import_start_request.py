from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_import_target import check_project_import_target
from ..models.project_import_target import ProjectImportTarget
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ProjectImportStartRequest")



@_attrs_define
class ProjectImportStartRequest:
    """ 
        Attributes:
            connection_id (UUID):
            source_id (str):
            project_name (str):
            target (ProjectImportTarget):
            confirm_environment_variable_read (bool):
            preflight_fingerprint (str):
     """

    connection_id: UUID
    source_id: str
    project_name: str
    target: ProjectImportTarget
    confirm_environment_variable_read: bool
    preflight_fingerprint: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        connection_id = str(self.connection_id)

        source_id = self.source_id

        project_name = self.project_name

        target: str = self.target

        confirm_environment_variable_read = self.confirm_environment_variable_read

        preflight_fingerprint = self.preflight_fingerprint


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "connection_id": connection_id,
            "source_id": source_id,
            "project_name": project_name,
            "target": target,
            "confirm_environment_variable_read": confirm_environment_variable_read,
            "preflight_fingerprint": preflight_fingerprint,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        connection_id = UUID(d.pop("connection_id"))




        source_id = d.pop("source_id")

        project_name = d.pop("project_name")

        target = check_project_import_target(d.pop("target"))




        confirm_environment_variable_read = d.pop("confirm_environment_variable_read")

        preflight_fingerprint = d.pop("preflight_fingerprint")

        project_import_start_request = cls(
            connection_id=connection_id,
            source_id=source_id,
            project_name=project_name,
            target=target,
            confirm_environment_variable_read=confirm_environment_variable_read,
            preflight_fingerprint=preflight_fingerprint,
        )


        project_import_start_request.additional_properties = d
        return project_import_start_request

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
