from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.log_activity_bucket_counts_levels import LogActivityBucketCountsLevels
  from ..models.log_activity_bucket_counts_regions import LogActivityBucketCountsRegions
  from ..models.log_activity_bucket_counts_resource_ids import LogActivityBucketCountsResourceIds





T = TypeVar("T", bound="LogActivityBucketCounts")



@_attrs_define
class LogActivityBucketCounts:
    """ Counts grouped by activity dimension.

        Attributes:
            levels (LogActivityBucketCountsLevels): Counts by normalized log level.
            regions (LogActivityBucketCountsRegions): Counts by event region.
            resource_ids (LogActivityBucketCountsResourceIds): Counts by resource ID.
     """

    levels: LogActivityBucketCountsLevels
    regions: LogActivityBucketCountsRegions
    resource_ids: LogActivityBucketCountsResourceIds
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.log_activity_bucket_counts_levels import LogActivityBucketCountsLevels
        from ..models.log_activity_bucket_counts_regions import LogActivityBucketCountsRegions
        from ..models.log_activity_bucket_counts_resource_ids import LogActivityBucketCountsResourceIds
        levels = self.levels.to_dict()

        regions = self.regions.to_dict()

        resource_ids = self.resource_ids.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "levels": levels,
            "regions": regions,
            "resource_ids": resource_ids,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_activity_bucket_counts_levels import LogActivityBucketCountsLevels
        from ..models.log_activity_bucket_counts_regions import LogActivityBucketCountsRegions
        from ..models.log_activity_bucket_counts_resource_ids import LogActivityBucketCountsResourceIds
        d = dict(src_dict)
        levels = LogActivityBucketCountsLevels.from_dict(d.pop("levels"))




        regions = LogActivityBucketCountsRegions.from_dict(d.pop("regions"))




        resource_ids = LogActivityBucketCountsResourceIds.from_dict(d.pop("resource_ids"))




        log_activity_bucket_counts = cls(
            levels=levels,
            regions=regions,
            resource_ids=resource_ids,
        )


        log_activity_bucket_counts.additional_properties = d
        return log_activity_bucket_counts

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
