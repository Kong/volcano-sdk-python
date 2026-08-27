from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.auth_update_user_body_user_metadata import AuthUpdateUserBodyUserMetadata





T = TypeVar("T", bound="AuthUpdateUserBody")



@_attrs_define
class AuthUpdateUserBody:
    """ 
        Attributes:
            password (str | Unset): Password validated after NFC normalization against the
                policy returned by GET /auth/password-policy.
            user_metadata (AuthUpdateUserBodyUserMetadata | Unset): Metadata keys to merge into the current user metadata.
                Omitted keys remain unchanged; set a key to null to remove it.
                Merging is shallow; nested objects replace the stored value for that top-level key.
     """

    password: str | Unset = UNSET
    user_metadata: AuthUpdateUserBodyUserMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_update_user_body_user_metadata import AuthUpdateUserBodyUserMetadata
        password = self.password

        user_metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if password is not UNSET:
            field_dict["password"] = password
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_update_user_body_user_metadata import AuthUpdateUserBodyUserMetadata
        d = dict(src_dict)
        password = d.pop("password", UNSET)

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: AuthUpdateUserBodyUserMetadata | Unset
        if isinstance(_user_metadata,  Unset):
            user_metadata = UNSET
        else:
            user_metadata = AuthUpdateUserBodyUserMetadata.from_dict(_user_metadata)




        auth_update_user_body = cls(
            password=password,
            user_metadata=user_metadata,
        )


        auth_update_user_body.additional_properties = d
        return auth_update_user_body

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
