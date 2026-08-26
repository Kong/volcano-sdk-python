from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ProjectConfigAuthPassword")



@_attrs_define
class ProjectConfigAuthPassword:
    """ 
        Attributes:
            min_length (int | Unset):
            require_uppercase (bool | Unset):
            require_lowercase (bool | Unset):
            require_numbers (bool | Unset):
            require_special_chars (bool | Unset):
     """

    min_length: int | Unset = UNSET
    require_uppercase: bool | Unset = UNSET
    require_lowercase: bool | Unset = UNSET
    require_numbers: bool | Unset = UNSET
    require_special_chars: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        min_length = self.min_length

        require_uppercase = self.require_uppercase

        require_lowercase = self.require_lowercase

        require_numbers = self.require_numbers

        require_special_chars = self.require_special_chars


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if min_length is not UNSET:
            field_dict["min_length"] = min_length
        if require_uppercase is not UNSET:
            field_dict["require_uppercase"] = require_uppercase
        if require_lowercase is not UNSET:
            field_dict["require_lowercase"] = require_lowercase
        if require_numbers is not UNSET:
            field_dict["require_numbers"] = require_numbers
        if require_special_chars is not UNSET:
            field_dict["require_special_chars"] = require_special_chars

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        min_length = d.pop("min_length", UNSET)

        require_uppercase = d.pop("require_uppercase", UNSET)

        require_lowercase = d.pop("require_lowercase", UNSET)

        require_numbers = d.pop("require_numbers", UNSET)

        require_special_chars = d.pop("require_special_chars", UNSET)

        project_config_auth_password = cls(
            min_length=min_length,
            require_uppercase=require_uppercase,
            require_lowercase=require_lowercase,
            require_numbers=require_numbers,
            require_special_chars=require_special_chars,
        )

        return project_config_auth_password

