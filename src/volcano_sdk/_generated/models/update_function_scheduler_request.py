from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.schedule_request import ScheduleRequest
  from ..models.update_function_scheduler_request_payload import UpdateFunctionSchedulerRequestPayload





T = TypeVar("T", bound="UpdateFunctionSchedulerRequest")



@_attrs_define
class UpdateFunctionSchedulerRequest:
    """ 
        Attributes:
            name (str | Unset):
            enabled (bool | Unset):
            schedule (ScheduleRequest | Unset):
            payload (UpdateFunctionSchedulerRequestPayload | Unset):
            regions (list[str] | Unset):
     """

    name: str | Unset = UNSET
    enabled: bool | Unset = UNSET
    schedule: ScheduleRequest | Unset = UNSET
    payload: UpdateFunctionSchedulerRequestPayload | Unset = UNSET
    regions: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.schedule_request import ScheduleRequest
        from ..models.update_function_scheduler_request_payload import UpdateFunctionSchedulerRequestPayload
        name = self.name

        enabled = self.enabled

        schedule: dict[str, Any] | Unset = UNSET
        if not isinstance(self.schedule, Unset):
            schedule = self.schedule.to_dict()

        payload: dict[str, Any] | Unset = UNSET
        if not isinstance(self.payload, Unset):
            payload = self.payload.to_dict()

        regions: list[str] | Unset = UNSET
        if not isinstance(self.regions, Unset):
            regions = self.regions




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if payload is not UNSET:
            field_dict["payload"] = payload
        if regions is not UNSET:
            field_dict["regions"] = regions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schedule_request import ScheduleRequest
        from ..models.update_function_scheduler_request_payload import UpdateFunctionSchedulerRequestPayload
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        enabled = d.pop("enabled", UNSET)

        _schedule = d.pop("schedule", UNSET)
        schedule: ScheduleRequest | Unset
        if isinstance(_schedule,  Unset):
            schedule = UNSET
        else:
            schedule = ScheduleRequest.from_dict(_schedule)




        _payload = d.pop("payload", UNSET)
        payload: UpdateFunctionSchedulerRequestPayload | Unset
        if isinstance(_payload,  Unset):
            payload = UNSET
        else:
            payload = UpdateFunctionSchedulerRequestPayload.from_dict(_payload)




        regions = cast(list[str], d.pop("regions", UNSET))


        update_function_scheduler_request = cls(
            name=name,
            enabled=enabled,
            schedule=schedule,
            payload=payload,
            regions=regions,
        )


        update_function_scheduler_request.additional_properties = d
        return update_function_scheduler_request

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
