from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.get_auth_methods_response_200_anonymous import GetAuthMethodsResponse200Anonymous
  from ..models.get_auth_methods_response_200_email_password import GetAuthMethodsResponse200EmailPassword
  from ..models.get_auth_methods_response_200_oauth_providers_item import GetAuthMethodsResponse200OauthProvidersItem





T = TypeVar("T", bound="GetAuthMethodsResponse200")



@_attrs_define
class GetAuthMethodsResponse200:
    """ 
        Attributes:
            email_password (GetAuthMethodsResponse200EmailPassword | Unset):
            anonymous (GetAuthMethodsResponse200Anonymous | Unset):
            oauth_providers (list[GetAuthMethodsResponse200OauthProvidersItem] | Unset):
            available_methods (list[str] | Unset):  Example: ['email_password', 'oauth_google', 'oauth_github'].
     """

    email_password: GetAuthMethodsResponse200EmailPassword | Unset = UNSET
    anonymous: GetAuthMethodsResponse200Anonymous | Unset = UNSET
    oauth_providers: list[GetAuthMethodsResponse200OauthProvidersItem] | Unset = UNSET
    available_methods: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.get_auth_methods_response_200_anonymous import GetAuthMethodsResponse200Anonymous
        from ..models.get_auth_methods_response_200_email_password import GetAuthMethodsResponse200EmailPassword
        from ..models.get_auth_methods_response_200_oauth_providers_item import GetAuthMethodsResponse200OauthProvidersItem
        email_password: dict[str, Any] | Unset = UNSET
        if not isinstance(self.email_password, Unset):
            email_password = self.email_password.to_dict()

        anonymous: dict[str, Any] | Unset = UNSET
        if not isinstance(self.anonymous, Unset):
            anonymous = self.anonymous.to_dict()

        oauth_providers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.oauth_providers, Unset):
            oauth_providers = []
            for oauth_providers_item_data in self.oauth_providers:
                oauth_providers_item = oauth_providers_item_data.to_dict()
                oauth_providers.append(oauth_providers_item)



        available_methods: list[str] | Unset = UNSET
        if not isinstance(self.available_methods, Unset):
            available_methods = self.available_methods




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if email_password is not UNSET:
            field_dict["email_password"] = email_password
        if anonymous is not UNSET:
            field_dict["anonymous"] = anonymous
        if oauth_providers is not UNSET:
            field_dict["oauth_providers"] = oauth_providers
        if available_methods is not UNSET:
            field_dict["available_methods"] = available_methods

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_auth_methods_response_200_anonymous import GetAuthMethodsResponse200Anonymous
        from ..models.get_auth_methods_response_200_email_password import GetAuthMethodsResponse200EmailPassword
        from ..models.get_auth_methods_response_200_oauth_providers_item import GetAuthMethodsResponse200OauthProvidersItem
        d = dict(src_dict)
        _email_password = d.pop("email_password", UNSET)
        email_password: GetAuthMethodsResponse200EmailPassword | Unset
        if isinstance(_email_password,  Unset):
            email_password = UNSET
        else:
            email_password = GetAuthMethodsResponse200EmailPassword.from_dict(_email_password)




        _anonymous = d.pop("anonymous", UNSET)
        anonymous: GetAuthMethodsResponse200Anonymous | Unset
        if isinstance(_anonymous,  Unset):
            anonymous = UNSET
        else:
            anonymous = GetAuthMethodsResponse200Anonymous.from_dict(_anonymous)




        _oauth_providers = d.pop("oauth_providers", UNSET)
        oauth_providers: list[GetAuthMethodsResponse200OauthProvidersItem] | Unset = UNSET
        if _oauth_providers is not UNSET:
            oauth_providers = []
            for oauth_providers_item_data in _oauth_providers:
                oauth_providers_item = GetAuthMethodsResponse200OauthProvidersItem.from_dict(oauth_providers_item_data)



                oauth_providers.append(oauth_providers_item)


        available_methods = cast(list[str], d.pop("available_methods", UNSET))


        get_auth_methods_response_200 = cls(
            email_password=email_password,
            anonymous=anonymous,
            oauth_providers=oauth_providers,
            available_methods=available_methods,
        )


        get_auth_methods_response_200.additional_properties = d
        return get_auth_methods_response_200

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
