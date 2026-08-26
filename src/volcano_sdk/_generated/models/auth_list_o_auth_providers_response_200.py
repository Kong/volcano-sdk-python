from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.auth_list_o_auth_providers_response_200_providers_item import AuthListOAuthProvidersResponse200ProvidersItem





T = TypeVar("T", bound="AuthListOAuthProvidersResponse200")



@_attrs_define
class AuthListOAuthProvidersResponse200:
    """ 
        Attributes:
            providers (list[AuthListOAuthProvidersResponse200ProvidersItem] | Unset):
     """

    providers: list[AuthListOAuthProvidersResponse200ProvidersItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_list_o_auth_providers_response_200_providers_item import AuthListOAuthProvidersResponse200ProvidersItem
        providers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.providers, Unset):
            providers = []
            for providers_item_data in self.providers:
                providers_item = providers_item_data.to_dict()
                providers.append(providers_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if providers is not UNSET:
            field_dict["providers"] = providers

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_list_o_auth_providers_response_200_providers_item import AuthListOAuthProvidersResponse200ProvidersItem
        d = dict(src_dict)
        _providers = d.pop("providers", UNSET)
        providers: list[AuthListOAuthProvidersResponse200ProvidersItem] | Unset = UNSET
        if _providers is not UNSET:
            providers = []
            for providers_item_data in _providers:
                providers_item = AuthListOAuthProvidersResponse200ProvidersItem.from_dict(providers_item_data)



                providers.append(providers_item)


        auth_list_o_auth_providers_response_200 = cls(
            providers=providers,
        )


        auth_list_o_auth_providers_response_200.additional_properties = d
        return auth_list_o_auth_providers_response_200

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
