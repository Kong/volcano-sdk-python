from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.log_activity_bucket_counts import LogActivityBucketCounts





T = TypeVar("T", bound="LogActivityBucket")



@_attrs_define
class LogActivityBucket:
    """ Log-event counts for one activity time bucket.

        Attributes:
            start_time (datetime.datetime): Bucket start time.
            end_time (datetime.datetime): Bucket end time.
            counts (LogActivityBucketCounts): Counts grouped by activity dimension.
            total (int): Total events in this bucket.
     """

    start_time: datetime.datetime
    end_time: datetime.datetime
    counts: LogActivityBucketCounts
    total: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.log_activity_bucket_counts import LogActivityBucketCounts
        start_time = self.start_time.isoformat()

        end_time = self.end_time.isoformat()

        counts = self.counts.to_dict()

        total = self.total


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "start_time": start_time,
            "end_time": end_time,
            "counts": counts,
            "total": total,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_activity_bucket_counts import LogActivityBucketCounts
        d = dict(src_dict)
        start_time = datetime.datetime.fromisoformat(d.pop("start_time"))




        end_time = datetime.datetime.fromisoformat(d.pop("end_time"))




        counts = LogActivityBucketCounts.from_dict(d.pop("counts"))




        total = d.pop("total")

        log_activity_bucket = cls(
            start_time=start_time,
            end_time=end_time,
            counts=counts,
            total=total,
        )


        log_activity_bucket.additional_properties = d
        return log_activity_bucket

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
