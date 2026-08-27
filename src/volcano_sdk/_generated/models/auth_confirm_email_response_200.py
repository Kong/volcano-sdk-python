from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auth_confirm_email_response_200_message import AuthConfirmEmailResponse200Message
from ..models.auth_confirm_email_response_200_message import check_auth_confirm_email_response_200_message
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="AuthConfirmEmailResponse200")



@_attrs_define
class AuthConfirmEmailResponse200:
    """ 
        Attributes:
            message (AuthConfirmEmailResponse200Message | Unset):
     """

    message: AuthConfirmEmailResponse200Message | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        message: str | Unset = UNSET
        if not isinstance(self.message, Unset):
            message = self.message



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _message = d.pop("message", UNSET)
        message: AuthConfirmEmailResponse200Message | Unset
        if isinstance(_message,  Unset):
            message = UNSET
        else:
            message = check_auth_confirm_email_response_200_message(_message)




        auth_confirm_email_response_200 = cls(
            message=message,
        )


        auth_confirm_email_response_200.additional_properties = d
        return auth_confirm_email_response_200

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
