from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_access_token_scope import check_project_access_token_scope
from ..models.project_access_token_scope import ProjectAccessTokenScope
from ..models.project_access_token_status import check_project_access_token_status
from ..models.project_access_token_status import ProjectAccessTokenStatus
from ..models.project_access_token_token_source import check_project_access_token_token_source
from ..models.project_access_token_token_source import ProjectAccessTokenTokenSource
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="CreatedProjectAccessToken")



@_attrs_define
class CreatedProjectAccessToken:
    """ 
        Attributes:
            id (UUID):
            project_id (UUID):
            name (str): Unique per project.
            token_prefix (str): First 12 characters of the secret, for recognising a token in a list.
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
            status (ProjectAccessTokenStatus): `revoked` means the token was deliberately revoked, by you or by the
                deletion of its project. `expired` means it simply reached
                `expires_at`; nothing was taken away. Both are refused, and both keep
                their record so a token's name, prefix, last use, and request history
                remain available after a leak.

                A token revoked before its expiry passed stays `revoked`, because
                that is the fact worth keeping.
            token_source (ProjectAccessTokenTokenSource): What created the token.
            created_at (datetime.datetime):
            all_time_requests (int): Requests authenticated with this token since it was created.
            token (str): The secret. Returned only here, and not recoverable afterwards:
                the server stores a hash rather than the value. Save it now.
            expires_at (datetime.datetime | None | Unset): Absent for a token that does not expire.
            last_used_at (datetime.datetime | None | Unset): Updated at most once every few minutes, so it may lag slightly.
     """

    id: UUID
    project_id: UUID
    name: str
    token_prefix: str
    scope: ProjectAccessTokenScope
    status: ProjectAccessTokenStatus
    token_source: ProjectAccessTokenTokenSource
    created_at: datetime.datetime
    all_time_requests: int
    token: str
    expires_at: datetime.datetime | None | Unset = UNSET
    last_used_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id = str(self.project_id)

        name = self.name

        token_prefix = self.token_prefix

        scope: str = self.scope

        status: str = self.status

        token_source: str = self.token_source

        created_at = self.created_at.isoformat()

        all_time_requests = self.all_time_requests

        token = self.token

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        last_used_at: None | str | Unset
        if isinstance(self.last_used_at, Unset):
            last_used_at = UNSET
        elif isinstance(self.last_used_at, datetime.datetime):
            last_used_at = self.last_used_at.isoformat()
        else:
            last_used_at = self.last_used_at


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "project_id": project_id,
            "name": name,
            "token_prefix": token_prefix,
            "scope": scope,
            "status": status,
            "token_source": token_source,
            "created_at": created_at,
            "all_time_requests": all_time_requests,
            "token": token,
        })
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        name = d.pop("name")

        token_prefix = d.pop("token_prefix")

        scope = check_project_access_token_scope(d.pop("scope"))




        status = check_project_access_token_status(d.pop("status"))




        token_source = check_project_access_token_token_source(d.pop("token_source"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        all_time_requests = d.pop("all_time_requests")

        token = d.pop("token")

        def _parse_expires_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = datetime.datetime.fromisoformat(data)



                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))


        def _parse_last_used_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_used_at_type_0 = datetime.datetime.fromisoformat(data)



                return last_used_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_used_at = _parse_last_used_at(d.pop("last_used_at", UNSET))


        created_project_access_token = cls(
            id=id,
            project_id=project_id,
            name=name,
            token_prefix=token_prefix,
            scope=scope,
            status=status,
            token_source=token_source,
            created_at=created_at,
            all_time_requests=all_time_requests,
            token=token,
            expires_at=expires_at,
            last_used_at=last_used_at,
        )


        created_project_access_token.additional_properties = d
        return created_project_access_token

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
