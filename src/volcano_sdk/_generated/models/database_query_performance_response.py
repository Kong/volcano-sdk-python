from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.database_query_performance_item import DatabaseQueryPerformanceItem





T = TypeVar("T", bound="DatabaseQueryPerformanceResponse")



@_attrs_define
class DatabaseQueryPerformanceResponse:
    """ 
        Attributes:
            data (list[DatabaseQueryPerformanceItem]):
     """

    data: list[DatabaseQueryPerformanceItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.database_query_performance_item import DatabaseQueryPerformanceItem
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "data": data,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.database_query_performance_item import DatabaseQueryPerformanceItem
        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in (_data):
            data_item = DatabaseQueryPerformanceItem.from_dict(data_item_data)



            data.append(data_item)


        database_query_performance_response = cls(
            data=data,
        )


        database_query_performance_response.additional_properties = d
        return database_query_performance_response

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
