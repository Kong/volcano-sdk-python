from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ProjectLockLeaseRequest")



@_attrs_define
class ProjectLockLeaseRequest:
    """ 
        Attributes:
            ttl_seconds (int): Lease duration in seconds, from 5 seconds through 90 days, measured
                from when the request is served. Renew before it elapses. A renewal
                sets the new expiry outright, so a shorter TTL shortens the lease.
                Renewals cannot extend an acquisition beyond its absolute 90-day
                deadline.
     """

    ttl_seconds: int





    def to_dict(self) -> dict[str, Any]:
        ttl_seconds = self.ttl_seconds


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "ttl_seconds": ttl_seconds,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ttl_seconds = d.pop("ttl_seconds")

        project_lock_lease_request = cls(
            ttl_seconds=ttl_seconds,
        )

        return project_lock_lease_request

