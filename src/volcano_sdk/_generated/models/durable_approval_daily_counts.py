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





T = TypeVar("T", bound="DurableApprovalDailyCounts")



@_attrs_define
class DurableApprovalDailyCounts:
    """ 
        Attributes:
            date (datetime.date):
            counts (DurableApprovalCounts): Approvals by status. `requested` is every approval, whatever its status.
     """

    date: datetime.date
    counts: DurableApprovalCounts
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.durable_approval_counts import DurableApprovalCounts # noqa: PLC0415
        date = self.date.isoformat()

        counts = self.counts.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "date": date,
            "counts": counts,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.durable_approval_counts import DurableApprovalCounts # noqa: PLC0415
        d = dict(src_dict)
        date = datetime.date.fromisoformat(d.pop("date"))




        counts = DurableApprovalCounts.from_dict(d.pop("counts"))




        durable_approval_daily_counts = cls(
            date=date,
            counts=counts,
        )


        durable_approval_daily_counts.additional_properties = d
        return durable_approval_daily_counts

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
