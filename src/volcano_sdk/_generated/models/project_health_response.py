from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_health_data_status import check_project_health_data_status
from ..models.project_health_data_status import ProjectHealthDataStatus
from ..models.project_health_status import check_project_health_status
from ..models.project_health_status import ProjectHealthStatus
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.project_health_check import ProjectHealthCheck





T = TypeVar("T", bound="ProjectHealthResponse")



@_attrs_define
class ProjectHealthResponse:
    """ 
        Attributes:
            project_id (UUID):
            status (ProjectHealthStatus):
            observed_at (datetime.datetime):
            fresh_through (datetime.datetime):
            data_status (ProjectHealthDataStatus):
            checks (list[ProjectHealthCheck]):
            findings (list[ProjectHealthCheck]): Top findings ordered by severity, then stable check ID.
     """

    project_id: UUID
    status: ProjectHealthStatus
    observed_at: datetime.datetime
    fresh_through: datetime.datetime
    data_status: ProjectHealthDataStatus
    checks: list[ProjectHealthCheck]
    findings: list[ProjectHealthCheck]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_health_check import ProjectHealthCheck
        project_id = str(self.project_id)

        status: str = self.status

        observed_at = self.observed_at.isoformat()

        fresh_through = self.fresh_through.isoformat()

        data_status: str = self.data_status

        checks = []
        for checks_item_data in self.checks:
            checks_item = checks_item_data.to_dict()
            checks.append(checks_item)



        findings = []
        for findings_item_data in self.findings:
            findings_item = findings_item_data.to_dict()
            findings.append(findings_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "project_id": project_id,
            "status": status,
            "observed_at": observed_at,
            "fresh_through": fresh_through,
            "data_status": data_status,
            "checks": checks,
            "findings": findings,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_health_check import ProjectHealthCheck
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        status = check_project_health_status(d.pop("status"))




        observed_at = datetime.datetime.fromisoformat(d.pop("observed_at"))




        fresh_through = datetime.datetime.fromisoformat(d.pop("fresh_through"))




        data_status = check_project_health_data_status(d.pop("data_status"))




        checks = []
        _checks = d.pop("checks")
        for checks_item_data in (_checks):
            checks_item = ProjectHealthCheck.from_dict(checks_item_data)



            checks.append(checks_item)


        findings = []
        _findings = d.pop("findings")
        for findings_item_data in (_findings):
            findings_item = ProjectHealthCheck.from_dict(findings_item_data)



            findings.append(findings_item)


        project_health_response = cls(
            project_id=project_id,
            status=status,
            observed_at=observed_at,
            fresh_through=fresh_through,
            data_status=data_status,
            checks=checks,
            findings=findings,
        )


        project_health_response.additional_properties = d
        return project_health_response

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
