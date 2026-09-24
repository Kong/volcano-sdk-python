from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SandboxFileResult")



@_attrs_define
class SandboxFileResult:
    """ 
        Attributes:
            data (str):
     """

    data: str





    def to_dict(self) -> dict[str, Any]:
        data = self.data


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "data": data,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        data = d.pop("data")

        sandbox_file_result = cls(
            data=data,
        )

        return sandbox_file_result

