from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SandboxCapacity")



@_attrs_define
class SandboxCapacity:
    """ 
        Attributes:
            region (str):
            allocated_memory_mb (int):
     """

    region: str
    allocated_memory_mb: int





    def to_dict(self) -> dict[str, Any]:
        region = self.region

        allocated_memory_mb = self.allocated_memory_mb


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "region": region,
            "allocated_memory_mb": allocated_memory_mb,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        region = d.pop("region")

        allocated_memory_mb = d.pop("allocated_memory_mb")

        sandbox_capacity = cls(
            region=region,
            allocated_memory_mb=allocated_memory_mb,
        )

        return sandbox_capacity

