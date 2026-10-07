from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_config_sandbox_memory_mb import check_project_config_sandbox_memory_mb
from ..models.project_config_sandbox_memory_mb import ProjectConfigSandboxMemoryMb
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProjectConfigSandbox")



@_attrs_define
class ProjectConfigSandbox:
    """
        Attributes:
            name (str): Name of an existing sandbox template or matching Git source directory.
            memory_mb (ProjectConfigSandboxMemoryMb | Unset): Immutable deployed memory profile; config apply asserts it and
                Git deploy builds it.
            ports (list[int] | Unset): Service readiness ports; config apply asserts them and Git deploy builds them.
            idle_timeout_seconds (int | Unset): Default idle timeout for new sessions when the caller omits it.
            ttl_seconds (int | Unset): Default absolute lifetime for new sessions when the caller omits it.
     """

    name: str
    memory_mb: ProjectConfigSandboxMemoryMb | Unset = UNSET
    ports: list[int] | Unset = UNSET
    idle_timeout_seconds: int | Unset = UNSET
    ttl_seconds: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        memory_mb: int | Unset = UNSET
        if not isinstance(self.memory_mb, Unset):
            memory_mb = self.memory_mb


        ports: list[int] | Unset = UNSET
        if not isinstance(self.ports, Unset):
            ports = self.ports



        idle_timeout_seconds = self.idle_timeout_seconds

        ttl_seconds = self.ttl_seconds


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
        })
        if memory_mb is not UNSET:
            field_dict["memory_mb"] = memory_mb
        if ports is not UNSET:
            field_dict["ports"] = ports
        if idle_timeout_seconds is not UNSET:
            field_dict["idle_timeout_seconds"] = idle_timeout_seconds
        if ttl_seconds is not UNSET:
            field_dict["ttl_seconds"] = ttl_seconds

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        _memory_mb = d.pop("memory_mb", UNSET)
        memory_mb: ProjectConfigSandboxMemoryMb | Unset
        if isinstance(_memory_mb,  Unset):
            memory_mb = UNSET
        else:
            memory_mb = check_project_config_sandbox_memory_mb(_memory_mb)




        ports = cast(list[int], d.pop("ports", UNSET))


        idle_timeout_seconds = d.pop("idle_timeout_seconds", UNSET)

        ttl_seconds = d.pop("ttl_seconds", UNSET)

        project_config_sandbox = cls(
            name=name,
            memory_mb=memory_mb,
            ports=ports,
            idle_timeout_seconds=idle_timeout_seconds,
            ttl_seconds=ttl_seconds,
        )

        return project_config_sandbox
