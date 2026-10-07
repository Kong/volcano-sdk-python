from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field
import json
from .. import types

from ..types import UNSET, Unset

from ..models.deploy_sandbox_body_memory_mb import check_deploy_sandbox_body_memory_mb
from ..models.deploy_sandbox_body_memory_mb import DeploySandboxBodyMemoryMb
from ..types import File, FileTypes
from ..types import UNSET, Unset
from io import BytesIO
from typing import cast






T = TypeVar("T", bound="DeploySandboxBody")



@_attrs_define
class DeploySandboxBody:
    """
        Attributes:
            name (str):
            code (File): Source tar.gz archive, limited to 32 MiB compressed and expanded.
            memory_mb (DeploySandboxBodyMemoryMb | Unset):  Default: 1024.
            ports (str | Unset): JSON array of application ports that must become ready before activation, for example
                [8080].
     """

    name: str
    code: File
    memory_mb: DeploySandboxBodyMemoryMb | Unset = 1024
    ports: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        code = self.code.to_tuple()


        memory_mb: int | Unset = UNSET
        if not isinstance(self.memory_mb, Unset):
            memory_mb = self.memory_mb


        ports = self.ports


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "code": code,
        })
        if memory_mb is not UNSET:
            field_dict["memory_mb"] = memory_mb
        if ports is not UNSET:
            field_dict["ports"] = ports

        return field_dict


    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("name", (None, str(self.name).encode(), "text/plain")))



        files.append(("code", self.code.to_tuple()))



        if not isinstance(self.memory_mb, Unset):
            files.append(("memory_mb", (None, str(self.memory_mb).encode(), "text/plain")))



        if not isinstance(self.ports, Unset):
            files.append(("ports", (None, str(self.ports).encode(), "text/plain")))




        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))



        return files


    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        code = File(
             payload = BytesIO(d.pop("code"))
        )




        _memory_mb = d.pop("memory_mb", UNSET)
        memory_mb: DeploySandboxBodyMemoryMb | Unset
        if isinstance(_memory_mb,  Unset):
            memory_mb = UNSET
        else:
            memory_mb = check_deploy_sandbox_body_memory_mb(_memory_mb)




        ports = d.pop("ports", UNSET)

        deploy_sandbox_body = cls(
            name=name,
            code=code,
            memory_mb=memory_mb,
            ports=ports,
        )


        deploy_sandbox_body.additional_properties = d
        return deploy_sandbox_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
