from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.deployment_phase_name import check_deployment_phase_name
from ..models.deployment_phase_name import DeploymentPhaseName
from ..models.deployment_phase_status import check_deployment_phase_status
from ..models.deployment_phase_status import DeploymentPhaseStatus
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="DeploymentPhase")



@_attrs_define
class DeploymentPhase:
    """ Timing and outcome for one normalized deployment pipeline phase.

        Attributes:
            name (DeploymentPhaseName):
            status (DeploymentPhaseStatus):
            started_at (datetime.datetime | Unset):
            completed_at (datetime.datetime | Unset):
            duration_seconds (int | Unset):
     """

    name: DeploymentPhaseName
    status: DeploymentPhaseStatus
    started_at: datetime.datetime | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET
    duration_seconds: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name: str = self.name

        status: str = self.status

        started_at: str | Unset = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        duration_seconds = self.duration_seconds


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "status": status,
        })
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if duration_seconds is not UNSET:
            field_dict["duration_seconds"] = duration_seconds

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = check_deployment_phase_name(d.pop("name"))




        status = check_deployment_phase_status(d.pop("status"))




        _started_at = d.pop("started_at", UNSET)
        started_at: datetime.datetime | Unset
        if isinstance(_started_at,  Unset):
            started_at = UNSET
        else:
            started_at = datetime.datetime.fromisoformat(_started_at)




        _completed_at = d.pop("completed_at", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at,  Unset):
            completed_at = UNSET
        else:
            completed_at = datetime.datetime.fromisoformat(_completed_at)




        duration_seconds = d.pop("duration_seconds", UNSET)

        deployment_phase = cls(
            name=name,
            status=status,
            started_at=started_at,
            completed_at=completed_at,
            duration_seconds=duration_seconds,
        )


        deployment_phase.additional_properties = d
        return deployment_phase

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
