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
            total_users (int): Current auth-user count, matching the auth-user list total.
            active_users_30d (int): Users with a successful session creation or refresh in the trailing 30 days since
                activity collection was deployed.
     """

    total_users: int
    active_users_30d: int





    def to_dict(self) -> dict[str, Any]:
        total_users = self.total_users

        active_users_30d = self.active_users_30d


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "total_users": total_users,
            "active_users_30d": active_users_30d,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_users = d.pop("total_users")

        active_users_30d = d.pop("active_users_30d")

        auth_insights_summary = cls(
            total_users=total_users,
            active_users_30d=active_users_30d,
        )

        return auth_insights_summary

