from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AutofixEdit")



@_attrs_define
class AutofixEdit:
    """ One exact text replacement. An empty `old_text` creates the file.

        Attributes:
            path (str):
            old_text (str):
            new_text (str):
     """

    path: str
    old_text: str
    new_text: str





    def to_dict(self) -> dict[str, Any]:
        path = self.path

        old_text = self.old_text

        new_text = self.new_text


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "path": path,
            "old_text": old_text,
            "new_text": new_text,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        old_text = d.pop("old_text")

        new_text = d.pop("new_text")

        autofix_edit = cls(
            path=path,
            old_text=old_text,
            new_text=new_text,
        )

        return autofix_edit

