from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ProjectConfigAuthRateLimits")



@_attrs_define
class ProjectConfigAuthRateLimits:
    """ Rate limits per hour.

        Attributes:
            signup (int | Unset):
            signin (int | Unset):
            token_refresh (int | Unset):
            password_reset (int | Unset):
     """

    signup: int | Unset = UNSET
    signin: int | Unset = UNSET
    token_refresh: int | Unset = UNSET
    password_reset: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        signup = self.signup

        signin = self.signin

        token_refresh = self.token_refresh

        password_reset = self.password_reset


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if signup is not UNSET:
            field_dict["signup"] = signup
        if signin is not UNSET:
            field_dict["signin"] = signin
        if token_refresh is not UNSET:
            field_dict["token_refresh"] = token_refresh
        if password_reset is not UNSET:
            field_dict["password_reset"] = password_reset

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        signup = d.pop("signup", UNSET)

        signin = d.pop("signin", UNSET)

        token_refresh = d.pop("token_refresh", UNSET)

        password_reset = d.pop("password_reset", UNSET)

        project_config_auth_rate_limits = cls(
            signup=signup,
            signin=signin,
            token_refresh=token_refresh,
            password_reset=password_reset,
        )

        return project_config_auth_rate_limits

