from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.lavaflow_run_counts import LavaflowRunCounts
  from ..models.lavaflow_run_summary import LavaflowRunSummary





T = TypeVar("T", bound="PaginatedLavaflowRuns")



@_attrs_define
class PaginatedLavaflowRuns:
    """ 
        Attributes:
            data (list[LavaflowRunSummary]):
            limit (int): Number of items per page
            has_more (bool): Whether a next page exists
            next_cursor (str | Unset): Opaque cursor for the next page, present if has_more is true. It works only for the
                same project_id, caller and order.
            counts (LavaflowRunCounts | Unset): Runs that match the request. `total` applies every filter. Each breakdown
                applies every filter but its own, so it shows what picking another value would return.
     """

    data: list[LavaflowRunSummary]
    limit: int
    has_more: bool
    next_cursor: str | Unset = UNSET
    counts: LavaflowRunCounts | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_run_counts import LavaflowRunCounts # noqa: PLC0415
        from ..models.lavaflow_run_summary import LavaflowRunSummary # noqa: PLC0415
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)



        limit = self.limit

        has_more = self.has_more

        next_cursor = self.next_cursor

        counts: dict[str, Any] | Unset = UNSET
        if not isinstance(self.counts, Unset):
            counts = self.counts.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "data": data,
            "limit": limit,
            "has_more": has_more,
        })
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor
        if counts is not UNSET:
            field_dict["counts"] = counts

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_run_counts import LavaflowRunCounts # noqa: PLC0415
        from ..models.lavaflow_run_summary import LavaflowRunSummary # noqa: PLC0415
        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in (_data):
            data_item = LavaflowRunSummary.from_dict(data_item_data)



            data.append(data_item)


        limit = d.pop("limit")

        has_more = d.pop("has_more")

        next_cursor = d.pop("next_cursor", UNSET)

        _counts = d.pop("counts", UNSET)
        counts: LavaflowRunCounts | Unset
        if isinstance(_counts,  Unset):
            counts = UNSET
        else:
            counts = LavaflowRunCounts.from_dict(_counts)




        paginated_lavaflow_runs = cls(
            data=data,
            limit=limit,
            has_more=has_more,
            next_cursor=next_cursor,
            counts=counts,
        )


        paginated_lavaflow_runs.additional_properties = d
        return paginated_lavaflow_runs

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
