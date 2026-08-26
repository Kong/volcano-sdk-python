from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.deployment_progress_current_phase import check_deployment_progress_current_phase
from ..models.deployment_progress_current_phase import DeploymentProgressCurrentPhase
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.deployment_phase import DeploymentPhase





T = TypeVar("T", bound="DeploymentProgress")



@_attrs_define
class DeploymentProgress:
    """ Normalized live progress derived from the deployment workflow and build phases.

        Attributes:
            started_at (datetime.datetime):
            elapsed_seconds (int):
            phases (list[DeploymentPhase]):
            updated_at (datetime.datetime):
            current_phase (DeploymentProgressCurrentPhase | Unset):
            completed_at (datetime.datetime | Unset):
     """

    started_at: datetime.datetime
    elapsed_seconds: int
    phases: list[DeploymentPhase]
    updated_at: datetime.datetime
    current_phase: DeploymentProgressCurrentPhase | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.deployment_phase import DeploymentPhase
        started_at = self.started_at.isoformat()

        elapsed_seconds = self.elapsed_seconds

        phases = []
        for phases_item_data in self.phases:
            phases_item = phases_item_data.to_dict()
            phases.append(phases_item)



        updated_at = self.updated_at.isoformat()

        current_phase: str | Unset = UNSET
        if not isinstance(self.current_phase, Unset):
            current_phase = self.current_phase


        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "started_at": started_at,
            "elapsed_seconds": elapsed_seconds,
            "phases": phases,
            "updated_at": updated_at,
        })
        if current_phase is not UNSET:
            field_dict["current_phase"] = current_phase
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.deployment_phase import DeploymentPhase
        d = dict(src_dict)
        started_at = datetime.datetime.fromisoformat(d.pop("started_at"))




        elapsed_seconds = d.pop("elapsed_seconds")

        phases = []
        _phases = d.pop("phases")
        for phases_item_data in (_phases):
            phases_item = DeploymentPhase.from_dict(phases_item_data)



            phases.append(phases_item)


        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        _current_phase = d.pop("current_phase", UNSET)
        current_phase: DeploymentProgressCurrentPhase | Unset
        if isinstance(_current_phase,  Unset):
            current_phase = UNSET
        else:
            current_phase = check_deployment_progress_current_phase(_current_phase)




        _completed_at = d.pop("completed_at", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at,  Unset):
            completed_at = UNSET
        else:
            completed_at = datetime.datetime.fromisoformat(_completed_at)




        deployment_progress = cls(
            started_at=started_at,
            elapsed_seconds=elapsed_seconds,
            phases=phases,
            updated_at=updated_at,
            current_phase=current_phase,
            completed_at=completed_at,
        )


        deployment_progress.additional_properties = d
        return deployment_progress

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
