from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SandboxSessionExecutions")



@_attrs_define
class SandboxSessionExecutions:
    """ How the session's command executions are kept. Fixed when the session is created.

        Attributes:
            keep_output (bool): When false, every command in the session keeps no output. stdout and stderr are returned
                once in the command's response, and Volcano's control plane never stores them in the execution journal,
                database, logs or traces. This does not cover the Sandbox's memory or a suspended session's snapshot. A retry
                with the same Idempotency-Key returns the exit code with empty streams. A command in such a session that sets
                `keep_output` to true is refused with 400 and code `sandbox_session_keeps_no_output`. False is refused with 400
                and code `feature_unavailable` while the `sandboxes.output_not_kept` capability is unavailable.
     """

    keep_output: bool





    def to_dict(self) -> dict[str, Any]:
        keep_output = self.keep_output


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "keep_output": keep_output,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        keep_output = d.pop("keep_output")

        sandbox_session_executions = cls(
            keep_output=keep_output,
        )

        return sandbox_session_executions
