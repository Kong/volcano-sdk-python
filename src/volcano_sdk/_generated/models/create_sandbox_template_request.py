from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_sandbox_template_request_memory_mb import check_create_sandbox_template_request_memory_mb
from ..models.create_sandbox_template_request_memory_mb import CreateSandboxTemplateRequestMemoryMb
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="CreateSandboxTemplateRequest")



@_attrs_define
class CreateSandboxTemplateRequest:
    """ 
        Attributes:
            name (str):
            preset (str): Preset ID from the available Sandbox preset catalog.
            memory_mb (CreateSandboxTemplateRequestMemoryMb | Unset):  Default: 1024.
     """

    name: str
    preset: str
    memory_mb: CreateSandboxTemplateRequestMemoryMb | Unset = 1024





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        preset = self.preset

        memory_mb: int | Unset = UNSET
        if not isinstance(self.memory_mb, Unset):
            memory_mb = self.memory_mb



        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
            "preset": preset,
        })
        if memory_mb is not UNSET:
            field_dict["memory_mb"] = memory_mb

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        preset = d.pop("preset")

        _memory_mb = d.pop("memory_mb", UNSET)
        memory_mb: CreateSandboxTemplateRequestMemoryMb | Unset
        if isinstance(_memory_mb,  Unset):
            memory_mb = UNSET
        else:
            memory_mb = check_create_sandbox_template_request_memory_mb(_memory_mb)




        create_sandbox_template_request = cls(
            name=name,
            preset=preset,
            memory_mb=memory_mb,
        )

        return create_sandbox_template_request

