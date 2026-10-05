from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ReplaceSharedVariablesBody")



@_attrs_define
class ReplaceSharedVariablesBody:
    """ 
        Attributes:
            shared_variables (list[str]):
            expected_shared_variables (list[str] | Unset): When present, replace only if the current complete shared list
                matches this list.
            expected_shared_variables_digest (str | Unset): SHA-256 of the sorted unique current shared names joined by a
                newline. Use instead of expected_shared_variables for a compact conditional replacement.
     """

    shared_variables: list[str]
    expected_shared_variables: list[str] | Unset = UNSET
    expected_shared_variables_digest: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        shared_variables = self.shared_variables



        expected_shared_variables: list[str] | Unset = UNSET
        if not isinstance(self.expected_shared_variables, Unset):
            expected_shared_variables = self.expected_shared_variables



        expected_shared_variables_digest = self.expected_shared_variables_digest


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "shared_variables": shared_variables,
        })
        if expected_shared_variables is not UNSET:
            field_dict["expected_shared_variables"] = expected_shared_variables
        if expected_shared_variables_digest is not UNSET:
            field_dict["expected_shared_variables_digest"] = expected_shared_variables_digest

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        shared_variables = cast(list[str], d.pop("shared_variables"))


        expected_shared_variables = cast(list[str], d.pop("expected_shared_variables", UNSET))


        expected_shared_variables_digest = d.pop("expected_shared_variables_digest", UNSET)

        replace_shared_variables_body = cls(
            shared_variables=shared_variables,
            expected_shared_variables=expected_shared_variables,
            expected_shared_variables_digest=expected_shared_variables_digest,
        )

        return replace_shared_variables_body

