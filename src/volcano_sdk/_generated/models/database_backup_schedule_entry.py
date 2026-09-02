from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.database_backup_schedule_entry_frequency import check_database_backup_schedule_entry_frequency
from ..models.database_backup_schedule_entry_frequency import DatabaseBackupScheduleEntryFrequency
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="DatabaseBackupScheduleEntry")



@_attrs_define
class DatabaseBackupScheduleEntry:
    """ One recurrence of the automated backup schedule.

        Attributes:
            frequency (DatabaseBackupScheduleEntryFrequency):
            hour (int): Hour of the day in UTC.
            day (int | Unset): Day of the week (1-7, Monday to Sunday) for a weekly schedule, or day
                of the month (1-28) for a monthly one. Required for both, ignored for
                a daily schedule. Monthly stops at 28 so the schedule fires in every
                month.
            retention_seconds (int | Unset): How long each backup from this recurrence is kept. Clamped to the
                plan's retention, and defaulted to it when omitted.
     """

    frequency: DatabaseBackupScheduleEntryFrequency
    hour: int
    day: int | Unset = UNSET
    retention_seconds: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        frequency: str = self.frequency

        hour = self.hour

        day = self.day

        retention_seconds = self.retention_seconds


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "frequency": frequency,
            "hour": hour,
        })
        if day is not UNSET:
            field_dict["day"] = day
        if retention_seconds is not UNSET:
            field_dict["retention_seconds"] = retention_seconds

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        frequency = check_database_backup_schedule_entry_frequency(d.pop("frequency"))




        hour = d.pop("hour")

        day = d.pop("day", UNSET)

        retention_seconds = d.pop("retention_seconds", UNSET)

        database_backup_schedule_entry = cls(
            frequency=frequency,
            hour=hour,
            day=day,
            retention_seconds=retention_seconds,
        )


        database_backup_schedule_entry.additional_properties = d
        return database_backup_schedule_entry

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
