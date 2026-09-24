from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="SandboxPagination")



@_attrs_define
class SandboxPagination:
    """ 
        Attributes:
            limit (int):
            has_more (bool):
            next_cursor (str | Unset):
     """

    limit: int
    has_more: bool
    next_cursor: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        has_more = self.has_more

        next_cursor = self.next_cursor


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "limit": limit,
            "has_more": has_more,
        })
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        limit = d.pop("limit")

        has_more = d.pop("has_more")

        next_cursor = d.pop("next_cursor", UNSET)

        sandbox_pagination = cls(
            limit=limit,
            has_more=has_more,
            next_cursor=next_cursor,
        )

        return sandbox_pagination

