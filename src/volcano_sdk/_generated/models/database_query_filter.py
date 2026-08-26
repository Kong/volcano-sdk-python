from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.database_query_filter_operator import check_database_query_filter_operator
from ..models.database_query_filter_operator import DatabaseQueryFilterOperator
from typing import cast






T = TypeVar("T", bound="DatabaseQueryFilter")



@_attrs_define
class DatabaseQueryFilter:
    """ One WHERE condition. Conditions are combined with AND.

        Attributes:
            column (str):  Example: status.
            operator (DatabaseQueryFilterOperator): Filter operators:
                - eq: equals (=)
                - neq: not equals (<>)
                - gt: greater than (>)
                - gte: greater than or equal (>=)
                - lt: less than (<)
                - lte: less than or equal (<=)
                - like: pattern match (LIKE)
                - ilike: case-insensitive pattern match (ILIKE)
                - is: IS NULL / IS NOT NULL
                - in: IN array
                 Example: eq.
            value (bool | float | list[bool | float | str] | None | str):  Example: published.
     """

    column: str
    operator: DatabaseQueryFilterOperator
    value: bool | float | list[bool | float | str] | None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        column = self.column

        operator: str = self.operator

        value: bool | float | list[bool | float | str] | None | str
        if isinstance(self.value, list):
            value = []
            for value_type_3_item_data in self.value:
                value_type_3_item: bool | float | str
                value_type_3_item = value_type_3_item_data
                value.append(value_type_3_item)


        else:
            value = self.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "column": column,
            "operator": operator,
            "value": value,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        column = d.pop("column")

        operator = check_database_query_filter_operator(d.pop("operator"))




        def _parse_value(data: object) -> bool | float | list[bool | float | str] | None | str:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_3 = []
                _value_type_3 = data
                for value_type_3_item_data in (_value_type_3):
                    def _parse_value_type_3_item(data: object) -> bool | float | str:
                        return cast(bool | float | str, data)

                    value_type_3_item = _parse_value_type_3_item(value_type_3_item_data)

                    value_type_3.append(value_type_3_item)

                return value_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(bool | float | list[bool | float | str] | None | str, data)

        value = _parse_value(d.pop("value"))


        database_query_filter = cls(
            column=column,
            operator=operator,
            value=value,
        )


        database_query_filter.additional_properties = d
        return database_query_filter

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
