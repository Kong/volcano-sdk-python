from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.function_scheduler_schedule_kind import check_function_scheduler_schedule_kind
from ..models.function_scheduler_schedule_kind import FunctionSchedulerScheduleKind
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.function_scheduler_payload import FunctionSchedulerPayload





T = TypeVar("T", bound="FunctionScheduler")



@_attrs_define
class FunctionScheduler:
    """ 
        Attributes:
            id (UUID | Unset):
            project_id (UUID | Unset):
            function_id (UUID | Unset):
            name (str | Unset):
            enabled (bool | Unset):
            schedule_kind (FunctionSchedulerScheduleKind | Unset):
            cron_expression (str | Unset):
            payload (FunctionSchedulerPayload | Unset):
            regions (list[str] | Unset):
            regions_explicit (bool | Unset):
            next_run_at (datetime.datetime | Unset):
            last_started_at (datetime.datetime | Unset):
            last_completed_at (datetime.datetime | Unset):
            last_error (str | Unset):
            run_count (int | Unset): Total number of times this scheduler has executed. 0 for a scheduler that has never
                run.
            created_at (datetime.datetime | Unset):
            updated_at (datetime.datetime | Unset):
     """

    id: UUID | Unset = UNSET
    project_id: UUID | Unset = UNSET
    function_id: UUID | Unset = UNSET
    name: str | Unset = UNSET
    enabled: bool | Unset = UNSET
    schedule_kind: FunctionSchedulerScheduleKind | Unset = UNSET
    cron_expression: str | Unset = UNSET
    payload: FunctionSchedulerPayload | Unset = UNSET
    regions: list[str] | Unset = UNSET
    regions_explicit: bool | Unset = UNSET
    next_run_at: datetime.datetime | Unset = UNSET
    last_started_at: datetime.datetime | Unset = UNSET
    last_completed_at: datetime.datetime | Unset = UNSET
    last_error: str | Unset = UNSET
    run_count: int | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.function_scheduler_payload import FunctionSchedulerPayload
        id: str | Unset = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        project_id: str | Unset = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        function_id: str | Unset = UNSET
        if not isinstance(self.function_id, Unset):
            function_id = str(self.function_id)

        name = self.name

        enabled = self.enabled

        schedule_kind: str | Unset = UNSET
        if not isinstance(self.schedule_kind, Unset):
            schedule_kind = self.schedule_kind


        cron_expression = self.cron_expression

        payload: dict[str, Any] | Unset = UNSET
        if not isinstance(self.payload, Unset):
            payload = self.payload.to_dict()

        regions: list[str] | Unset = UNSET
        if not isinstance(self.regions, Unset):
            regions = self.regions



        regions_explicit = self.regions_explicit

        next_run_at: str | Unset = UNSET
        if not isinstance(self.next_run_at, Unset):
            next_run_at = self.next_run_at.isoformat()

        last_started_at: str | Unset = UNSET
        if not isinstance(self.last_started_at, Unset):
            last_started_at = self.last_started_at.isoformat()

        last_completed_at: str | Unset = UNSET
        if not isinstance(self.last_completed_at, Unset):
            last_completed_at = self.last_completed_at.isoformat()

        last_error = self.last_error

        run_count = self.run_count

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if function_id is not UNSET:
            field_dict["function_id"] = function_id
        if name is not UNSET:
            field_dict["name"] = name
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if schedule_kind is not UNSET:
            field_dict["schedule_kind"] = schedule_kind
        if cron_expression is not UNSET:
            field_dict["cron_expression"] = cron_expression
        if payload is not UNSET:
            field_dict["payload"] = payload
        if regions is not UNSET:
            field_dict["regions"] = regions
        if regions_explicit is not UNSET:
            field_dict["regions_explicit"] = regions_explicit
        if next_run_at is not UNSET:
            field_dict["next_run_at"] = next_run_at
        if last_started_at is not UNSET:
            field_dict["last_started_at"] = last_started_at
        if last_completed_at is not UNSET:
            field_dict["last_completed_at"] = last_completed_at
        if last_error is not UNSET:
            field_dict["last_error"] = last_error
        if run_count is not UNSET:
            field_dict["run_count"] = run_count
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.function_scheduler_payload import FunctionSchedulerPayload
        d = dict(src_dict)
        _id = d.pop("id", UNSET)
        id: UUID | Unset
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        _project_id = d.pop("project_id", UNSET)
        project_id: UUID | Unset
        if isinstance(_project_id,  Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)




        _function_id = d.pop("function_id", UNSET)
        function_id: UUID | Unset
        if isinstance(_function_id,  Unset):
            function_id = UNSET
        else:
            function_id = UUID(_function_id)




        name = d.pop("name", UNSET)

        enabled = d.pop("enabled", UNSET)

        _schedule_kind = d.pop("schedule_kind", UNSET)
        schedule_kind: FunctionSchedulerScheduleKind | Unset
        if isinstance(_schedule_kind,  Unset):
            schedule_kind = UNSET
        else:
            schedule_kind = check_function_scheduler_schedule_kind(_schedule_kind)




        cron_expression = d.pop("cron_expression", UNSET)

        _payload = d.pop("payload", UNSET)
        payload: FunctionSchedulerPayload | Unset
        if isinstance(_payload,  Unset):
            payload = UNSET
        else:
            payload = FunctionSchedulerPayload.from_dict(_payload)




        regions = cast(list[str], d.pop("regions", UNSET))


        regions_explicit = d.pop("regions_explicit", UNSET)

        _next_run_at = d.pop("next_run_at", UNSET)
        next_run_at: datetime.datetime | Unset
        if isinstance(_next_run_at,  Unset):
            next_run_at = UNSET
        else:
            next_run_at = datetime.datetime.fromisoformat(_next_run_at)




        _last_started_at = d.pop("last_started_at", UNSET)
        last_started_at: datetime.datetime | Unset
        if isinstance(_last_started_at,  Unset):
            last_started_at = UNSET
        else:
            last_started_at = datetime.datetime.fromisoformat(_last_started_at)




        _last_completed_at = d.pop("last_completed_at", UNSET)
        last_completed_at: datetime.datetime | Unset
        if isinstance(_last_completed_at,  Unset):
            last_completed_at = UNSET
        else:
            last_completed_at = datetime.datetime.fromisoformat(_last_completed_at)




        last_error = d.pop("last_error", UNSET)

        run_count = d.pop("run_count", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)




        _updated_at = d.pop("updated_at", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at,  Unset):
            updated_at = UNSET
        else:
            updated_at = datetime.datetime.fromisoformat(_updated_at)




        function_scheduler = cls(
            id=id,
            project_id=project_id,
            function_id=function_id,
            name=name,
            enabled=enabled,
            schedule_kind=schedule_kind,
            cron_expression=cron_expression,
            payload=payload,
            regions=regions,
            regions_explicit=regions_explicit,
            next_run_at=next_run_at,
            last_started_at=last_started_at,
            last_completed_at=last_completed_at,
            last_error=last_error,
            run_count=run_count,
            created_at=created_at,
            updated_at=updated_at,
        )


        function_scheduler.additional_properties = d
        return function_scheduler

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
