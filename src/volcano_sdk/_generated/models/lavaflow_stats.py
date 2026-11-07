from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.lavaflow_day_counts import LavaflowDayCounts
  from ..models.lavaflow_stats_totals import LavaflowStatsTotals





T = TypeVar("T", bound="LavaflowStats")



@_attrs_define
class LavaflowStats:
    """ 
        Attributes:
            project_id (UUID): The project the counts are for.
            window_start (datetime.date): The first UTC day in the window.
            window_end (datetime.date): The last UTC day in the window, today.
            days (list[LavaflowDayCounts]): One entry per UTC day, oldest first, zeros included.
            totals (LavaflowStatsTotals):
     """

    project_id: UUID
    window_start: datetime.date
    window_end: datetime.date
    days: list[LavaflowDayCounts]
    totals: LavaflowStatsTotals
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_day_counts import LavaflowDayCounts # noqa: PLC0415
        from ..models.lavaflow_stats_totals import LavaflowStatsTotals # noqa: PLC0415
        project_id = str(self.project_id)

        window_start = self.window_start.isoformat()

        window_end = self.window_end.isoformat()

        days = []
        for days_item_data in self.days:
            days_item = days_item_data.to_dict()
            days.append(days_item)



        totals = self.totals.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "project_id": project_id,
            "window_start": window_start,
            "window_end": window_end,
            "days": days,
            "totals": totals,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_day_counts import LavaflowDayCounts # noqa: PLC0415
        from ..models.lavaflow_stats_totals import LavaflowStatsTotals # noqa: PLC0415
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        window_start = datetime.date.fromisoformat(d.pop("window_start"))




        window_end = datetime.date.fromisoformat(d.pop("window_end"))




        days = []
        _days = d.pop("days")
        for days_item_data in (_days):
            days_item = LavaflowDayCounts.from_dict(days_item_data)



            days.append(days_item)


        totals = LavaflowStatsTotals.from_dict(d.pop("totals"))




        lavaflow_stats = cls(
            project_id=project_id,
            window_start=window_start,
            window_end=window_end,
            days=days,
            totals=totals,
        )


        lavaflow_stats.additional_properties = d
        return lavaflow_stats

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
