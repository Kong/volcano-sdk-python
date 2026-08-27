from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.storage_bucket import StorageBucket





T = TypeVar("T", bound="PaginatedStorageBuckets")



@_attrs_define
class PaginatedStorageBuckets:
    """ Cursor-paginated storage buckets (returned only when cursor pagination is requested).

        Attributes:
            data (list[StorageBucket]):
            limit (int): Number of items per page
            has_more (bool): Whether a next page exists
            total (int | Unset): Total number of items matching the query
            next_cursor (str | Unset): Opaque cursor for the next page (present if has_more is true)
            prev_cursor (str | Unset): Opaque cursor for the previous page (present when a previous page exists). Send as
                `ending_before`.
     """

    data: list[StorageBucket]
    limit: int
    has_more: bool
    total: int | Unset = UNSET
    next_cursor: str | Unset = UNSET
    prev_cursor: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.storage_bucket import StorageBucket
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)



        limit = self.limit

        has_more = self.has_more

        total = self.total

        next_cursor = self.next_cursor

        prev_cursor = self.prev_cursor


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "data": data,
            "limit": limit,
            "has_more": has_more,
        })
        if total is not UNSET:
            field_dict["total"] = total
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor
        if prev_cursor is not UNSET:
            field_dict["prev_cursor"] = prev_cursor

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.storage_bucket import StorageBucket
        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in (_data):
            data_item = StorageBucket.from_dict(data_item_data)



            data.append(data_item)


        limit = d.pop("limit")

        has_more = d.pop("has_more")

        total = d.pop("total", UNSET)

        next_cursor = d.pop("next_cursor", UNSET)

        prev_cursor = d.pop("prev_cursor", UNSET)

        paginated_storage_buckets = cls(
            data=data,
            limit=limit,
            has_more=has_more,
            total=total,
            next_cursor=next_cursor,
            prev_cursor=prev_cursor,
        )


        paginated_storage_buckets.additional_properties = d
        return paginated_storage_buckets

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
