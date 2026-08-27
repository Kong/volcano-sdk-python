from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.log_search_event import LogSearchEvent





T = TypeVar("T", bound="LogSearchResponse")



@_attrs_define
class LogSearchResponse:
    """ Paginated project runtime log search response.

        Attributes:
            data (list[LogSearchEvent]): Array of log events sorted by timestamp, newest first.
            limit (int): Number of items requested per page.
            has_more (bool): Whether there are more log events available.
            next_cursor (str | Unset): Opaque cursor for the next page. Send this value as `cursor` on the next request.
     """

    data: list[LogSearchEvent]
    limit: int
    has_more: bool
    next_cursor: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.log_search_event import LogSearchEvent
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)



        limit = self.limit

        has_more = self.has_more

        next_cursor = self.next_cursor


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "data": data,
            "limit": limit,
            "has_more": has_more,
        })
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_search_event import LogSearchEvent
        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in (_data):
            data_item = LogSearchEvent.from_dict(data_item_data)



            data.append(data_item)


        limit = d.pop("limit")

        has_more = d.pop("has_more")

        next_cursor = d.pop("next_cursor", UNSET)

        log_search_response = cls(
            data=data,
            limit=limit,
            has_more=has_more,
            next_cursor=next_cursor,
        )


        log_search_response.additional_properties = d
        return log_search_response

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
