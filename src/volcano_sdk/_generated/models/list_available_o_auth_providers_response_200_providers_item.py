from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ListAvailableOAuthProvidersResponse200ProvidersItem")



@_attrs_define
class ListAvailableOAuthProvidersResponse200ProvidersItem:
    """ 
        Attributes:
            id (str | Unset):
            name (str | Unset):
            default_scopes (list[str] | Unset):
     """

    id: str | Unset = UNSET
    name: str | Unset = UNSET
    default_scopes: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        default_scopes: list[str] | Unset = UNSET
        if not isinstance(self.default_scopes, Unset):
            default_scopes = self.default_scopes




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if default_scopes is not UNSET:
            field_dict["default_scopes"] = default_scopes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        default_scopes = cast(list[str], d.pop("default_scopes", UNSET))


        list_available_o_auth_providers_response_200_providers_item = cls(
            id=id,
            name=name,
            default_scopes=default_scopes,
        )


        list_available_o_auth_providers_response_200_providers_item.additional_properties = d
        return list_available_o_auth_providers_response_200_providers_item

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
