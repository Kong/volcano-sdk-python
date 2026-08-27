from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ProjectConfigAuthTokens")



@_attrs_define
class ProjectConfigAuthTokens:
    """ Token lifetimes in seconds.

        Attributes:
            access_token_lifetime (int | Unset):
            refresh_token_lifetime (int | Unset):
            refresh_token_reuse_interval (int | Unset):
            platform_token_ttl (int | Unset):
     """

    access_token_lifetime: int | Unset = UNSET
    refresh_token_lifetime: int | Unset = UNSET
    refresh_token_reuse_interval: int | Unset = UNSET
    platform_token_ttl: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        access_token_lifetime = self.access_token_lifetime

        refresh_token_lifetime = self.refresh_token_lifetime

        refresh_token_reuse_interval = self.refresh_token_reuse_interval

        platform_token_ttl = self.platform_token_ttl


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if access_token_lifetime is not UNSET:
            field_dict["access_token_lifetime"] = access_token_lifetime
        if refresh_token_lifetime is not UNSET:
            field_dict["refresh_token_lifetime"] = refresh_token_lifetime
        if refresh_token_reuse_interval is not UNSET:
            field_dict["refresh_token_reuse_interval"] = refresh_token_reuse_interval
        if platform_token_ttl is not UNSET:
            field_dict["platform_token_ttl"] = platform_token_ttl

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        access_token_lifetime = d.pop("access_token_lifetime", UNSET)

        refresh_token_lifetime = d.pop("refresh_token_lifetime", UNSET)

        refresh_token_reuse_interval = d.pop("refresh_token_reuse_interval", UNSET)

        platform_token_ttl = d.pop("platform_token_ttl", UNSET)

        project_config_auth_tokens = cls(
            access_token_lifetime=access_token_lifetime,
            refresh_token_lifetime=refresh_token_lifetime,
            refresh_token_reuse_interval=refresh_token_reuse_interval,
            platform_token_ttl=platform_token_ttl,
        )

        return project_config_auth_tokens

