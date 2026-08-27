from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.auth_signup_body_user_metadata import AuthSignupBodyUserMetadata





T = TypeVar("T", bound="AuthSignupBody")



@_attrs_define
class AuthSignupBody:
    """ 
        Attributes:
            email (str):
            password (str): Password validated after NFC normalization against the
                policy returned by GET /auth/password-policy.
            user_metadata (AuthSignupBodyUserMetadata | Unset):
     """

    email: str
    password: str
    user_metadata: AuthSignupBodyUserMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_signup_body_user_metadata import AuthSignupBodyUserMetadata
        email = self.email

        password = self.password

        user_metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "email": email,
            "password": password,
        })
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_signup_body_user_metadata import AuthSignupBodyUserMetadata
        d = dict(src_dict)
        email = d.pop("email")

        password = d.pop("password")

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: AuthSignupBodyUserMetadata | Unset
        if isinstance(_user_metadata,  Unset):
            user_metadata = UNSET
        else:
            user_metadata = AuthSignupBodyUserMetadata.from_dict(_user_metadata)




        auth_signup_body = cls(
            email=email,
            password=password,
            user_metadata=user_metadata,
        )


        auth_signup_body.additional_properties = d
        return auth_signup_body

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
