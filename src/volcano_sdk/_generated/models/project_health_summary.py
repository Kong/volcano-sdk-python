from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_health_status import check_project_health_status
from ..models.project_health_status import ProjectHealthStatus
from typing import cast






T = TypeVar("T", bound="ProjectHealthSummary")



@_attrs_define
class ProjectHealthSummary:
    """ 
        Attributes:
            status (ProjectHealthStatus): empty means no functions, frontends, databases, storage, Volcano Auth users, or
                Sandbox resources are listed. needs_attention means an operation needs review without confirmed service
                impairment, or a serving frontend whose edge recovery gave up needs a redeploy. degraded means a resource is
                only partly available or is unavailable for an expected, temporary reason, such as a frontend whose edge
                synchronization did not complete or a database being restored; critical means use is blocked. A failed workflow
                or deployment record alone does not establish an outage. Findings remain available for empty projects.
     """

    status: ProjectHealthStatus
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        status: str = self.status


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = check_project_health_status(d.pop("status"))




        project_health_summary = cls(
            status=status,
        )


        project_health_summary.additional_properties = d
        return project_health_summary

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
