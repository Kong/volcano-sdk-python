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
            stdout (str): The first 1 MiB (1,048,576 bytes) the command wrote to stdout. Empty in a replay of a command that
                kept no output.
            stderr (str): The first 1 MiB (1,048,576 bytes) the command wrote to stderr. Empty in a replay of a command that
                kept no output.
            exit_code (int):
            stdout_truncated (bool): True when the command wrote more than 1 MiB to stdout. False in a replay of a command
                that kept no output.
            stderr_truncated (bool): True when the command wrote more than 1 MiB to stderr. False in a replay of a command
                that kept no output.
            timed_out (bool):
            output_kept (bool): False when the command kept no output. Its streams appear only in the response to the
                request that ran it, and Volcano's control plane never stores them in the execution journal, database, logs or
                traces. This does not cover the Sandbox's memory or a suspended session's snapshot. A retry with the same
                Idempotency-Key returns them empty.
     """

    stdout: str
    stderr: str
    exit_code: int
    stdout_truncated: bool
    stderr_truncated: bool
    timed_out: bool
    output_kept: bool





    def to_dict(self) -> dict[str, Any]:
        stdout = self.stdout

        stderr = self.stderr

        exit_code = self.exit_code

        stdout_truncated = self.stdout_truncated

        stderr_truncated = self.stderr_truncated

        timed_out = self.timed_out

        output_kept = self.output_kept


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": exit_code,
            "stdout_truncated": stdout_truncated,
            "stderr_truncated": stderr_truncated,
            "timed_out": timed_out,
            "output_kept": output_kept,
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

        output_kept = d.pop("output_kept")

        sandbox_command_result = cls(
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            stdout_truncated=stdout_truncated,
            stderr_truncated=stderr_truncated,
            timed_out=timed_out,
            output_kept=output_kept,
        )

        return sandbox_command_result
