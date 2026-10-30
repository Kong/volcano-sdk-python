from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="DatabaseMigrationFileError")



@_attrs_define
class DatabaseMigrationFileError:
    """ The database's error for a failed file. `message` is the database's own
    message and can quote values from the file or the data.

        Attributes:
            message (str): At most 8 KiB (8,192 bytes). A longer message is cut and ends with
                ` … [truncated]`. Volcano reads each reply the database sends about
                the file up to 4 MiB, which leaves room for a reply that quotes the
                whole file twice. A larger reply is not read: the file fails, and
                this message says so instead.
                 Example: column "email" of relation "users" already exists.
            sqlstate (str | Unset): The Postgres error code, when the database reported one. Example: 42701.
            line (int | Unset): The line of the file the database reported, when known.
     """

    message: str
    sqlstate: str | Unset = UNSET
    line: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        message = self.message

        sqlstate = self.sqlstate

        line = self.line


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "message": message,
        })
        if sqlstate is not UNSET:
            field_dict["sqlstate"] = sqlstate
        if line is not UNSET:
            field_dict["line"] = line

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        sqlstate = d.pop("sqlstate", UNSET)

        line = d.pop("line", UNSET)

        database_migration_file_error = cls(
            message=message,
            sqlstate=sqlstate,
            line=line,
        )


        database_migration_file_error.additional_properties = d
        return database_migration_file_error

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
