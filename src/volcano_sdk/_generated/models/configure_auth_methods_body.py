from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.configure_auth_methods_body_oauth_providers_item import ConfigureAuthMethodsBodyOauthProvidersItem





T = TypeVar("T", bound="ConfigureAuthMethodsBody")



@_attrs_define
class ConfigureAuthMethodsBody:
    """ 
        Attributes:
            enable_email_password (bool | Unset):
            enable_anonymous (bool | Unset):
            oauth_providers (list[ConfigureAuthMethodsBodyOauthProvidersItem] | Unset):
     """

    enable_email_password: bool | Unset = UNSET
    enable_anonymous: bool | Unset = UNSET
    oauth_providers: list[ConfigureAuthMethodsBodyOauthProvidersItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.configure_auth_methods_body_oauth_providers_item import ConfigureAuthMethodsBodyOauthProvidersItem
        enable_email_password = self.enable_email_password

        enable_anonymous = self.enable_anonymous

        oauth_providers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.oauth_providers, Unset):
            oauth_providers = []
            for oauth_providers_item_data in self.oauth_providers:
                oauth_providers_item = oauth_providers_item_data.to_dict()
                oauth_providers.append(oauth_providers_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if enable_email_password is not UNSET:
            field_dict["enable_email_password"] = enable_email_password
        if enable_anonymous is not UNSET:
            field_dict["enable_anonymous"] = enable_anonymous
        if oauth_providers is not UNSET:
            field_dict["oauth_providers"] = oauth_providers

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.configure_auth_methods_body_oauth_providers_item import ConfigureAuthMethodsBodyOauthProvidersItem
        d = dict(src_dict)
        enable_email_password = d.pop("enable_email_password", UNSET)

        enable_anonymous = d.pop("enable_anonymous", UNSET)

        _oauth_providers = d.pop("oauth_providers", UNSET)
        oauth_providers: list[ConfigureAuthMethodsBodyOauthProvidersItem] | Unset = UNSET
        if _oauth_providers is not UNSET:
            oauth_providers = []
            for oauth_providers_item_data in _oauth_providers:
                oauth_providers_item = ConfigureAuthMethodsBodyOauthProvidersItem.from_dict(oauth_providers_item_data)



                oauth_providers.append(oauth_providers_item)


        configure_auth_methods_body = cls(
            enable_email_password=enable_email_password,
            enable_anonymous=enable_anonymous,
            oauth_providers=oauth_providers,
        )


        configure_auth_methods_body.additional_properties = d
        return configure_auth_methods_body

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
