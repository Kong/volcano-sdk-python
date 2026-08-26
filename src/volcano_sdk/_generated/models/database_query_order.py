from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="DatabaseQueryOrder")



@_attrs_define
class DatabaseQueryOrder:
    """ One ORDER BY clause.

        Attributes:
            column (str):  Example: created_at.
            ascending (bool | Unset):  Default: True.
            nulls_first (bool | Unset):  Default: False.
     """

    column: str
    ascending: bool | Unset = True
    nulls_first: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        column = self.column

        ascending = self.ascending

        nulls_first = self.nulls_first


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "column": column,
        })
        if ascending is not UNSET:
            field_dict["ascending"] = ascending
        if nulls_first is not UNSET:
            field_dict["nulls_first"] = nulls_first

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        column = d.pop("column")

        ascending = d.pop("ascending", UNSET)

        nulls_first = d.pop("nulls_first", UNSET)

        database_query_order = cls(
            column=column,
            ascending=ascending,
            nulls_first=nulls_first,
        )


        database_query_order.additional_properties = d
        return database_query_order

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
