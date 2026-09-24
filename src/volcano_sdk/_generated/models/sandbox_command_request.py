from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.sandbox_command_request_environment import SandboxCommandRequestEnvironment





T = TypeVar("T", bound="SandboxCommandRequest")



@_attrs_define
class SandboxCommandRequest:
    """ 
        Attributes:
            command (str):
            timeout_seconds (int | Unset):  Default: 60.
            environment (SandboxCommandRequestEnvironment | Unset):
     """

    command: str
    timeout_seconds: int | Unset = 60
    environment: SandboxCommandRequestEnvironment | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.sandbox_command_request_environment import SandboxCommandRequestEnvironment
        command = self.command

        timeout_seconds = self.timeout_seconds

        environment: dict[str, Any] | Unset = UNSET
        if not isinstance(self.environment, Unset):
            environment = self.environment.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "command": command,
        })
        if timeout_seconds is not UNSET:
            field_dict["timeout_seconds"] = timeout_seconds
        if environment is not UNSET:
            field_dict["environment"] = environment

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_command_request_environment import SandboxCommandRequestEnvironment
        d = dict(src_dict)
        command = d.pop("command")

        timeout_seconds = d.pop("timeout_seconds", UNSET)

        _environment = d.pop("environment", UNSET)
        environment: SandboxCommandRequestEnvironment | Unset
        if isinstance(_environment,  Unset):
            environment = UNSET
        else:
            environment = SandboxCommandRequestEnvironment.from_dict(_environment)




        sandbox_command_request = cls(
            command=command,
            timeout_seconds=timeout_seconds,
            environment=environment,
        )

        return sandbox_command_request

