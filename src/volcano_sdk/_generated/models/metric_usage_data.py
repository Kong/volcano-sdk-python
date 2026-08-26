from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.usage_data_point import UsageDataPoint





T = TypeVar("T", bound="MetricUsageData")



@_attrs_define
class MetricUsageData:
    """ Usage data for one metric across totals, daily, and hourly windows.

        Attributes:
            metric (str): Metric name (for example, "Function & Frontend Invocations", "Frontend Requests",
                "CodeBuild Build Seconds", "Bandwidth Ingress (Bytes)", "Bandwidth Egress (Bytes)",
                "Bandwidth Total (Bytes)", or "Database Storage (Bytes)"). Byte-based metrics are
                reported in bytes. "Bandwidth Total (Bytes)" is derived (ingress + egress) and
                is not billed separately. "Database Storage (Bytes)" is a current observed gauge,
                not a cumulative counter. It is the sum of the latest `pg_database_size` samples
                exposed as `storage_bytes` by the project's database list.
            total (int): Total usage for the current usage month
            all_time (int): Lifetime cumulative usage across every month for this metric
            daily (list[UsageDataPoint]): Last 30 days of daily usage points
            hourly (list[UsageDataPoint]): Last 24 hours of hourly usage points
     """

    metric: str
    total: int
    all_time: int
    daily: list[UsageDataPoint]
    hourly: list[UsageDataPoint]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.usage_data_point import UsageDataPoint
        metric = self.metric

        total = self.total

        all_time = self.all_time

        daily = []
        for daily_item_data in self.daily:
            daily_item = daily_item_data.to_dict()
            daily.append(daily_item)



        hourly = []
        for hourly_item_data in self.hourly:
            hourly_item = hourly_item_data.to_dict()
            hourly.append(hourly_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "metric": metric,
            "total": total,
            "all_time": all_time,
            "daily": daily,
            "hourly": hourly,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_data_point import UsageDataPoint
        d = dict(src_dict)
        metric = d.pop("metric")

        total = d.pop("total")

        all_time = d.pop("all_time")

        daily = []
        _daily = d.pop("daily")
        for daily_item_data in (_daily):
            daily_item = UsageDataPoint.from_dict(daily_item_data)



            daily.append(daily_item)


        hourly = []
        _hourly = d.pop("hourly")
        for hourly_item_data in (_hourly):
            hourly_item = UsageDataPoint.from_dict(hourly_item_data)



            hourly.append(hourly_item)


        metric_usage_data = cls(
            metric=metric,
            total=total,
            all_time=all_time,
            daily=daily,
            hourly=hourly,
        )


        metric_usage_data.additional_properties = d
        return metric_usage_data

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
