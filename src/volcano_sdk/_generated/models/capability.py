from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.capability_status import CapabilityStatus
from ..models.capability_status import check_capability_status
from typing import cast






T = TypeVar("T", bound="Capability")



@_attrs_define
class Capability:
    """ A product capability and whether it accepts new work in this environment.

        Attributes:
            id (str): Stable capability ID, such as `sandboxes`, `sandboxes.sessions`, or `sandboxes.custom_templates`. New
                IDs may appear at any time. Example: sandboxes.sessions.
            status (CapabilityStatus): `available` means the capability accepts new work; a temporary outage still answers
                `503`. `unavailable` means requests that start new work answer `404` or `400` with code `feature_unavailable`.
                Treat any other value as `unavailable`.
     """

    id: str
    status: CapabilityStatus





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status: str = self.status


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        status = check_capability_status(d.pop("status"))




        capability = cls(
            id=id,
            status=status,
        )

        return capability

