from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateSandboxSessionActivityBodyActivity")



@_attrs_define
class UpdateSandboxSessionActivityBodyActivity:
    """
        Attributes:
            sequence (int):
            idle (bool):
            idle_timeout_seconds (int | Unset): Seconds from acceptance of an idle report to expiry. Required when idle is
                true and omitted when active.
     """

    sequence: int
    idle: bool
    idle_timeout_seconds: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        sequence = self.sequence

        idle = self.idle

        idle_timeout_seconds = self.idle_timeout_seconds


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "sequence": sequence,
            "idle": idle,
        })
        if idle_timeout_seconds is not UNSET:
            field_dict["idle_timeout_seconds"] = idle_timeout_seconds

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sequence = d.pop("sequence")

        idle = d.pop("idle")

        idle_timeout_seconds = d.pop("idle_timeout_seconds", UNSET)

        update_sandbox_session_activity_body_activity = cls(
            sequence=sequence,
            idle=idle,
            idle_timeout_seconds=idle_timeout_seconds,
        )

        return update_sandbox_session_activity_body_activity
