from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.database_migration_history_entry_status import check_database_migration_history_entry_status
from ..models.database_migration_history_entry_status import DatabaseMigrationHistoryEntryStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="DatabaseMigrationHistoryEntry")



@_attrs_define
class DatabaseMigrationHistoryEntry:
    """ One file the database's migration history records.

        Attributes:
            name (str):  Example: 001_create_users.sql.
            checksum (str): `sha256:` and the hex digest of the file as recorded, with a leading
                byte order mark removed and CRLF line endings converted to LF.
                 Example: sha256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08.
            status (DatabaseMigrationHistoryEntryStatus): `applied`: a run ran the file and it committed. `baselined`: the
                file
                was recorded as applied without running.
            applied_at (datetime.datetime):
            run_id (UUID | Unset): The run that recorded the file. Absent for a baseline.
     """

    name: str
    checksum: str
    status: DatabaseMigrationHistoryEntryStatus
    applied_at: datetime.datetime
    run_id: UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        checksum = self.checksum

        status: str = self.status

        applied_at = self.applied_at.isoformat()

        run_id: str | Unset = UNSET
        if not isinstance(self.run_id, Unset):
            run_id = str(self.run_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "checksum": checksum,
            "status": status,
            "applied_at": applied_at,
        })
        if run_id is not UNSET:
            field_dict["run_id"] = run_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        checksum = d.pop("checksum")

        status = check_database_migration_history_entry_status(d.pop("status"))




        applied_at = datetime.datetime.fromisoformat(d.pop("applied_at"))




        _run_id = d.pop("run_id", UNSET)
        run_id: UUID | Unset
        if isinstance(_run_id,  Unset):
            run_id = UNSET
        else:
            run_id = UUID(_run_id)




        database_migration_history_entry = cls(
            name=name,
            checksum=checksum,
            status=status,
            applied_at=applied_at,
            run_id=run_id,
        )


        database_migration_history_entry.additional_properties = d
        return database_migration_history_entry

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
