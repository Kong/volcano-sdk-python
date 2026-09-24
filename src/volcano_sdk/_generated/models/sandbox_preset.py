from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.sandbox_preset_memory_mb import check_sandbox_preset_memory_mb
from ..models.sandbox_preset_memory_mb import SandboxPresetMemoryMb
from typing import cast






T = TypeVar("T", bound="SandboxPreset")



@_attrs_define
class SandboxPreset:
    """ 
        Attributes:
            id (str):
            runtime (str):
            version (str):
            memory_mb (SandboxPresetMemoryMb):
            regions (list[str]):
     """

    id: str
    runtime: str
    version: str
    memory_mb: SandboxPresetMemoryMb
    regions: list[str]





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        runtime = self.runtime

        version = self.version

        memory_mb: int = self.memory_mb

        regions = self.regions




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "runtime": runtime,
            "version": version,
            "memory_mb": memory_mb,
            "regions": regions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        runtime = d.pop("runtime")

        version = d.pop("version")

        memory_mb = check_sandbox_preset_memory_mb(d.pop("memory_mb"))




        regions = cast(list[str], d.pop("regions"))


        sandbox_preset = cls(
            id=id,
            runtime=runtime,
            version=version,
            memory_mb=memory_mb,
            regions=regions,
        )

        return sandbox_preset

