from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.database_query_result_data_item import DatabaseQueryResultDataItem





T = TypeVar("T", bound="DatabaseQueryResult")



@_attrs_define
class DatabaseQueryResult:
    """ Rows returned by a data API request. RLS-filtered unless the request was
    made with a service key.

        Attributes:
            data (list[DatabaseQueryResultDataItem] | Unset): Result rows
            count (int | Unset): Number of rows returned
     """

    data: list[DatabaseQueryResultDataItem] | Unset = UNSET
    count: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.database_query_result_data_item import DatabaseQueryResultDataItem
        data: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)



        count = self.count


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if data is not UNSET:
            field_dict["data"] = data
        if count is not UNSET:
            field_dict["count"] = count

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.database_query_result_data_item import DatabaseQueryResultDataItem
        d = dict(src_dict)
        _data = d.pop("data", UNSET)
        data: list[DatabaseQueryResultDataItem] | Unset = UNSET
        if _data is not UNSET:
            data = []
            for data_item_data in _data:
                data_item = DatabaseQueryResultDataItem.from_dict(data_item_data)



                data.append(data_item)


        count = d.pop("count", UNSET)

        database_query_result = cls(
            data=data,
            count=count,
        )


        database_query_result.additional_properties = d
        return database_query_result

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
