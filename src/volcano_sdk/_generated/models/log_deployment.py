from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.log_deployment_stage import check_log_deployment_stage
from ..models.log_deployment_stage import LogDeploymentStage
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="LogDeployment")



@_attrs_define
class LogDeployment:
    """ Deployment context associated with a historical deployment log event.

        Attributes:
            id (UUID): Deployment ID associated with the log event.
            stage (LogDeploymentStage | Unset): Deployment stage that produced the log event, when available.
     """

    id: UUID
    stage: LogDeploymentStage | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        stage: str | Unset = UNSET
        if not isinstance(self.stage, Unset):
            stage = self.stage



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
        })
        if stage is not UNSET:
            field_dict["stage"] = stage

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        _stage = d.pop("stage", UNSET)
        stage: LogDeploymentStage | Unset
        if isinstance(_stage,  Unset):
            stage = UNSET
        else:
            stage = check_log_deployment_stage(_stage)




        log_deployment = cls(
            id=id,
            stage=stage,
        )


        log_deployment.additional_properties = d
        return log_deployment

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
