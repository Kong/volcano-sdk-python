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
            code (File | Unset): Source tar.gz archive, limited to 32 MiB compressed and expanded. Required for customer
                templates. Omit for the managed Builder template.
            memory_mb (DeploySandboxBodyMemoryMb | Unset): Memory in MiB. Defaults to 1024 when omitted.
            ports (str | Unset): JSON array of application ports that must become ready before activation, for example
                [8080].
            containers (bool | Unset): Run a rootless container engine (Docker Engine with Compose) in every session of this
                template. Commands reach it through `DOCKER_HOST` and keep the same privileges as in any other session. Disabled
                by default. Only the operator-authorized Builder caller in local mode can deploy its reserved platform template,
                with no code archive or ports. Disabled or unsupported opt-ins answer `400 feature_unavailable`. An unauthorized
                caller receives 403; incompatible form fields receive 400.
     """

    name: str
    code: File | Unset = UNSET
    memory_mb: DeploySandboxBodyMemoryMb | Unset = UNSET
    ports: str | Unset = UNSET
    containers: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        code: FileTypes | Unset = UNSET
        if not isinstance(self.code, Unset):
            code = self.code.to_tuple()


        memory_mb: int | Unset = UNSET
        if not isinstance(self.memory_mb, Unset):
            memory_mb = self.memory_mb


        ports = self.ports

        containers = self.containers


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
        })
        if code is not UNSET:
            field_dict["code"] = code
        if memory_mb is not UNSET:
            field_dict["memory_mb"] = memory_mb
        if ports is not UNSET:
            field_dict["ports"] = ports
        if containers is not UNSET:
            field_dict["containers"] = containers

        return field_dict


    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("name", (None, str(self.name).encode(), "text/plain")))



        if not isinstance(self.code, Unset):
            files.append(("code", self.code.to_tuple()))



        if not isinstance(self.memory_mb, Unset):
            files.append(("memory_mb", (None, str(self.memory_mb).encode(), "text/plain")))



        if not isinstance(self.ports, Unset):
            files.append(("ports", (None, str(self.ports).encode(), "text/plain")))



        if not isinstance(self.containers, Unset):
            files.append(("containers", (None, str(self.containers).encode(), "text/plain")))




        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))



        return files


    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        _code = d.pop("code", UNSET)
        code: File | Unset
        if isinstance(_code,  Unset):
            code = UNSET
        else:
            code = File(
             payload = BytesIO(_code)
        )




        _memory_mb = d.pop("memory_mb", UNSET)
        memory_mb: DeploySandboxBodyMemoryMb | Unset
        if isinstance(_memory_mb,  Unset):
            memory_mb = UNSET
        else:
            memory_mb = check_deploy_sandbox_body_memory_mb(_memory_mb)




        ports = d.pop("ports", UNSET)

        containers = d.pop("containers", UNSET)

        deploy_sandbox_body = cls(
            name=name,
            code=code,
            memory_mb=memory_mb,
            ports=ports,
            containers=containers,
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
