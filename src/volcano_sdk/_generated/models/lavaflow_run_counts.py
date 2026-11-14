from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.lavaflow_category_counts import LavaflowCategoryCounts
  from ..models.lavaflow_involved_resource_count import LavaflowInvolvedResourceCount
  from ..models.lavaflow_pull_request_state_counts import LavaflowPullRequestStateCounts
  from ..models.lavaflow_run_status_counts import LavaflowRunStatusCounts





T = TypeVar("T", bound="LavaflowRunCounts")



@_attrs_define
class LavaflowRunCounts:
    """ Runs that match the request. `total` applies every filter. Each breakdown applies every filter but its own, so it
    shows what picking another value would return.

        Attributes:
            total (int):
            status (LavaflowRunStatusCounts): Matching runs in each status, zeros included.
            category (LavaflowCategoryCounts): Matching runs in each category, zeros included. `uncategorized` counts runs
                whose `category` is null.
            pull_request_state (LavaflowPullRequestStateCounts): Matching runs by the state of their pull request, zeros
                included. `none` counts runs without one.
            involved_resources (list[LavaflowInvolvedResourceCount]): Resources involved in at least one matching run, most
                runs first, then by name; at most 50. A run counts once per resource it involves. A run whose report came from
                what it saved rather than its source, such as one from before involved resources were recorded, may leave out
                frontends and the functions involved through shared code or the build root's dependency files, so these counts
                can undercount them.
     """

    total: int
    status: LavaflowRunStatusCounts
    category: LavaflowCategoryCounts
    pull_request_state: LavaflowPullRequestStateCounts
    involved_resources: list[LavaflowInvolvedResourceCount]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_category_counts import LavaflowCategoryCounts # noqa: PLC0415
        from ..models.lavaflow_involved_resource_count import LavaflowInvolvedResourceCount # noqa: PLC0415
        from ..models.lavaflow_pull_request_state_counts import LavaflowPullRequestStateCounts # noqa: PLC0415
        from ..models.lavaflow_run_status_counts import LavaflowRunStatusCounts # noqa: PLC0415
        total = self.total

        status = self.status.to_dict()

        category = self.category.to_dict()

        pull_request_state = self.pull_request_state.to_dict()

        involved_resources = []
        for involved_resources_item_data in self.involved_resources:
            involved_resources_item = involved_resources_item_data.to_dict()
            involved_resources.append(involved_resources_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "total": total,
            "status": status,
            "category": category,
            "pull_request_state": pull_request_state,
            "involved_resources": involved_resources,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_category_counts import LavaflowCategoryCounts # noqa: PLC0415
        from ..models.lavaflow_involved_resource_count import LavaflowInvolvedResourceCount # noqa: PLC0415
        from ..models.lavaflow_pull_request_state_counts import LavaflowPullRequestStateCounts # noqa: PLC0415
        from ..models.lavaflow_run_status_counts import LavaflowRunStatusCounts # noqa: PLC0415
        d = dict(src_dict)
        total = d.pop("total")

        status = LavaflowRunStatusCounts.from_dict(d.pop("status"))




        category = LavaflowCategoryCounts.from_dict(d.pop("category"))




        pull_request_state = LavaflowPullRequestStateCounts.from_dict(d.pop("pull_request_state"))




        involved_resources = []
        _involved_resources = d.pop("involved_resources")
        for involved_resources_item_data in (_involved_resources):
            involved_resources_item = LavaflowInvolvedResourceCount.from_dict(involved_resources_item_data)



            involved_resources.append(involved_resources_item)


        lavaflow_run_counts = cls(
            total=total,
            status=status,
            category=category,
            pull_request_state=pull_request_state,
            involved_resources=involved_resources,
        )


        lavaflow_run_counts.additional_properties = d
        return lavaflow_run_counts

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
