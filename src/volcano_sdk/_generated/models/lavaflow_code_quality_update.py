from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowCodeQualityUpdate")



@_attrs_define
class LavaflowCodeQualityUpdate:
    """ Turns Code Quality on or off. Only the project's owner, signed in, can turn it on; any credential that can save the
    settings can turn it off.

        Attributes:
            enabled (bool):
     """

    enabled: bool





    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "enabled": enabled,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        lavaflow_code_quality_update = cls(
            enabled=enabled,
        )

        return lavaflow_code_quality_update

