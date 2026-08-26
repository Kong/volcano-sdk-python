from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="AuthIdentity")



@_attrs_define
class AuthIdentity:
    """ A real email identity owned by the account. One account can own multiple
    identities (for example a work email plus a personal email linked via OAuth).

        Attributes:
            id (UUID): Unique identity identifier
            email (str): The email address this identity represents
            email_verified (bool): Whether ownership of this email has been verified
            is_primary (bool): Whether the account's primary sign-in method resolves to this identity
            created_at (datetime.datetime):
     """

    id: UUID
    email: str
    email_verified: bool
    is_primary: bool
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        email = self.email

        email_verified = self.email_verified

        is_primary = self.is_primary

        created_at = self.created_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "email": email,
            "email_verified": email_verified,
            "is_primary": is_primary,
            "created_at": created_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        email = d.pop("email")

        email_verified = d.pop("email_verified")

        is_primary = d.pop("is_primary")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        auth_identity = cls(
            id=id,
            email=email,
            email_verified=email_verified,
            is_primary=is_primary,
            created_at=created_at,
        )


        auth_identity.additional_properties = d
        return auth_identity

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
