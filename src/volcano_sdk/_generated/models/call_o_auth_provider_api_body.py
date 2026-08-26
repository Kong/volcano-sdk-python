from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.call_o_auth_provider_api_body_method import CallOAuthProviderAPIBodyMethod
from ..models.call_o_auth_provider_api_body_method import check_call_o_auth_provider_api_body_method
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.call_o_auth_provider_api_body_body import CallOAuthProviderAPIBodyBody





T = TypeVar("T", bound="CallOAuthProviderAPIBody")



@_attrs_define
class CallOAuthProviderAPIBody:
    """ 
        Attributes:
            endpoint (str): Relative path on the provider's API, beginning with `/`. It is
                joined with the provider's fixed base URL; it must not contain a
                scheme, host, userinfo, or a leading `//`.
                 Example: /user/repos.
            method (CallOAuthProviderAPIBodyMethod | Unset): HTTP method to use Default: 'GET'.
            body (CallOAuthProviderAPIBodyBody | Unset): Request body for POST requests
     """

    endpoint: str
    method: CallOAuthProviderAPIBodyMethod | Unset = 'GET'
    body: CallOAuthProviderAPIBodyBody | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.call_o_auth_provider_api_body_body import CallOAuthProviderAPIBodyBody
        endpoint = self.endpoint

        method: str | Unset = UNSET
        if not isinstance(self.method, Unset):
            method = self.method


        body: dict[str, Any] | Unset = UNSET
        if not isinstance(self.body, Unset):
            body = self.body.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "endpoint": endpoint,
        })
        if method is not UNSET:
            field_dict["method"] = method
        if body is not UNSET:
            field_dict["body"] = body

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_o_auth_provider_api_body_body import CallOAuthProviderAPIBodyBody
        d = dict(src_dict)
        endpoint = d.pop("endpoint")

        _method = d.pop("method", UNSET)
        method: CallOAuthProviderAPIBodyMethod | Unset
        if isinstance(_method,  Unset):
            method = UNSET
        else:
            method = check_call_o_auth_provider_api_body_method(_method)




        _body = d.pop("body", UNSET)
        body: CallOAuthProviderAPIBodyBody | Unset
        if isinstance(_body,  Unset):
            body = UNSET
        else:
            body = CallOAuthProviderAPIBodyBody.from_dict(_body)




        call_o_auth_provider_api_body = cls(
            endpoint=endpoint,
            method=method,
            body=body,
        )


        call_o_auth_provider_api_body.additional_properties = d
        return call_o_auth_provider_api_body

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
