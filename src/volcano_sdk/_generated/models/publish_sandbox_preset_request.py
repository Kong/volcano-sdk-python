from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.publish_sandbox_preset_request_memory_mb import check_publish_sandbox_preset_request_memory_mb
from ..models.publish_sandbox_preset_request_memory_mb import PublishSandboxPresetRequestMemoryMb
from ..models.publish_sandbox_preset_request_preset import check_publish_sandbox_preset_request_preset
from ..models.publish_sandbox_preset_request_preset import PublishSandboxPresetRequestPreset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="PublishSandboxPresetRequest")



@_attrs_define
class PublishSandboxPresetRequest:
    """ 
        Attributes:
            id (UUID):
            preset (PublishSandboxPresetRequestPreset):
            memory_mb (PublishSandboxPresetRequestMemoryMb):
            deployment_id (UUID):
     """

    id: UUID
    preset: PublishSandboxPresetRequestPreset
    memory_mb: PublishSandboxPresetRequestMemoryMb
    deployment_id: UUID





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        preset: str = self.preset

        memory_mb: int = self.memory_mb

        deployment_id = str(self.deployment_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "preset": preset,
            "memory_mb": memory_mb,
            "deployment_id": deployment_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        preset = check_publish_sandbox_preset_request_preset(d.pop("preset"))




        memory_mb = check_publish_sandbox_preset_request_memory_mb(d.pop("memory_mb"))




        deployment_id = UUID(d.pop("deployment_id"))




        publish_sandbox_preset_request = cls(
            id=id,
            preset=preset,
            memory_mb=memory_mb,
            deployment_id=deployment_id,
        )

        return publish_sandbox_preset_request

