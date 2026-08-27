from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="DeviceAuthorizationResponse")



@_attrs_define
class DeviceAuthorizationResponse:
    """ 
        Attributes:
            device_code (str):
            user_code (str):
            verification_uri (str): Browser verification URL. Points at the project's managed device
                approval page served by this API:
                `/projects/{projectId}/auth/hosted?action=device&anon_key=...`.
                Requires the project to have managed auth enabled and a default anon
                key. A custom CLI may ignore this and direct users to its own
                RFC 8628-compatible page instead (see the device-auth guide).
            verification_uri_complete (str): Same as `verification_uri` but with the `user_code` prefilled
                (`&user_code=...`). This is the URL most device clients open.
            expires_in (int):
            interval (int):
     """

    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        device_code = self.device_code

        user_code = self.user_code

        verification_uri = self.verification_uri

        verification_uri_complete = self.verification_uri_complete

        expires_in = self.expires_in

        interval = self.interval


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "device_code": device_code,
            "user_code": user_code,
            "verification_uri": verification_uri,
            "verification_uri_complete": verification_uri_complete,
            "expires_in": expires_in,
            "interval": interval,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        device_code = d.pop("device_code")

        user_code = d.pop("user_code")

        verification_uri = d.pop("verification_uri")

        verification_uri_complete = d.pop("verification_uri_complete")

        expires_in = d.pop("expires_in")

        interval = d.pop("interval")

        device_authorization_response = cls(
            device_code=device_code,
            user_code=user_code,
            verification_uri=verification_uri,
            verification_uri_complete=verification_uri_complete,
            expires_in=expires_in,
            interval=interval,
        )


        device_authorization_response.additional_properties = d
        return device_authorization_response

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
