from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.anon_key import AnonKey





T = TypeVar("T", bound="ListAnonKeysResponse200")



@_attrs_define
class ListAnonKeysResponse200:
    """ 
        Attributes:
            data (list[AnonKey] | Unset):
            total (int | Unset): Total number of items matching the query (so the UI can render numbered pages).
            has_more (bool | Unset): Whether a next page exists.
            next_cursor (str | Unset): Opaque cursor for the next page (cursor pagination only)
            prev_cursor (str | Unset): Opaque cursor for the previous page (cursor pagination only). Send as
                `ending_before`.
     """

    data: list[AnonKey] | Unset = UNSET
    total: int | Unset = UNSET
    has_more: bool | Unset = UNSET
    next_cursor: str | Unset = UNSET
    prev_cursor: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.anon_key import AnonKey
        data: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)



        total = self.total

        has_more = self.has_more

        next_cursor = self.next_cursor

        prev_cursor = self.prev_cursor


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if data is not UNSET:
            field_dict["data"] = data
        if total is not UNSET:
            field_dict["total"] = total
        if has_more is not UNSET:
            field_dict["has_more"] = has_more
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor
        if prev_cursor is not UNSET:
            field_dict["prev_cursor"] = prev_cursor

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.anon_key import AnonKey
        d = dict(src_dict)
        _data = d.pop("data", UNSET)
        data: list[AnonKey] | Unset = UNSET
        if _data is not UNSET:
            data = []
            for data_item_data in _data:
                data_item = AnonKey.from_dict(data_item_data)



                data.append(data_item)


        total = d.pop("total", UNSET)

        has_more = d.pop("has_more", UNSET)

        next_cursor = d.pop("next_cursor", UNSET)

        prev_cursor = d.pop("prev_cursor", UNSET)

        list_anon_keys_response_200 = cls(
            data=data,
            total=total,
            has_more=has_more,
            next_cursor=next_cursor,
            prev_cursor=prev_cursor,
        )


        list_anon_keys_response_200.additional_properties = d
        return list_anon_keys_response_200

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
