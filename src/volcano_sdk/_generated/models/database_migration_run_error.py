from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.database_migration_run_error_code import check_database_migration_run_error_code
from ..models.database_migration_run_error_code import DatabaseMigrationRunErrorCode
from typing import cast






T = TypeVar("T", bound="DatabaseMigrationRunError")



@_attrs_define
class DatabaseMigrationRunError:
    """ Why the run failed, or why its last attempt did.

        Attributes:
            code (DatabaseMigrationRunErrorCode): Stable machine-readable reason. `migration_failed`: a file's SQL,
                or its `COMMIT`, failed; `phase` says whether in the rehearsal,
                leaving the database untouched, or in the database, where the files
                before it stay applied. `checksum_mismatch`: an applied file changed.
                `history_missing`: the database's history table is gone though
                migrations ran there; record a baseline of the files already
                applied. Dropping the whole `_volcano_migrations` schema is not
                supported and not detected: the database reads as new, and the run
                applies every file again. `history_too_large`: the history has
                more than the 1,000 entries Volcano reads. `invalid_file`: a file
                Volcano refuses to run. `invalid_layout`: file paths that do not map
                to the database.
                `plan_changed`: the history changed after the rehearsal.
                `branch_limit`: the rehearsal branch would exceed the plan's branch
                allowance. `backup_failed` and `rehearsal_unavailable`: Volcano
                could not take the backup or prepare the rehearsal.
                `restore_in_progress` and `database_unavailable`: the database could
                not take the run. `owner_not_active`: the project owner's account
                was not `active` when Volcano picked the run up, or before its
                `backup` or `apply`, so the run applied nothing further; files it
                already applied stay applied.
                `locked`: another session held the migration lock,
                or a file waited too long for a lock. `connection_failed`: the
                database could not be reached, or the connection was lost,
                including while a file ran. `internal_error`: Volcano failed for a
                reason of its own, such as its own statements around a file.
                `timeout` and `attempts_exhausted`: the run could not finish.
                `operator_failed`: Volcano ended a run that stopped making
                progress; read the history to see which files were applied, then
                start a new run.
            message (str): What happened, naming files and Postgres error codes. The
                database's own message is on the failed file.
     """

    code: DatabaseMigrationRunErrorCode
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        code: str = self.code

        message = self.message


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "code": code,
            "message": message,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = check_database_migration_run_error_code(d.pop("code"))




        message = d.pop("message")

        database_migration_run_error = cls(
            code=code,
            message=message,
        )


        database_migration_run_error.additional_properties = d
        return database_migration_run_error

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
