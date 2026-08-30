from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.database_restore_kind import check_database_restore_kind
from ..models.database_restore_kind import DatabaseRestoreKind
from ..models.database_restore_status import check_database_restore_status
from ..models.database_restore_status import DatabaseRestoreStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="DatabaseRestore")



@_attrs_define
class DatabaseRestore:
    """ A restore of a database, either from a named backup or to a point in
    time. Restores run in the background and take longer than a request, so
    the database is unavailable until this reports `completed`.

        Attributes:
            id (UUID):
            database_id (UUID):
            project_id (UUID):
            kind (DatabaseRestoreKind): Whether the restore targets a named backup or an arbitrary point in
                time. Both replace the database's data in place.
            status (DatabaseRestoreStatus): Restore status. `pending` and `running` both mean the restore is
                still in flight and the database is not connectable; an attempt that
                fails with tries left goes back to `pending`. `failed` and
                `exhausted` both mean Volcano gave up: the database is left `failed`
                if its data may already have been replaced, and `active` if the
                restore never started — a backup that no longer exists at the
                provider ends the restore without touching the database. A restore
                cannot be cancelled once it starts.
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            backup_name (str | Unset): The backup restored, kept even if that backup is later deleted.
                Absent for a point-in-time restore.
            restore_to (datetime.datetime | Unset): The point in time restored to. Absent for a backup restore.
            error (str | Unset): Why the most recent attempt failed, when one has.
            completed_at (datetime.datetime | Unset):
     """

    id: UUID
    database_id: UUID
    project_id: UUID
    kind: DatabaseRestoreKind
    status: DatabaseRestoreStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    backup_name: str | Unset = UNSET
    restore_to: datetime.datetime | Unset = UNSET
    error: str | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        database_id = str(self.database_id)

        project_id = str(self.project_id)

        kind: str = self.kind

        status: str = self.status

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        backup_name = self.backup_name

        restore_to: str | Unset = UNSET
        if not isinstance(self.restore_to, Unset):
            restore_to = self.restore_to.isoformat()

        error = self.error

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "database_id": database_id,
            "project_id": project_id,
            "kind": kind,
            "status": status,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if backup_name is not UNSET:
            field_dict["backup_name"] = backup_name
        if restore_to is not UNSET:
            field_dict["restore_to"] = restore_to
        if error is not UNSET:
            field_dict["error"] = error
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        database_id = UUID(d.pop("database_id"))




        project_id = UUID(d.pop("project_id"))




        kind = check_database_restore_kind(d.pop("kind"))




        status = check_database_restore_status(d.pop("status"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        backup_name = d.pop("backup_name", UNSET)

        _restore_to = d.pop("restore_to", UNSET)
        restore_to: datetime.datetime | Unset
        if isinstance(_restore_to,  Unset):
            restore_to = UNSET
        else:
            restore_to = datetime.datetime.fromisoformat(_restore_to)




        error = d.pop("error", UNSET)

        _completed_at = d.pop("completed_at", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at,  Unset):
            completed_at = UNSET
        else:
            completed_at = datetime.datetime.fromisoformat(_completed_at)




        database_restore = cls(
            id=id,
            database_id=database_id,
            project_id=project_id,
            kind=kind,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            backup_name=backup_name,
            restore_to=restore_to,
            error=error,
            completed_at=completed_at,
        )


        database_restore.additional_properties = d
        return database_restore

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
