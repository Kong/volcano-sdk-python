from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.call_o_auth_provider_api_response_200_provider import CallOAuthProviderAPIResponse200Provider
from ..models.call_o_auth_provider_api_response_200_provider import check_call_o_auth_provider_api_response_200_provider
from typing import cast






T = TypeVar("T", bound="CallOAuthProviderAPIResponse200")



@_attrs_define
class CallOAuthProviderAPIResponse200:
    """ OAuth provider API response envelope

        Attributes:
            provider (CallOAuthProviderAPIResponse200Provider):
            endpoint (str):
            status_code (int):
            data (Any): Raw provider JSON value, or null when the provider returns no body
     """

    provider: CallOAuthProviderAPIResponse200Provider
    endpoint: str
    status_code: int
    data: Any
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        provider: str = self.provider

        endpoint = self.endpoint

        status_code = self.status_code

        data = self.data


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "provider": provider,
            "endpoint": endpoint,
            "status_code": status_code,
            "data": data,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider = check_call_o_auth_provider_api_response_200_provider(d.pop("provider"))




        endpoint = d.pop("endpoint")

        status_code = d.pop("status_code")

        data = d.pop("data")

        call_o_auth_provider_api_response_200 = cls(
            provider=provider,
            endpoint=endpoint,
            status_code=status_code,
            data=data,
        )


        call_o_auth_provider_api_response_200.additional_properties = d
        return call_o_auth_provider_api_response_200

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
