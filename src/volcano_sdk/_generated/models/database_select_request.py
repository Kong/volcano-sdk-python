from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.database_query_filter import DatabaseQueryFilter
  from ..models.database_query_order import DatabaseQueryOrder





T = TypeVar("T", bound="DatabaseSelectRequest")



@_attrs_define
class DatabaseSelectRequest:
    """ 
        Attributes:
            table (str): Table name to query Example: posts.
            select (list[str] | Unset): Columns to select (omit for *) Example: ['id', 'title', 'content', 'created_at'].
            filters (list[DatabaseQueryFilter] | Unset): WHERE conditions (combined with AND) Example: [{'column': 'status',
                'operator': 'eq', 'value': 'published'}, {'column': 'views', 'operator': 'gt', 'value': 100}].
            order (list[DatabaseQueryOrder] | Unset): ORDER BY clauses Example: [{'column': 'created_at', 'ascending':
                False}].
            limit (int | Unset): Maximum rows to return Example: 10.
            offset (int | Unset): Number of rows to skip (for pagination)
     """

    table: str
    select: list[str] | Unset = UNSET
    filters: list[DatabaseQueryFilter] | Unset = UNSET
    order: list[DatabaseQueryOrder] | Unset = UNSET
    limit: int | Unset = UNSET
    offset: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.database_query_filter import DatabaseQueryFilter
        from ..models.database_query_order import DatabaseQueryOrder
        table = self.table

        select: list[str] | Unset = UNSET
        if not isinstance(self.select, Unset):
            select = self.select



        filters: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item = filters_item_data.to_dict()
                filters.append(filters_item)



        order: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.order, Unset):
            order = []
            for order_item_data in self.order:
                order_item = order_item_data.to_dict()
                order.append(order_item)



        limit = self.limit

        offset = self.offset


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "table": table,
        })
        if select is not UNSET:
            field_dict["select"] = select
        if filters is not UNSET:
            field_dict["filters"] = filters
        if order is not UNSET:
            field_dict["order"] = order
        if limit is not UNSET:
            field_dict["limit"] = limit
        if offset is not UNSET:
            field_dict["offset"] = offset

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.database_query_filter import DatabaseQueryFilter
        from ..models.database_query_order import DatabaseQueryOrder
        d = dict(src_dict)
        table = d.pop("table")

        select = cast(list[str], d.pop("select", UNSET))


        _filters = d.pop("filters", UNSET)
        filters: list[DatabaseQueryFilter] | Unset = UNSET
        if _filters is not UNSET:
            filters = []
            for filters_item_data in _filters:
                filters_item = DatabaseQueryFilter.from_dict(filters_item_data)



                filters.append(filters_item)


        _order = d.pop("order", UNSET)
        order: list[DatabaseQueryOrder] | Unset = UNSET
        if _order is not UNSET:
            order = []
            for order_item_data in _order:
                order_item = DatabaseQueryOrder.from_dict(order_item_data)



                order.append(order_item)


        limit = d.pop("limit", UNSET)

        offset = d.pop("offset", UNSET)

        database_select_request = cls(
            table=table,
            select=select,
            filters=filters,
            order=order,
            limit=limit,
            offset=offset,
        )


        database_select_request.additional_properties = d
        return database_select_request

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
