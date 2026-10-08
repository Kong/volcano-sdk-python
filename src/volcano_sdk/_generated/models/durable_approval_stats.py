from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.durable_approval_counts import DurableApprovalCounts
  from ..models.durable_approval_daily_counts import DurableApprovalDailyCounts
  from ..models.durable_approval_function_counts import DurableApprovalFunctionCounts





T = TypeVar("T", bound="DurableApprovalStats")



@_attrs_define
class DurableApprovalStats:
    """ 
        Attributes:
            from_ (datetime.datetime):
            to (datetime.datetime):
            counts (DurableApprovalCounts): Approvals by status. `requested` is every approval, whatever its status.
            approval_rate (float | None): `approved / (approved + denied)`, from 0 to 1. Null when nothing in
                the window was decided.
            median_seconds_to_decision (float | None): Median time from request to decision. Null when nothing was decided.
            p90_seconds_to_decision (float | None): 90th percentile time from request to decision. Null when nothing was
                decided.
            functions (list[DurableApprovalFunctionCounts]): The ten workflows that requested the most approvals, most
                first.
                The rest are summed in `other_functions`.
            other_functions (DurableApprovalCounts): Approvals by status. `requested` is every approval, whatever its
                status.
            daily (list[DurableApprovalDailyCounts]): One entry per UTC day in the window that has approvals, oldest
                first. Days with none are omitted.
     """

    from_: datetime.datetime
    to: datetime.datetime
    counts: DurableApprovalCounts
    approval_rate: float | None
    median_seconds_to_decision: float | None
    p90_seconds_to_decision: float | None
    functions: list[DurableApprovalFunctionCounts]
    other_functions: DurableApprovalCounts
    daily: list[DurableApprovalDailyCounts]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.durable_approval_counts import DurableApprovalCounts # noqa: PLC0415
        from ..models.durable_approval_daily_counts import DurableApprovalDailyCounts # noqa: PLC0415
        from ..models.durable_approval_function_counts import DurableApprovalFunctionCounts # noqa: PLC0415
        from_ = self.from_.isoformat()

        to = self.to.isoformat()

        counts = self.counts.to_dict()

        approval_rate: float | None
        approval_rate = self.approval_rate

        median_seconds_to_decision: float | None
        median_seconds_to_decision = self.median_seconds_to_decision

        p90_seconds_to_decision: float | None
        p90_seconds_to_decision = self.p90_seconds_to_decision

        functions = []
        for functions_item_data in self.functions:
            functions_item = functions_item_data.to_dict()
            functions.append(functions_item)



        other_functions = self.other_functions.to_dict()

        daily = []
        for daily_item_data in self.daily:
            daily_item = daily_item_data.to_dict()
            daily.append(daily_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "from": from_,
            "to": to,
            "counts": counts,
            "approval_rate": approval_rate,
            "median_seconds_to_decision": median_seconds_to_decision,
            "p90_seconds_to_decision": p90_seconds_to_decision,
            "functions": functions,
            "other_functions": other_functions,
            "daily": daily,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.durable_approval_counts import DurableApprovalCounts # noqa: PLC0415
        from ..models.durable_approval_daily_counts import DurableApprovalDailyCounts # noqa: PLC0415
        from ..models.durable_approval_function_counts import DurableApprovalFunctionCounts # noqa: PLC0415
        d = dict(src_dict)
        from_ = datetime.datetime.fromisoformat(d.pop("from"))




        to = datetime.datetime.fromisoformat(d.pop("to"))




        counts = DurableApprovalCounts.from_dict(d.pop("counts"))




        def _parse_approval_rate(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        approval_rate = _parse_approval_rate(d.pop("approval_rate"))


        def _parse_median_seconds_to_decision(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        median_seconds_to_decision = _parse_median_seconds_to_decision(d.pop("median_seconds_to_decision"))


        def _parse_p90_seconds_to_decision(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        p90_seconds_to_decision = _parse_p90_seconds_to_decision(d.pop("p90_seconds_to_decision"))


        functions = []
        _functions = d.pop("functions")
        for functions_item_data in (_functions):
            functions_item = DurableApprovalFunctionCounts.from_dict(functions_item_data)



            functions.append(functions_item)


        other_functions = DurableApprovalCounts.from_dict(d.pop("other_functions"))




        daily = []
        _daily = d.pop("daily")
        for daily_item_data in (_daily):
            daily_item = DurableApprovalDailyCounts.from_dict(daily_item_data)



            daily.append(daily_item)


        durable_approval_stats = cls(
            from_=from_,
            to=to,
            counts=counts,
            approval_rate=approval_rate,
            median_seconds_to_decision=median_seconds_to_decision,
            p90_seconds_to_decision=p90_seconds_to_decision,
            functions=functions,
            other_functions=other_functions,
            daily=daily,
        )


        durable_approval_stats.additional_properties = d
        return durable_approval_stats

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
