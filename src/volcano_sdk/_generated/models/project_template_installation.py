from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_template_installation_phase import check_project_template_installation_phase
from ..models.project_template_installation_phase import ProjectTemplateInstallationPhase
from ..models.project_template_installation_status import check_project_template_installation_status
from ..models.project_template_installation_status import ProjectTemplateInstallationStatus
from typing import cast






T = TypeVar("T", bound="ProjectTemplateInstallation")



@_attrs_define
class ProjectTemplateInstallation:
    """ Template initialization progress, returned by project creation and the
    individual project endpoint. Omitted for projects without a template.
    Project creation accepts the installation; wait for `ready` before use.
    A failed installation retains the project for inspection or deletion.

        Attributes:
            status (ProjectTemplateInstallationStatus):
            phase (ProjectTemplateInstallationPhase):
     """

    status: ProjectTemplateInstallationStatus
    phase: ProjectTemplateInstallationPhase
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        status: str = self.status

        phase: str = self.phase


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "status": status,
            "phase": phase,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = check_project_template_installation_status(d.pop("status"))




        phase = check_project_template_installation_phase(d.pop("phase"))




        project_template_installation = cls(
            status=status,
            phase=phase,
        )


        project_template_installation.additional_properties = d
        return project_template_installation

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
