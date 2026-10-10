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
            timeout_seconds (int | Unset): Command execution time from process start. Cloud defaults to 60 seconds and
                accepts 1–28800; local defaults to 0 (unlimited) and accepts nonnegative values. VM expiry always takes
                precedence. Cloud synchronous requests must return within the public connection idle limit (1000 seconds); use a
                session with a background process and short polling requests for longer work.
            environment (SandboxCommandRequestEnvironment | Unset):
     """

    command: str
    timeout_seconds: int | Unset = UNSET
    environment: SandboxCommandRequestEnvironment | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.sandbox_command_request_environment import SandboxCommandRequestEnvironment # noqa: PLC0415
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
        from ..models.sandbox_command_request_environment import SandboxCommandRequestEnvironment # noqa: PLC0415
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
