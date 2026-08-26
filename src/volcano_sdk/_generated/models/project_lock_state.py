from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ProjectLockState")



@_attrs_define
class ProjectLockState:
    """ 
        Attributes:
            held (bool): Whether the lock is unavailable right now. False means an acquire would
                succeed. It remains true during the brief grace window after expiry.
            expires_at (datetime.datetime | Unset): Advisory lease expiry timestamp in UTC. Present only when held.
            fencing_token (int | Unset): Current holder's fencing token. Present only when held.
     """

    held: bool
    expires_at: datetime.datetime | Unset = UNSET
    fencing_token: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        held = self.held

        expires_at: str | Unset = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        fencing_token = self.fencing_token


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "held": held,
        })
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if fencing_token is not UNSET:
            field_dict["fencing_token"] = fencing_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        held = d.pop("held")

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: datetime.datetime | Unset
        if isinstance(_expires_at,  Unset):
            expires_at = UNSET
        else:
            expires_at = datetime.datetime.fromisoformat(_expires_at)




        fencing_token = d.pop("fencing_token", UNSET)

        project_lock_state = cls(
            held=held,
            expires_at=expires_at,
            fencing_token=fencing_token,
        )

        return project_lock_state

