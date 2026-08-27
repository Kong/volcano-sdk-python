from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="UpdateOAuthConfigRequest")



@_attrs_define
class UpdateOAuthConfigRequest:
    """ 
        Attributes:
            client_id (str | Unset): Supported for non-device providers. Not supported for `provider=device`.
            client_secret (str | Unset): Supported for non-device providers. Not supported for `provider=device`.
            redirect_url (str | Unset):
            scopes (list[str] | Unset):
            enabled (bool | Unset):
     """

    client_id: str | Unset = UNSET
    client_secret: str | Unset = UNSET
    redirect_url: str | Unset = UNSET
    scopes: list[str] | Unset = UNSET
    enabled: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        client_id = self.client_id

        client_secret = self.client_secret

        redirect_url = self.redirect_url

        scopes: list[str] | Unset = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes



        enabled = self.enabled


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_secret is not UNSET:
            field_dict["client_secret"] = client_secret
        if redirect_url is not UNSET:
            field_dict["redirect_url"] = redirect_url
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_id = d.pop("client_id", UNSET)

        client_secret = d.pop("client_secret", UNSET)

        redirect_url = d.pop("redirect_url", UNSET)

        scopes = cast(list[str], d.pop("scopes", UNSET))


        enabled = d.pop("enabled", UNSET)

        update_o_auth_config_request = cls(
            client_id=client_id,
            client_secret=client_secret,
            redirect_url=redirect_url,
            scopes=scopes,
            enabled=enabled,
        )


        update_o_auth_config_request.additional_properties = d
        return update_o_auth_config_request

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
