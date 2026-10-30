from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="DatabaseMigrationFile")



@_attrs_define
class DatabaseMigrationFile:
    """ One migration file and its SQL.

        Attributes:
            name (str): The file's path under `volcano/migrations/`: a file name such as
                `001_create_users.sql`, or `<database>/001_create_users.sql` in a
                project with more than one database, where `<database>` must be
                this database. Every file in a request takes the same form. Files
                run in byte order of their file name, which the history records.
                 Example: 001_create_users.sql.
            sql (str): The file's SQL, at most 1 MiB. A file may hold several statements
                and runs in one transaction. A file cannot commit, roll back, use
                savepoints, or `COPY` from the client, and statements that cannot
                run in a transaction, such as `CREATE INDEX CONCURRENTLY`, are not
                supported yet; such a file fails with `migration_failed`.
     """

    name: str
    sql: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        sql = self.sql


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "sql": sql,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        sql = d.pop("sql")

        database_migration_file = cls(
            name=name,
            sql=sql,
        )


        database_migration_file.additional_properties = d
        return database_migration_file

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
