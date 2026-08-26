from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.database_query_filter import DatabaseQueryFilter





T = TypeVar("T", bound="DatabaseDeleteRequest")



@_attrs_define
class DatabaseDeleteRequest:
    """ 
        Attributes:
            table (str): Table name Example: posts.
            filters (list[DatabaseQueryFilter]): WHERE conditions (required for safety) Example: [{'column': 'id',
                'operator': 'eq', 'value': 'post-uuid'}].
     """

    table: str
    filters: list[DatabaseQueryFilter]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.database_query_filter import DatabaseQueryFilter
        table = self.table

        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()
            filters.append(filters_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "table": table,
            "filters": filters,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.database_query_filter import DatabaseQueryFilter
        d = dict(src_dict)
        table = d.pop("table")

        filters = []
        _filters = d.pop("filters")
        for filters_item_data in (_filters):
            filters_item = DatabaseQueryFilter.from_dict(filters_item_data)



            filters.append(filters_item)


        database_delete_request = cls(
            table=table,
            filters=filters,
        )


        database_delete_request.additional_properties = d
        return database_delete_request

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
