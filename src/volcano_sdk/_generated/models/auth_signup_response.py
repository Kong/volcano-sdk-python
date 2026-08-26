from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AuthSignupResponse")



@_attrs_define
class AuthSignupResponse:
    """ Uniform, session-less response returned by POST /auth/signup. It carries no
    tokens and no user object, and is identical for a new account and for an
    already-registered email (anti-enumeration). Clients obtain a session with a
    subsequent POST /auth/signin.

        Attributes:
            confirmation_required (bool): Whether the project requires email confirmation. Reflects project config
                only (identical for a new and an existing email), so it leaks nothing about
                account existence.
            message (str): Human-readable acknowledgement.
     """

    confirmation_required: bool
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        confirmation_required = self.confirmation_required

        message = self.message


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "confirmation_required": confirmation_required,
            "message": message,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        confirmation_required = d.pop("confirmation_required")

        message = d.pop("message")

        auth_signup_response = cls(
            confirmation_required=confirmation_required,
            message=message,
        )


        auth_signup_response.additional_properties = d
        return auth_signup_response

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
