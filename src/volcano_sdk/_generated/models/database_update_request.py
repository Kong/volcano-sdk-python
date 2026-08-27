from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.database_query_filter import DatabaseQueryFilter
  from ..models.database_update_request_values import DatabaseUpdateRequestValues





T = TypeVar("T", bound="DatabaseUpdateRequest")



@_attrs_define
class DatabaseUpdateRequest:
    """ 
        Attributes:
            table (str): Table name Example: posts.
            values (DatabaseUpdateRequestValues): Column values to update Example: {'title': 'Updated Title', 'status':
                'published'}.
            filters (list[DatabaseQueryFilter]): WHERE conditions for which rows to update. At least one filter is
                required; a filterless update is rejected to avoid rewriting every
                row.
                 Example: [{'column': 'id', 'operator': 'eq', 'value': 'post-uuid'}].
     """

    table: str
    values: DatabaseUpdateRequestValues
    filters: list[DatabaseQueryFilter]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.database_query_filter import DatabaseQueryFilter
        from ..models.database_update_request_values import DatabaseUpdateRequestValues
        table = self.table

        values = self.values.to_dict()

        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()
            filters.append(filters_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "table": table,
            "values": values,
            "filters": filters,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.database_query_filter import DatabaseQueryFilter
        from ..models.database_update_request_values import DatabaseUpdateRequestValues
        d = dict(src_dict)
        table = d.pop("table")

        values = DatabaseUpdateRequestValues.from_dict(d.pop("values"))




        filters = []
        _filters = d.pop("filters")
        for filters_item_data in (_filters):
            filters_item = DatabaseQueryFilter.from_dict(filters_item_data)



            filters.append(filters_item)


        database_update_request = cls(
            table=table,
            values=values,
            filters=filters,
        )


        database_update_request.additional_properties = d
        return database_update_request

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
