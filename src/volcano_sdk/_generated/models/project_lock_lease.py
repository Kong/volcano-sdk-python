from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="ProjectLockLease")



@_attrs_define
class ProjectLockLease:
    """ 
        Attributes:
            expires_at (datetime.datetime): Advisory lease expiry timestamp in UTC.
            fencing_token (int): Monotonically increasing token for this acquisition. It rises whenever the
                lock changes hands and stays the same across renewals of one lease. Pass it
                to the resource you are protecting and reject any write carrying a token
                lower than the highest already seen; that is what stops a displaced holder
                from writing after its lease lapsed.
     """

    expires_at: datetime.datetime
    fencing_token: int





    def to_dict(self) -> dict[str, Any]:
        expires_at = self.expires_at.isoformat()

        fencing_token = self.fencing_token


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "expires_at": expires_at,
            "fencing_token": fencing_token,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))




        fencing_token = d.pop("fencing_token")

        project_lock_lease = cls(
            expires_at=expires_at,
            fencing_token=fencing_token,
        )

        return project_lock_lease

