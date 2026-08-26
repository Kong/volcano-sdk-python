from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_health_category import check_project_health_category
from ..models.project_health_category import ProjectHealthCategory
from ..models.project_health_status import check_project_health_status
from ..models.project_health_status import ProjectHealthStatus
from typing import cast

if TYPE_CHECKING:
  from ..models.project_health_evidence import ProjectHealthEvidence
  from ..models.project_health_scope import ProjectHealthScope





T = TypeVar("T", bound="ProjectHealthCheck")



@_attrs_define
class ProjectHealthCheck:
    """ 
        Attributes:
            id (str):
            category (ProjectHealthCategory):
            status (ProjectHealthStatus):
            reason_code (str):
            scope (ProjectHealthScope):
            evidence (ProjectHealthEvidence):
     """

    id: str
    category: ProjectHealthCategory
    status: ProjectHealthStatus
    reason_code: str
    scope: ProjectHealthScope
    evidence: ProjectHealthEvidence
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_health_evidence import ProjectHealthEvidence
        from ..models.project_health_scope import ProjectHealthScope
        id = self.id

        category: str = self.category

        status: str = self.status

        reason_code = self.reason_code

        scope = self.scope.to_dict()

        evidence = self.evidence.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "category": category,
            "status": status,
            "reason_code": reason_code,
            "scope": scope,
            "evidence": evidence,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_health_evidence import ProjectHealthEvidence
        from ..models.project_health_scope import ProjectHealthScope
        d = dict(src_dict)
        id = d.pop("id")

        category = check_project_health_category(d.pop("category"))




        status = check_project_health_status(d.pop("status"))




        reason_code = d.pop("reason_code")

        scope = ProjectHealthScope.from_dict(d.pop("scope"))




        evidence = ProjectHealthEvidence.from_dict(d.pop("evidence"))




        project_health_check = cls(
            id=id,
            category=category,
            status=status,
            reason_code=reason_code,
            scope=scope,
            evidence=evidence,
        )


        project_health_check.additional_properties = d
        return project_health_check

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
