from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_import_disposition import check_project_import_disposition
from ..models.project_import_disposition import ProjectImportDisposition
from ..models.project_import_impact import check_project_import_impact
from ..models.project_import_impact import ProjectImportImpact
from typing import cast

if TYPE_CHECKING:
  from ..models.project_import_resource import ProjectImportResource





T = TypeVar("T", bound="ProjectImportFinding")



@_attrs_define
class ProjectImportFinding:
    """ 
        Attributes:
            code (str):
            resource (ProjectImportResource):
            disposition (ProjectImportDisposition):
            impact (ProjectImportImpact):
            message (str):
            remediation (str):
     """

    code: str
    resource: ProjectImportResource
    disposition: ProjectImportDisposition
    impact: ProjectImportImpact
    message: str
    remediation: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_import_resource import ProjectImportResource
        code = self.code

        resource = self.resource.to_dict()

        disposition: str = self.disposition

        impact: str = self.impact

        message = self.message

        remediation = self.remediation


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "code": code,
            "resource": resource,
            "disposition": disposition,
            "impact": impact,
            "message": message,
            "remediation": remediation,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_import_resource import ProjectImportResource
        d = dict(src_dict)
        code = d.pop("code")

        resource = ProjectImportResource.from_dict(d.pop("resource"))




        disposition = check_project_import_disposition(d.pop("disposition"))




        impact = check_project_import_impact(d.pop("impact"))




        message = d.pop("message")

        remediation = d.pop("remediation")

        project_import_finding = cls(
            code=code,
            resource=resource,
            disposition=disposition,
            impact=impact,
            message=message,
            remediation=remediation,
        )


        project_import_finding.additional_properties = d
        return project_import_finding

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
