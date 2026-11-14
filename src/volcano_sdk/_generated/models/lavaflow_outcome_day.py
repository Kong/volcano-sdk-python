from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.lavaflow_outcome_counts import LavaflowOutcomeCounts
  from ..models.lavaflow_outcome_values import LavaflowOutcomeValues





T = TypeVar("T", bound="LavaflowOutcomeDay")



@_attrs_define
class LavaflowOutcomeDay:
    """ 
        Attributes:
            date (datetime.date):
            counts (LavaflowOutcomeValues): Exact counts only when collection coverage is complete. Null means unknown,
                including days with no retained observations.
            confirmed_counts (LavaflowOutcomeCounts): Retained confirmations in the requested interval. These are lower
                bounds when collection coverage is incomplete.
     """

    date: datetime.date
    counts: LavaflowOutcomeValues
    confirmed_counts: LavaflowOutcomeCounts
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_outcome_counts import LavaflowOutcomeCounts # noqa: PLC0415
        from ..models.lavaflow_outcome_values import LavaflowOutcomeValues # noqa: PLC0415
        date = self.date.isoformat()

        counts = self.counts.to_dict()

        confirmed_counts = self.confirmed_counts.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "date": date,
            "counts": counts,
            "confirmed_counts": confirmed_counts,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_outcome_counts import LavaflowOutcomeCounts # noqa: PLC0415
        from ..models.lavaflow_outcome_values import LavaflowOutcomeValues # noqa: PLC0415
        d = dict(src_dict)
        date = datetime.date.fromisoformat(d.pop("date"))




        counts = LavaflowOutcomeValues.from_dict(d.pop("counts"))




        confirmed_counts = LavaflowOutcomeCounts.from_dict(d.pop("confirmed_counts"))




        lavaflow_outcome_day = cls(
            date=date,
            counts=counts,
            confirmed_counts=confirmed_counts,
        )


        lavaflow_outcome_day.additional_properties = d
        return lavaflow_outcome_day

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
