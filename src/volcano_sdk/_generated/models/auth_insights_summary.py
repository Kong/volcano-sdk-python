from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AuthInsightsSummary")



@_attrs_define
class AuthInsightsSummary:
    """ 
        Attributes:
            total_users (int): Current auth-user count, excluding accounts with deleted status.
            deleted_users (int): Recorded deletions, excluding internal test identities. Includes soft and hard deletion,
                counted once per account.
            active_users_1d (int): Distinct users active in the trailing 24 hours, including activity before account
                deletion.
            active_users_30d (int): Distinct users with a successful session creation or refresh in the trailing 30 days,
                including activity before account deletion.
     """

    total_users: int
    deleted_users: int
    active_users_1d: int
    active_users_30d: int





    def to_dict(self) -> dict[str, Any]:
        total_users = self.total_users

        deleted_users = self.deleted_users

        active_users_1d = self.active_users_1d

        active_users_30d = self.active_users_30d


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "total_users": total_users,
            "deleted_users": deleted_users,
            "active_users_1d": active_users_1d,
            "active_users_30d": active_users_30d,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_users = d.pop("total_users")

        deleted_users = d.pop("deleted_users")

        active_users_1d = d.pop("active_users_1d")

        active_users_30d = d.pop("active_users_30d")

        auth_insights_summary = cls(
            total_users=total_users,
            deleted_users=deleted_users,
            active_users_1d=active_users_1d,
            active_users_30d=active_users_30d,
        )

        return auth_insights_summary

