from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.o_auth_config_provider import check_o_auth_config_provider
from ..models.o_auth_config_provider import OAuthConfigProvider
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="OAuthConfig")



@_attrs_define
class OAuthConfig:
    """ 
        Attributes:
            id (UUID | Unset):
            provider (OAuthConfigProvider | Unset):
            client_id (str | Unset):  Example: 123456789.apps.googleusercontent.com.
            client_secret (str | Unset): Masked in responses (shows only first/last 4 chars) Example: GOCS...****.
            enabled (bool | Unset):
            redirect_url (str | Unset):  Example: https://yourapp.com/auth/callback.
            scopes (list[str] | Unset):  Example: ['openid', 'email', 'profile'].
            created_at (datetime.datetime | Unset):
            updated_at (datetime.datetime | Unset):
     """

    id: UUID | Unset = UNSET
    provider: OAuthConfigProvider | Unset = UNSET
    client_id: str | Unset = UNSET
    client_secret: str | Unset = UNSET
    enabled: bool | Unset = UNSET
    redirect_url: str | Unset = UNSET
    scopes: list[str] | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id: str | Unset = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        provider: str | Unset = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider


        client_id = self.client_id

        client_secret = self.client_secret

        enabled = self.enabled

        redirect_url = self.redirect_url

        scopes: list[str] | Unset = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes



        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if provider is not UNSET:
            field_dict["provider"] = provider
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_secret is not UNSET:
            field_dict["client_secret"] = client_secret
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if redirect_url is not UNSET:
            field_dict["redirect_url"] = redirect_url
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _id = d.pop("id", UNSET)
        id: UUID | Unset
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        _provider = d.pop("provider", UNSET)
        provider: OAuthConfigProvider | Unset
        if isinstance(_provider,  Unset):
            provider = UNSET
        else:
            provider = check_o_auth_config_provider(_provider)




        client_id = d.pop("client_id", UNSET)

        client_secret = d.pop("client_secret", UNSET)

        enabled = d.pop("enabled", UNSET)

        redirect_url = d.pop("redirect_url", UNSET)

        scopes = cast(list[str], d.pop("scopes", UNSET))


        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)




        _updated_at = d.pop("updated_at", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at,  Unset):
            updated_at = UNSET
        else:
            updated_at = datetime.datetime.fromisoformat(_updated_at)




        o_auth_config = cls(
            id=id,
            provider=provider,
            client_id=client_id,
            client_secret=client_secret,
            enabled=enabled,
            redirect_url=redirect_url,
            scopes=scopes,
            created_at=created_at,
            updated_at=updated_at,
        )


        o_auth_config.additional_properties = d
        return o_auth_config

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
