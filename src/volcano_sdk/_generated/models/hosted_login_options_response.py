from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="HostedLoginOptionsResponse")



@_attrs_define
class HostedLoginOptionsResponse:
    """ 
        Attributes:
            require_email_confirmation (bool | Unset):
            email_password_enabled (bool | Unset):
            enable_signup (bool | Unset):
            post_auth_redirect_url (str | Unset):
            oauth_providers (list[str] | Unset):
     """

    require_email_confirmation: bool | Unset = UNSET
    email_password_enabled: bool | Unset = UNSET
    enable_signup: bool | Unset = UNSET
    post_auth_redirect_url: str | Unset = UNSET
    oauth_providers: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        require_email_confirmation = self.require_email_confirmation

        email_password_enabled = self.email_password_enabled

        enable_signup = self.enable_signup

        post_auth_redirect_url = self.post_auth_redirect_url

        oauth_providers: list[str] | Unset = UNSET
        if not isinstance(self.oauth_providers, Unset):
            oauth_providers = self.oauth_providers




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if require_email_confirmation is not UNSET:
            field_dict["require_email_confirmation"] = require_email_confirmation
        if email_password_enabled is not UNSET:
            field_dict["email_password_enabled"] = email_password_enabled
        if enable_signup is not UNSET:
            field_dict["enable_signup"] = enable_signup
        if post_auth_redirect_url is not UNSET:
            field_dict["post_auth_redirect_url"] = post_auth_redirect_url
        if oauth_providers is not UNSET:
            field_dict["oauth_providers"] = oauth_providers

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        require_email_confirmation = d.pop("require_email_confirmation", UNSET)

        email_password_enabled = d.pop("email_password_enabled", UNSET)

        enable_signup = d.pop("enable_signup", UNSET)

        post_auth_redirect_url = d.pop("post_auth_redirect_url", UNSET)

        oauth_providers = cast(list[str], d.pop("oauth_providers", UNSET))


        hosted_login_options_response = cls(
            require_email_confirmation=require_email_confirmation,
            email_password_enabled=email_password_enabled,
            enable_signup=enable_signup,
            post_auth_redirect_url=post_auth_redirect_url,
            oauth_providers=oauth_providers,
        )


        hosted_login_options_response.additional_properties = d
        return hosted_login_options_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
