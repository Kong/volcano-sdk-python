from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProjectConfigAuthRedirects")



@_attrs_define
class ProjectConfigAuthRedirects:
    """ 
        Attributes:
            allowed (list[str] | Unset): Redirect allowlist. Every entry must be a valid http/https URL.
            post_auth (str | Unset): Must be included in `allowed` when set.
            post_logout (str | Unset): Must be included in `allowed` when set.
            device_verification (str | Unset): Optional custom device-authorization verification page URL.
     """

    allowed: list[str] | Unset = UNSET
    post_auth: str | Unset = UNSET
    post_logout: str | Unset = UNSET
    device_verification: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        allowed: list[str] | Unset = UNSET
        if not isinstance(self.allowed, Unset):
            allowed = self.allowed



        post_auth = self.post_auth

        post_logout = self.post_logout

        device_verification = self.device_verification


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if allowed is not UNSET:
            field_dict["allowed"] = allowed
        if post_auth is not UNSET:
            field_dict["post_auth"] = post_auth
        if post_logout is not UNSET:
            field_dict["post_logout"] = post_logout
        if device_verification is not UNSET:
            field_dict["device_verification"] = device_verification

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        allowed = cast(list[str], d.pop("allowed", UNSET))


        post_auth = d.pop("post_auth", UNSET)

        post_logout = d.pop("post_logout", UNSET)

        device_verification = d.pop("device_verification", UNSET)

        project_config_auth_redirects = cls(
            allowed=allowed,
            post_auth=post_auth,
            post_logout=post_logout,
            device_verification=device_verification,
        )

        return project_config_auth_redirects

