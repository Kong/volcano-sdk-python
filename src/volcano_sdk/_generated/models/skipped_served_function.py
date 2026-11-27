from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="SkippedServedFunction")



@_attrs_define
class SkippedServedFunction:
    """ 
        Attributes:
            id (UUID): Function ID.
            name (str): Function name.
            code (str): Why the function was left out. Clients must accept codes not listed here.
                `function_served_by_candidate` - a promoted preview serves the function and keeps the
                variables it was built with.
            message (str): What brings the function in line.
     """

    id: UUID
    name: str
    code: str
    message: str





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        code = self.code

        message = self.message


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "name": name,
            "code": code,
            "message": message,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        name = d.pop("name")

        code = d.pop("code")

        message = d.pop("message")

        skipped_served_function = cls(
            id=id,
            name=name,
            code=code,
            message=message,
        )

        return skipped_served_function

