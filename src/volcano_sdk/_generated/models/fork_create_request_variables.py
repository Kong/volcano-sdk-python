from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ForkCreateRequestVariables")



@_attrs_define
class ForkCreateRequestVariables:
    """ Values for the variables the preview lists, by name. Any may be left out
    and is then created empty; only listed names are accepted (`422`
    otherwise). Each value is at most 4096 bytes of UTF-8, since a function's
    environment is limited in bytes; a longer one, or one containing a NUL
    character, answers `400`. Values are never logged, and `Idempotency-Key` compares only the names given a value.

     """

    additional_properties: dict[str, str] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        fork_create_request_variables = cls(
        )


        fork_create_request_variables.additional_properties = d
        return fork_create_request_variables

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
