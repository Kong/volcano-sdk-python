from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.share_daily_count_kind import check_share_daily_count_kind
from ..models.share_daily_count_kind import ShareDailyCountKind
from typing import cast
import datetime






T = TypeVar("T", bound="ShareDailyCount")



@_attrs_define
class ShareDailyCount:
    """ 
        Attributes:
            day (datetime.date): UTC day.
            kind (ShareDailyCountKind):
            events (int):
     """

    day: datetime.date
    kind: ShareDailyCountKind
    events: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        day = self.day.isoformat()

        kind: str = self.kind

        events = self.events


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "day": day,
            "kind": kind,
            "events": events,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        day = datetime.date.fromisoformat(d.pop("day"))




        kind = check_share_daily_count_kind(d.pop("kind"))




        events = d.pop("events")

        share_daily_count = cls(
            day=day,
            kind=kind,
            events=events,
        )


        share_daily_count.additional_properties = d
        return share_daily_count

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
