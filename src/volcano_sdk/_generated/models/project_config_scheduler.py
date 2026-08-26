from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_config_scheduler_payload import ProjectConfigSchedulerPayload





T = TypeVar("T", bound="ProjectConfigScheduler")



@_attrs_define
class ProjectConfigScheduler:
    """ 
        Attributes:
            name (str):
            cron (str): 5-field UTC cron expression
            enabled (bool | Unset):
            payload (ProjectConfigSchedulerPayload | Unset):
     """

    name: str
    cron: str
    enabled: bool | Unset = UNSET
    payload: ProjectConfigSchedulerPayload | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_scheduler_payload import ProjectConfigSchedulerPayload
        name = self.name

        cron = self.cron

        enabled = self.enabled

        payload: dict[str, Any] | Unset = UNSET
        if not isinstance(self.payload, Unset):
            payload = self.payload.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
            "cron": cron,
        })
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if payload is not UNSET:
            field_dict["payload"] = payload

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_scheduler_payload import ProjectConfigSchedulerPayload
        d = dict(src_dict)
        name = d.pop("name")

        cron = d.pop("cron")

        enabled = d.pop("enabled", UNSET)

        _payload = d.pop("payload", UNSET)
        payload: ProjectConfigSchedulerPayload | Unset
        if isinstance(_payload,  Unset):
            payload = UNSET
        else:
            payload = ProjectConfigSchedulerPayload.from_dict(_payload)




        project_config_scheduler = cls(
            name=name,
            cron=cron,
            enabled=enabled,
            payload=payload,
        )

        return project_config_scheduler

