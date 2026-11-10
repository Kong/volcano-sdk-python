from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="SandboxSessionLimits")



@_attrs_define
class SandboxSessionLimits:
    """ Caps the session's code runs under, enforced inside the session. Each
    cap is an upper bound; the session's own size still bounds both.

        Attributes:
            vcpus (int | Unset): CPU time the session's commands and template service may use
                together, in vCPUs. A 1024 MiB session has 2 vCPUs and a 2048 MiB
                session has 4; asking for more answers 400 with code
                `sandbox_limits_exceed_session`.
            disk_mib (int | Unset): Space the session can write beyond its image's contents, in MiB.
                It covers every path commands and the template service can write,
                including `/workspace` and `/tmp`. A write past it fails with
                `ENOSPC`. `/dev/shm` is memory, capped separately at 64 MiB.
     """

    vcpus: int | Unset = UNSET
    disk_mib: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        vcpus = self.vcpus

        disk_mib = self.disk_mib


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if vcpus is not UNSET:
            field_dict["vcpus"] = vcpus
        if disk_mib is not UNSET:
            field_dict["disk_mib"] = disk_mib

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        vcpus = d.pop("vcpus", UNSET)

        disk_mib = d.pop("disk_mib", UNSET)

        sandbox_session_limits = cls(
            vcpus=vcpus,
            disk_mib=disk_mib,
        )

        return sandbox_session_limits
