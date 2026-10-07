from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_access_token_scope import check_project_access_token_scope
from ..models.project_access_token_scope import ProjectAccessTokenScope
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="CreateProjectAccessTokenRequest")



@_attrs_define
class CreateProjectAccessTokenRequest:
    """ 
        Attributes:
            name (str): Held by any of the project's tokens you have not revoked, including
                one that has expired. Creating a duplicate returns 409 with code
                `access_token_name_exists`; revoking the holder frees the name, so a
                rotation can keep the name its caller already references.
            scope (ProjectAccessTokenScope): What a project access token may do within its project.

                `full` is everything you can do to that one project, up to and including
                deleting it. It cannot manage access tokens, so a leaked token cannot
                mint a replacement or erase the record of its own use, but for a CI or
                agent credential that only deploys, prefer `read_only` where the job
                allows it.

                `read_only` refuses mutations. It is enforced by route classification
                rather than HTTP method, so the log and metrics query endpoints remain
                available even though they are POST requests that carry body filters.

                `read_only` also refuses the reads that return a credential — service
                keys, anon keys, variable values, and database connection strings. Those
                grant write access over the project's data and keep working after the
                token that fetched them is revoked, so returning one to a read-only
                credential would make the scope a formality. An anon key is included
                because its permissions are chosen per key and may include uploading,
                deleting, and publishing.
            expires_at (datetime.datetime | Unset): Omit for a token that does not expire.
     """

    name: str
    scope: ProjectAccessTokenScope
    expires_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        scope: str = self.scope

        expires_at: str | Unset = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "scope": scope,
        })
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        scope = check_project_access_token_scope(d.pop("scope"))




        _expires_at = d.pop("expires_at", UNSET)
        expires_at: datetime.datetime | Unset
        if isinstance(_expires_at,  Unset):
            expires_at = UNSET
        else:
            expires_at = datetime.datetime.fromisoformat(_expires_at)




        create_project_access_token_request = cls(
            name=name,
            scope=scope,
            expires_at=expires_at,
        )


        create_project_access_token_request.additional_properties = d
        return create_project_access_token_request

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
