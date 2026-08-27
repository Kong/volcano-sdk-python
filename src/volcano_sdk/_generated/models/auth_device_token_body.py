from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auth_device_token_body_grant_type import AuthDeviceTokenBodyGrantType
from ..models.auth_device_token_body_grant_type import check_auth_device_token_body_grant_type
from typing import cast






T = TypeVar("T", bound="AuthDeviceTokenBody")



@_attrs_define
class AuthDeviceTokenBody:
    """ 
        Attributes:
            grant_type (AuthDeviceTokenBodyGrantType):
            device_code (str):
            client_id (str):
     """

    grant_type: AuthDeviceTokenBodyGrantType
    device_code: str
    client_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        grant_type: str = self.grant_type

        device_code = self.device_code

        client_id = self.client_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "grant_type": grant_type,
            "device_code": device_code,
            "client_id": client_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        grant_type = check_auth_device_token_body_grant_type(d.pop("grant_type"))




        device_code = d.pop("device_code")

        client_id = d.pop("client_id")

        auth_device_token_body = cls(
            grant_type=grant_type,
            device_code=device_code,
            client_id=client_id,
        )


        auth_device_token_body.additional_properties = d
        return auth_device_token_body

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
