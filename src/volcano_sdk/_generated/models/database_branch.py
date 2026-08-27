from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.database_branch_status import check_database_branch_status
from ..models.database_branch_status import DatabaseBranchStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="DatabaseBranch")



@_attrs_define
class DatabaseBranch:
    """ A copy-on-write fork of a database, for development and testing.

    A branch starts as an exact copy of its parent's data and diverges from
    there. It has its own connection string and its own credential, so a
    branch password cannot reach the parent.

    Every branch expires. `expires_at` is a hard deadline: once it passes the
    branch stops accepting connections and is deleted. Use `PATCH` to extend
    a branch you are still working on.

        Attributes:
            id (UUID):
            database_id (UUID): The parent database this branch was forked from.
            project_id (UUID):
            name (str): Branch name, unique within the parent database.
            status (DatabaseBranchStatus): Branch status. A new branch starts `provisioning` and is not
                connectable until it reports `active`; poll this endpoint until it
                does. `connection_string` is only present while `active`.

                `provisioning` also covers a branch being rebuilt after a `reset`,
                and a build that is between retries, so it is the status to keep
                waiting on. `failed` is terminal: it means the platform gave up, and
                the branch will not become `active` on its own.
            ttl_seconds (int): The lifetime the branch was created with. Resetting a branch re-arms
                this same duration, so a reset never shortens a branch's remaining
                life.
            expires_at (datetime.datetime): When the branch stops serving connections and becomes eligible for
                deletion. Enforced on the connection path, so it holds even if
                reclamation is delayed.
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            connection_string (str | Unset): PostgreSQL connection URI for this branch. Present only while the
                branch is `active`.

                The URI carries the branch's own globally-unique username and
                password; `application_name` selects the access mode exactly as it
                does for the parent database:
                - `volcano_full_access` — Full admin access (DDL, migrations)
                - `volcano_user_access:{user_id}` — User impersonation (RLS enforced)
                - `volcano_user_access` — Anonymous access (anon role, RLS enforced)
            storage_bytes (int | Unset): Bytes this branch has diverged from its parent, which is what a
                branch actually costs. Shared pages are not counted twice. Counts
                against the parent database's storage allowance. Absent until the
                branch has been sampled.
            last_invoked_at (datetime.datetime | Unset): Most recent request timestamp for this branch
     """

    id: UUID
    database_id: UUID
    project_id: UUID
    name: str
    status: DatabaseBranchStatus
    ttl_seconds: int
    expires_at: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime
    connection_string: str | Unset = UNSET
    storage_bytes: int | Unset = UNSET
    last_invoked_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        database_id = str(self.database_id)

        project_id = str(self.project_id)

        name = self.name

        status: str = self.status

        ttl_seconds = self.ttl_seconds

        expires_at = self.expires_at.isoformat()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        connection_string = self.connection_string

        storage_bytes = self.storage_bytes

        last_invoked_at: str | Unset = UNSET
        if not isinstance(self.last_invoked_at, Unset):
            last_invoked_at = self.last_invoked_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "database_id": database_id,
            "project_id": project_id,
            "name": name,
            "status": status,
            "ttl_seconds": ttl_seconds,
            "expires_at": expires_at,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if connection_string is not UNSET:
            field_dict["connection_string"] = connection_string
        if storage_bytes is not UNSET:
            field_dict["storage_bytes"] = storage_bytes
        if last_invoked_at is not UNSET:
            field_dict["last_invoked_at"] = last_invoked_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        database_id = UUID(d.pop("database_id"))




        project_id = UUID(d.pop("project_id"))




        name = d.pop("name")

        status = check_database_branch_status(d.pop("status"))




        ttl_seconds = d.pop("ttl_seconds")

        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        connection_string = d.pop("connection_string", UNSET)

        storage_bytes = d.pop("storage_bytes", UNSET)

        _last_invoked_at = d.pop("last_invoked_at", UNSET)
        last_invoked_at: datetime.datetime | Unset
        if isinstance(_last_invoked_at,  Unset):
            last_invoked_at = UNSET
        else:
            last_invoked_at = datetime.datetime.fromisoformat(_last_invoked_at)




        database_branch = cls(
            id=id,
            database_id=database_id,
            project_id=project_id,
            name=name,
            status=status,
            ttl_seconds=ttl_seconds,
            expires_at=expires_at,
            created_at=created_at,
            updated_at=updated_at,
            connection_string=connection_string,
            storage_bytes=storage_bytes,
            last_invoked_at=last_invoked_at,
        )


        database_branch.additional_properties = d
        return database_branch

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
