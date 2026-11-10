from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.sandbox_limits_applied import check_sandbox_limits_applied
from ..models.sandbox_limits_applied import SandboxLimitsApplied
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="SandboxSessionAppliedLimits")



@_attrs_define
class SandboxSessionAppliedLimits:
    """ The caps the session enforces, as the session reports them. Present only
    when the session was created with `limits`. The session stays
    `starting` until `applied` is known.

        Attributes:
            applied (SandboxLimitsApplied): `enforced` when every requested cap is enforced, `not_enforced` when the
                session could not enforce them, and `unknown` until the session reports.
                Terminate a session that reports anything but `enforced` if you rely on
                the caps.
            vcpus (int | Unset): Enforced vCPU cap. Never higher than requested; lower when the session has fewer vCPUs.
            disk_mib (int | Unset): Enforced disk cap in MiB. Never higher than requested; lower when the session's disk has
                less free space.
     """

    applied: SandboxLimitsApplied
    vcpus: int | Unset = UNSET
    disk_mib: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        applied: str = self.applied

        vcpus = self.vcpus

        disk_mib = self.disk_mib


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "applied": applied,
        })
        if vcpus is not UNSET:
            field_dict["vcpus"] = vcpus
        if disk_mib is not UNSET:
            field_dict["disk_mib"] = disk_mib

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        applied = check_sandbox_limits_applied(d.pop("applied"))




        vcpus = d.pop("vcpus", UNSET)

        disk_mib = d.pop("disk_mib", UNSET)

        sandbox_session_applied_limits = cls(
            applied=applied,
            vcpus=vcpus,
            disk_mib=disk_mib,
        )

        return sandbox_session_applied_limits
