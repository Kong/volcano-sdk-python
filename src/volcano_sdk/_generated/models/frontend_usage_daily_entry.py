from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="FrontendUsageDailyEntry")



@_attrs_define
class FrontendUsageDailyEntry:
    """ One day of request and error counts for a single frontend.

        Attributes:
            day (datetime.date): UTC date (YYYY-MM-DD) the counts cover.
            requests (int): Total requests served on this day.
            errors (int): 5xx responses served on this day.
            page_views (int): Navigable-document responses served on this day (text/html or Sec-Fetch-Dest=document) —
                strict subset of `requests`.
     """

    day: datetime.date
    requests: int
    errors: int
    page_views: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        day = self.day.isoformat()

        requests = self.requests

        errors = self.errors

        page_views = self.page_views


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "day": day,
            "requests": requests,
            "errors": errors,
            "page_views": page_views,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        day = datetime.date.fromisoformat(d.pop("day"))




        requests = d.pop("requests")

        errors = d.pop("errors")

        page_views = d.pop("page_views")

        frontend_usage_daily_entry = cls(
            day=day,
            requests=requests,
            errors=errors,
            page_views=page_views,
        )


        frontend_usage_daily_entry.additional_properties = d
        return frontend_usage_daily_entry

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
