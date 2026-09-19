from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ProjectConfigVariable")



@_attrs_define
class ProjectConfigVariable:
    """ 
        Attributes:
            name (str):
            value (str):
            shared (bool | Unset): Include this name in the project's shared function variables. Omission preserves existing
                membership; new variables default to true for legacy clients. Send false explicitly to create a non-shared
                variable.
     """

    name: str
    value: str
    shared: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value = self.value

        shared = self.shared


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
            "value": value,
        })
        if shared is not UNSET:
            field_dict["shared"] = shared

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        value = d.pop("value")

        shared = d.pop("shared", UNSET)

        project_config_variable = cls(
            name=name,
            value=value,
            shared=shared,
        )

        return project_config_variable

