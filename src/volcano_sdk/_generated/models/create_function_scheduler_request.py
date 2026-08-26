from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_function_scheduler_request_payload import CreateFunctionSchedulerRequestPayload
  from ..models.schedule_request import ScheduleRequest





T = TypeVar("T", bound="CreateFunctionSchedulerRequest")



@_attrs_define
class CreateFunctionSchedulerRequest:
    """ 
        Attributes:
            name (str):
            schedule (ScheduleRequest):
            enabled (bool | Unset):  Default: True.
            payload (CreateFunctionSchedulerRequestPayload | Unset):
            regions (list[str] | Unset): Optional single explicit deployed region. If omitted, the scheduler chooses one
                deployed region and invokes according to the cron expression.
     """

    name: str
    schedule: ScheduleRequest
    enabled: bool | Unset = True
    payload: CreateFunctionSchedulerRequestPayload | Unset = UNSET
    regions: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_function_scheduler_request_payload import CreateFunctionSchedulerRequestPayload
        from ..models.schedule_request import ScheduleRequest
        name = self.name

        schedule = self.schedule.to_dict()

        enabled = self.enabled

        payload: dict[str, Any] | Unset = UNSET
        if not isinstance(self.payload, Unset):
            payload = self.payload.to_dict()

        regions: list[str] | Unset = UNSET
        if not isinstance(self.regions, Unset):
            regions = self.regions




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "schedule": schedule,
        })
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if payload is not UNSET:
            field_dict["payload"] = payload
        if regions is not UNSET:
            field_dict["regions"] = regions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_function_scheduler_request_payload import CreateFunctionSchedulerRequestPayload
        from ..models.schedule_request import ScheduleRequest
        d = dict(src_dict)
        name = d.pop("name")

        schedule = ScheduleRequest.from_dict(d.pop("schedule"))




        enabled = d.pop("enabled", UNSET)

        _payload = d.pop("payload", UNSET)
        payload: CreateFunctionSchedulerRequestPayload | Unset
        if isinstance(_payload,  Unset):
            payload = UNSET
        else:
            payload = CreateFunctionSchedulerRequestPayload.from_dict(_payload)




        regions = cast(list[str], d.pop("regions", UNSET))


        create_function_scheduler_request = cls(
            name=name,
            schedule=schedule,
            enabled=enabled,
            payload=payload,
            regions=regions,
        )


        create_function_scheduler_request.additional_properties = d
        return create_function_scheduler_request

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
