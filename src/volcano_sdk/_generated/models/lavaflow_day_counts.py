from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="LavaflowDayCounts")



@_attrs_define
class LavaflowDayCounts:
    """ 
        Attributes:
            date (datetime.date):
            issues_opened (int): Issues LavaFlow took on that UTC day.
            pull_requests_opened (int): Pull requests with a fix LavaFlow opened that UTC day.
     """

    date: datetime.date
    issues_opened: int
    pull_requests_opened: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        date = self.date.isoformat()

        issues_opened = self.issues_opened

        pull_requests_opened = self.pull_requests_opened


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "date": date,
            "issues_opened": issues_opened,
            "pull_requests_opened": pull_requests_opened,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = datetime.date.fromisoformat(d.pop("date"))




        issues_opened = d.pop("issues_opened")

        pull_requests_opened = d.pop("pull_requests_opened")

        lavaflow_day_counts = cls(
            date=date,
            issues_opened=issues_opened,
            pull_requests_opened=pull_requests_opened,
        )


        lavaflow_day_counts.additional_properties = d
        return lavaflow_day_counts

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
