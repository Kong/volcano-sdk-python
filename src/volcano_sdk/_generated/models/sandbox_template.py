from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.sandbox_template_status import check_sandbox_template_status
from ..models.sandbox_template_status import SandboxTemplateStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="SandboxTemplate")



@_attrs_define
class SandboxTemplate:
    """ 
        Attributes:
            id (UUID):
            project_id (UUID):
            name (str):
            status (SandboxTemplateStatus):
            created_at (datetime.datetime):
            preset (str | Unset):
            memory_mb (int | Unset):
     """

    id: UUID
    project_id: UUID
    name: str
    status: SandboxTemplateStatus
    created_at: datetime.datetime
    preset: str | Unset = UNSET
    memory_mb: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id = str(self.project_id)

        name = self.name

        status: str = self.status

        created_at = self.created_at.isoformat()

        preset = self.preset

        memory_mb = self.memory_mb


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "project_id": project_id,
            "name": name,
            "status": status,
            "created_at": created_at,
        })
        if preset is not UNSET:
            field_dict["preset"] = preset
        if memory_mb is not UNSET:
            field_dict["memory_mb"] = memory_mb

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        name = d.pop("name")

        status = check_sandbox_template_status(d.pop("status"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        preset = d.pop("preset", UNSET)

        memory_mb = d.pop("memory_mb", UNSET)

        sandbox_template = cls(
            id=id,
            project_id=project_id,
            name=name,
            status=status,
            created_at=created_at,
            preset=preset,
            memory_mb=memory_mb,
        )

        return sandbox_template

