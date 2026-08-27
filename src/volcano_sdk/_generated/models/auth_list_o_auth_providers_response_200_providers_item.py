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
            provider (str | Unset):
            linked_at (datetime.datetime | Unset):
            updated_at (datetime.datetime | Unset):
     """

    provider: str | Unset = UNSET
    linked_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        provider = self.provider

        linked_at: str | Unset = UNSET
        if not isinstance(self.linked_at, Unset):
            linked_at = self.linked_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if provider is not UNSET:
            field_dict["provider"] = provider
        if linked_at is not UNSET:
            field_dict["linked_at"] = linked_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider = d.pop("provider", UNSET)

        _linked_at = d.pop("linked_at", UNSET)
        linked_at: datetime.datetime | Unset
        if isinstance(_linked_at,  Unset):
            linked_at = UNSET
        else:
            linked_at = datetime.datetime.fromisoformat(_linked_at)




        _updated_at = d.pop("updated_at", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at,  Unset):
            updated_at = UNSET
        else:
            updated_at = datetime.datetime.fromisoformat(_updated_at)




        auth_list_o_auth_providers_response_200_providers_item = cls(
            provider=provider,
            linked_at=linked_at,
            updated_at=updated_at,
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
