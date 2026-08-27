from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.auth_user import AuthUser





T = TypeVar("T", bound="AuthTokenResponse")



@_attrs_define
class AuthTokenResponse:
    """ 
        Attributes:
            access_token (str): JWT access token (expires after configured lifetime)
            token_type (str):  Example: bearer.
            expires_in (int): Access token lifetime in seconds
            user (AuthUser):
            refresh_token (str | Unset): Long-lived token for getting new access tokens. Omitted when the
                request uses eligible HttpOnly cookie session storage.
     """

    access_token: str
    token_type: str
    expires_in: int
    user: AuthUser
    refresh_token: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_user import AuthUser
        access_token = self.access_token

        token_type = self.token_type

        expires_in = self.expires_in

        user = self.user.to_dict()

        refresh_token = self.refresh_token


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "access_token": access_token,
            "token_type": token_type,
            "expires_in": expires_in,
            "user": user,
        })
        if refresh_token is not UNSET:
            field_dict["refresh_token"] = refresh_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_user import AuthUser
        d = dict(src_dict)
        access_token = d.pop("access_token")

        token_type = d.pop("token_type")

        expires_in = d.pop("expires_in")

        user = AuthUser.from_dict(d.pop("user"))




        refresh_token = d.pop("refresh_token", UNSET)

        auth_token_response = cls(
            access_token=access_token,
            token_type=token_type,
            expires_in=expires_in,
            user=user,
            refresh_token=refresh_token,
        )


        auth_token_response.additional_properties = d
        return auth_token_response

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
