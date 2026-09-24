from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SandboxCommandResult")



@_attrs_define
class SandboxCommandResult:
    """ 
        Attributes:
            stdout (str):
            stderr (str):
            exit_code (int):
            stdout_truncated (bool):
            stderr_truncated (bool):
            timed_out (bool):
     """

    stdout: str
    stderr: str
    exit_code: int
    stdout_truncated: bool
    stderr_truncated: bool
    timed_out: bool





    def to_dict(self) -> dict[str, Any]:
        stdout = self.stdout

        stderr = self.stderr

        exit_code = self.exit_code

        stdout_truncated = self.stdout_truncated

        stderr_truncated = self.stderr_truncated

        timed_out = self.timed_out


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": exit_code,
            "stdout_truncated": stdout_truncated,
            "stderr_truncated": stderr_truncated,
            "timed_out": timed_out,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        stdout = d.pop("stdout")

        stderr = d.pop("stderr")

        exit_code = d.pop("exit_code")

        stdout_truncated = d.pop("stdout_truncated")

        stderr_truncated = d.pop("stderr_truncated")

        timed_out = d.pop("timed_out")

        sandbox_command_result = cls(
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            stdout_truncated=stdout_truncated,
            stderr_truncated=stderr_truncated,
            timed_out=timed_out,
        )

        return sandbox_command_result

