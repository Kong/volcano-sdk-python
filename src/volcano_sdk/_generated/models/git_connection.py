from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="GitConnection")



@_attrs_define
class GitConnection:
    """ 
        Attributes:
            id (UUID):
            provider (str):
            provider_user_id (str):
            provider_login (str):
            status (str):
            last_authenticated_at (datetime.datetime):
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
     """

    id: UUID
    provider: str
    provider_user_id: str
    provider_login: str
    status: str
    last_authenticated_at: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        provider = self.provider

        provider_user_id = self.provider_user_id

        provider_login = self.provider_login

        status = self.status

        last_authenticated_at = self.last_authenticated_at.isoformat()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "provider": provider,
            "provider_user_id": provider_user_id,
            "provider_login": provider_login,
            "status": status,
            "last_authenticated_at": last_authenticated_at,
            "created_at": created_at,
            "updated_at": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        provider = d.pop("provider")

        provider_user_id = d.pop("provider_user_id")

        provider_login = d.pop("provider_login")

        status = d.pop("status")

        last_authenticated_at = datetime.datetime.fromisoformat(d.pop("last_authenticated_at"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        git_connection = cls(
            id=id,
            provider=provider,
            provider_user_id=provider_user_id,
            provider_login=provider_login,
            status=status,
            last_authenticated_at=last_authenticated_at,
            created_at=created_at,
            updated_at=updated_at,
        )


        git_connection.additional_properties = d
        return git_connection

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
