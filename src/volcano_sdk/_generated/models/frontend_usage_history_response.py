from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.frontend_usage_daily_entry import FrontendUsageDailyEntry





T = TypeVar("T", bound="FrontendUsageHistoryResponse")



@_attrs_define
class FrontendUsageHistoryResponse:
    """ Zero-filled daily series of request + error counts for a single frontend, oldest first.

        Attributes:
            frontend_id (UUID):
            days (int): Number of daily entries returned (always equal to the `days` query param after clamping).
            daily (list[FrontendUsageDailyEntry]):
            total_requests (int):
            total_errors (int):
            total_page_views (int):
     """

    frontend_id: UUID
    days: int
    daily: list[FrontendUsageDailyEntry]
    total_requests: int
    total_errors: int
    total_page_views: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.frontend_usage_daily_entry import FrontendUsageDailyEntry
        frontend_id = str(self.frontend_id)

        days = self.days

        daily = []
        for daily_item_data in self.daily:
            daily_item = daily_item_data.to_dict()
            daily.append(daily_item)



        total_requests = self.total_requests

        total_errors = self.total_errors

        total_page_views = self.total_page_views


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "frontend_id": frontend_id,
            "days": days,
            "daily": daily,
            "total_requests": total_requests,
            "total_errors": total_errors,
            "total_page_views": total_page_views,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.frontend_usage_daily_entry import FrontendUsageDailyEntry
        d = dict(src_dict)
        frontend_id = UUID(d.pop("frontend_id"))




        days = d.pop("days")

        daily = []
        _daily = d.pop("daily")
        for daily_item_data in (_daily):
            daily_item = FrontendUsageDailyEntry.from_dict(daily_item_data)



            daily.append(daily_item)


        total_requests = d.pop("total_requests")

        total_errors = d.pop("total_errors")

        total_page_views = d.pop("total_page_views")

        frontend_usage_history_response = cls(
            frontend_id=frontend_id,
            days=days,
            daily=daily,
            total_requests=total_requests,
            total_errors=total_errors,
            total_page_views=total_page_views,
        )


        frontend_usage_history_response.additional_properties = d
        return frontend_usage_history_response

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
