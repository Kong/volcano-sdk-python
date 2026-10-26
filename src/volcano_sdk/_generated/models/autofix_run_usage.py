from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AutofixRunUsage")



@_attrs_define
class AutofixRunUsage:
    """ Model tokens the run used across every attempt.

        Attributes:
            input_tokens (int):
            output_tokens (int):
            cache_read_input_tokens (int):
            cache_creation_input_tokens (int):
     """

    input_tokens: int
    output_tokens: int
    cache_read_input_tokens: int
    cache_creation_input_tokens: int





    def to_dict(self) -> dict[str, Any]:
        input_tokens = self.input_tokens

        output_tokens = self.output_tokens

        cache_read_input_tokens = self.cache_read_input_tokens

        cache_creation_input_tokens = self.cache_creation_input_tokens


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cache_read_input_tokens": cache_read_input_tokens,
            "cache_creation_input_tokens": cache_creation_input_tokens,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        input_tokens = d.pop("input_tokens")

        output_tokens = d.pop("output_tokens")

        cache_read_input_tokens = d.pop("cache_read_input_tokens")

        cache_creation_input_tokens = d.pop("cache_creation_input_tokens")

        autofix_run_usage = cls(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_read_input_tokens=cache_read_input_tokens,
            cache_creation_input_tokens=cache_creation_input_tokens,
        )

        return autofix_run_usage

