from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="GetAuthMethodsResponse200OauthProvidersItem")



@_attrs_define
class GetAuthMethodsResponse200OauthProvidersItem:
    """ 
        Attributes:
            enabled (bool | Unset):
            method (str | Unset):
            provider (str | Unset):
            name (str | Unset):
            redirect_url (str | Unset):
            scopes (list[str] | Unset):
     """

    enabled: bool | Unset = UNSET
    method: str | Unset = UNSET
    provider: str | Unset = UNSET
    name: str | Unset = UNSET
    redirect_url: str | Unset = UNSET
    scopes: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        method = self.method

        provider = self.provider

        name = self.name

        redirect_url = self.redirect_url

        scopes: list[str] | Unset = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if method is not UNSET:
            field_dict["method"] = method
        if provider is not UNSET:
            field_dict["provider"] = provider
        if name is not UNSET:
            field_dict["name"] = name
        if redirect_url is not UNSET:
            field_dict["redirect_url"] = redirect_url
        if scopes is not UNSET:
            field_dict["scopes"] = scopes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        method = d.pop("method", UNSET)

        provider = d.pop("provider", UNSET)

        name = d.pop("name", UNSET)

        redirect_url = d.pop("redirect_url", UNSET)

        scopes = cast(list[str], d.pop("scopes", UNSET))


        get_auth_methods_response_200_oauth_providers_item = cls(
            enabled=enabled,
            method=method,
            provider=provider,
            name=name,
            redirect_url=redirect_url,
            scopes=scopes,
        )


        get_auth_methods_response_200_oauth_providers_item.additional_properties = d
        return get_auth_methods_response_200_oauth_providers_item

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
