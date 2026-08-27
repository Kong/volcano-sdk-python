from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.auth_signup_anonymous_body_user_metadata import AuthSignupAnonymousBodyUserMetadata





T = TypeVar("T", bound="AuthSignupAnonymousBody")



@_attrs_define
class AuthSignupAnonymousBody:
    """ 
        Attributes:
            user_metadata (AuthSignupAnonymousBodyUserMetadata | Unset): Custom user metadata (e.g., display_name,
                avatar_url) Example: {'display_name': 'Alice', 'avatar_url': 'https://example.com/alice.jpg'}.
     """

    user_metadata: AuthSignupAnonymousBodyUserMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_signup_anonymous_body_user_metadata import AuthSignupAnonymousBodyUserMetadata
        user_metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_signup_anonymous_body_user_metadata import AuthSignupAnonymousBodyUserMetadata
        d = dict(src_dict)
        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: AuthSignupAnonymousBodyUserMetadata | Unset
        if isinstance(_user_metadata,  Unset):
            user_metadata = UNSET
        else:
            user_metadata = AuthSignupAnonymousBodyUserMetadata.from_dict(_user_metadata)




        auth_signup_anonymous_body = cls(
            user_metadata=user_metadata,
        )


        auth_signup_anonymous_body.additional_properties = d
        return auth_signup_anonymous_body

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
