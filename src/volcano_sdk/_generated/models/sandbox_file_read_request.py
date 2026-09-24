from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SandboxFileReadRequest")



@_attrs_define
class SandboxFileReadRequest:
    """ 
        Attributes:
            path (str):
     """

    path: str





    def to_dict(self) -> dict[str, Any]:
        path = self.path


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "path": path,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        sandbox_file_read_request = cls(
            path=path,
        )

        return sandbox_file_read_request

