from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ExportProjectSourceRequest")



@_attrs_define
class ExportProjectSourceRequest:
    """ 
        Attributes:
            production_branch (str): The currently configured production branch the user confirmed for export.
     """

    production_branch: str





    def to_dict(self) -> dict[str, Any]:
        production_branch = self.production_branch


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "production_branch": production_branch,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        production_branch = d.pop("production_branch")

        export_project_source_request = cls(
            production_branch=production_branch,
        )

        return export_project_source_request

