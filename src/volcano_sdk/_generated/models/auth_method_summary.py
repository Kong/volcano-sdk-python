from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auth_method_summary_type import AuthMethodSummaryType
from ..models.auth_method_summary_type import check_auth_method_summary_type
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="AuthMethodSummary")



@_attrs_define
class AuthMethodSummary:
    """ A single sign-in method the account owns (password, an OAuth provider, or an
    active anonymous method). `is_primary` reflects the account's primary_method_id.

        Attributes:
            id (UUID): Unique method identifier
            type_ (AuthMethodSummaryType): The kind of sign-in method
            identity_id (str): The identity this method signs in to — a UUID for password/oauth methods,
                empty for anonymous methods.
            email (str): The email of the method's identity (empty for anonymous)
            is_primary (bool): Whether this is the account's primary sign-in method
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            provider (str | Unset): OAuth provider name; present only when type is oauth Example: google.
            last_used_at (datetime.datetime | Unset): When this method was last used to sign in, if ever
     """

    id: UUID
    type_: AuthMethodSummaryType
    identity_id: str
    email: str
    is_primary: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    provider: str | Unset = UNSET
    last_used_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        type_: str = self.type_

        identity_id = self.identity_id

        email = self.email

        is_primary = self.is_primary

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        provider = self.provider

        last_used_at: str | Unset = UNSET
        if not isinstance(self.last_used_at, Unset):
            last_used_at = self.last_used_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "type": type_,
            "identity_id": identity_id,
            "email": email,
            "is_primary": is_primary,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if provider is not UNSET:
            field_dict["provider"] = provider
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        type_ = check_auth_method_summary_type(d.pop("type"))




        identity_id = d.pop("identity_id")

        email = d.pop("email")

        is_primary = d.pop("is_primary")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        provider = d.pop("provider", UNSET)

        _last_used_at = d.pop("last_used_at", UNSET)
        last_used_at: datetime.datetime | Unset
        if isinstance(_last_used_at,  Unset):
            last_used_at = UNSET
        else:
            last_used_at = datetime.datetime.fromisoformat(_last_used_at)




        auth_method_summary = cls(
            id=id,
            type_=type_,
            identity_id=identity_id,
            email=email,
            is_primary=is_primary,
            created_at=created_at,
            updated_at=updated_at,
            provider=provider,
            last_used_at=last_used_at,
        )


        auth_method_summary.additional_properties = d
        return auth_method_summary

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
