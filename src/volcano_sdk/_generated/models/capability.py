from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.capability_status import CapabilityStatus
from ..models.capability_status import check_capability_status
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="Capability")



@_attrs_define
class Capability:
    """ A product capability and whether it accepts new work in this environment.

        Attributes:
            id (str): Stable capability ID, such as `sandboxes`, `sandboxes.sessions`, `sandboxes.custom_templates`, or
                `issues`. New IDs may appear at any time. Example: sandboxes.sessions.
            status (CapabilityStatus): `available` means the capability accepts new work; a temporary outage still answers
                `503`. `unavailable` means requests that start new work answer `404` or `400` with code `feature_unavailable`,
                or with the capability's `code` when it has one; while the owner's plan can't be read, they answer `403` without
                a code. `read_only` means the capability takes no new work for the project, but what the project already has
                stays readable; only a project's list reports it. Treat any other value as `unavailable`.
            code (str | Unset): Why an `unavailable` capability refuses new work, named like the error code its requests
                answer with, such as `plan_required`. Absent on any other status, and when requests answer
                `feature_unavailable`. Treat an unknown code as absent. Example: plan_required.
     """

    id: str
    status: CapabilityStatus
    code: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status: str = self.status

        code = self.code


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "status": status,
        })
        if code is not UNSET:
            field_dict["code"] = code

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        status = check_capability_status(d.pop("status"))




        code = d.pop("code", UNSET)

        capability = cls(
            id=id,
            status=status,
            code=code,
        )

        return capability

