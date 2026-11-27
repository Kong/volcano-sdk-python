from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.database_migration_warning_code import check_database_migration_warning_code
from ..models.database_migration_warning_code import DatabaseMigrationWarningCode
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="DatabaseMigrationWarning")



@_attrs_define
class DatabaseMigrationWarning:
    """ A condition the run reports that did not stop it.

        Attributes:
            code (DatabaseMigrationWarningCode): `out_of_order`: a pending file sorts before one the history already
                records; it still ran. `missing_file`: the history records a file
                the run did not include. `rehearsal_skipped`: the files were not
                rehearsed, because branches are not available here or on the plan.
                `backup_skipped`: no backup was taken, because backups are not
                available here or on the plan. `backup_prune_failed`: Volcano
                could not delete older migration backups beyond the 20 it keeps;
                the run's outcome is unaffected, and the next run that takes a
                backup tries again. `warnings_truncated`: the run raised more than
                100 warnings; it is the last one, and its message says how many
                more were not kept.
            message (str):
            file (str | Unset): The file the warning is about, when it is about one.
     """

    code: DatabaseMigrationWarningCode
    message: str
    file: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        code: str = self.code

        message = self.message

        file = self.file


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "code": code,
            "message": message,
        })
        if file is not UNSET:
            field_dict["file"] = file

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = check_database_migration_warning_code(d.pop("code"))




        message = d.pop("message")

        file = d.pop("file", UNSET)

        database_migration_warning = cls(
            code=code,
            message=message,
            file=file,
        )


        database_migration_warning.additional_properties = d
        return database_migration_warning

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
