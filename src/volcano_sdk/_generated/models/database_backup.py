from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.database_backup_source import check_database_backup_source
from ..models.database_backup_source import DatabaseBackupSource
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="DatabaseBackup")



@_attrs_define
class DatabaseBackup:
    """ A point-in-time copy of a database, kept by the storage provider and
    restorable in place.

    Backups cover the database itself, not its branches. Restoring one
    replaces the database's data and keeps its connection string.

        Attributes:
            name (str): Backup name, unique within the database. Backups you create are
                named by you; scheduled backups are named by the storage provider.
            source (DatabaseBackupSource): Whether the backup was requested explicitly or produced by the
                backup schedule. Only `manual` backups count against the plan's
                backup allowance.
            created_at (datetime.datetime): The point in time the backup captures.
            size_bytes (int | Unset): Storage the backup occupies. Absent until the provider has costed
                it, which takes a few minutes after the backup is taken; absent is
                not the same as empty.
            expires_at (datetime.datetime | Unset): When the backup is deleted automatically, from the plan's retention.
                Absent means it is kept until deleted explicitly.
     """

    name: str
    source: DatabaseBackupSource
    created_at: datetime.datetime
    size_bytes: int | Unset = UNSET
    expires_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        source: str = self.source

        created_at = self.created_at.isoformat()

        size_bytes = self.size_bytes

        expires_at: str | Unset = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "source": source,
            "created_at": created_at,
        })
        if size_bytes is not UNSET:
            field_dict["size_bytes"] = size_bytes
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        source = check_database_backup_source(d.pop("source"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        size_bytes = d.pop("size_bytes", UNSET)

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: datetime.datetime | Unset
        if isinstance(_expires_at,  Unset):
            expires_at = UNSET
        else:
            expires_at = datetime.datetime.fromisoformat(_expires_at)




        database_backup = cls(
            name=name,
            source=source,
            created_at=created_at,
            size_bytes=size_bytes,
            expires_at=expires_at,
        )


        database_backup.additional_properties = d
        return database_backup

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
