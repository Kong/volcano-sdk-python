from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="AuthListOAuthProvidersResponse200ProvidersItem")



@_attrs_define
class AuthListOAuthProvidersResponse200ProvidersItem:
    """ 
        Attributes:
            provider (str):
            provider_user_id (str): The user's account ID at the provider, as a string.
                It stays the same when the user renames the account.
                 Example: 583231.
            linked_at (datetime.datetime):
            updated_at (datetime.datetime):
            provider_login (str | Unset): The account's login at the provider when it was
                linked, such as a GitHub username. It isn't updated
                when the user renames the account. Omitted for
                providers without logins.
                 Example: octocat.
     """

    provider: str
    provider_user_id: str
    linked_at: datetime.datetime
    updated_at: datetime.datetime
    provider_login: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        provider = self.provider

        provider_user_id = self.provider_user_id

        linked_at = self.linked_at.isoformat()

        updated_at = self.updated_at.isoformat()

        provider_login = self.provider_login


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "provider": provider,
            "provider_user_id": provider_user_id,
            "linked_at": linked_at,
            "updated_at": updated_at,
        })
        if provider_login is not UNSET:
            field_dict["provider_login"] = provider_login

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider = d.pop("provider")

        provider_user_id = d.pop("provider_user_id")

        linked_at = datetime.datetime.fromisoformat(d.pop("linked_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        provider_login = d.pop("provider_login", UNSET)

        auth_list_o_auth_providers_response_200_providers_item = cls(
            provider=provider,
            provider_user_id=provider_user_id,
            linked_at=linked_at,
            updated_at=updated_at,
            provider_login=provider_login,
        )


        auth_list_o_auth_providers_response_200_providers_item.additional_properties = d
        return auth_list_o_auth_providers_response_200_providers_item

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
