from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.database_migration_run_file_outcome import check_database_migration_run_file_outcome
from ..models.database_migration_run_file_outcome import DatabaseMigrationRunFileOutcome
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.database_migration_file_error import DatabaseMigrationFileError





T = TypeVar("T", bound="DatabaseMigrationRunFile")



@_attrs_define
class DatabaseMigrationRunFile:
    """ 
        Attributes:
            name (str):  Example: 001_create_users.sql.
            outcome (DatabaseMigrationRunFileOutcome): `pending`: not settled yet, including a file the run will try again
                on its next attempt. `already_applied`: the history already recorded
                it, so it did not run; a file can also end this way in `apply`, when
                another session applied or baselined it after the run planned.
                `applied`: this run applied it. `failed`: its own SQL failed and
                its transaction rolled back, in the rehearsal or in the database as
                the run's `phase` says, including when the run's time limit stopped
                it; a file whose `COMMIT` failed is `unknown` instead. `not_run`:
                the run ended before the file committed, without its SQL failing:
                before `apply`, after an earlier file failed or lost its `COMMIT`,
                or after the connection was lost or Volcano's own statements around
                the file failed, which rolled it back. `unknown`: the run ended
                in `apply` without confirming whether the file ran, for example
                because its attempts ran out or its `COMMIT` failed or was cut
                short. The file may have committed; the database's history says,
                and the next run's plan applies it only if it is not recorded.
                While the run is `queued` or `running`, each attempt reads the
                history again before it runs a file, and sets every file the run
                has not applied from it: `already_applied` if the history holds
                it, `pending` otherwise.
            error (DatabaseMigrationFileError | Unset): The database's error for a failed file. `message` is the database's
                own
                message and can quote values from the file or the data.
     """

    name: str
    outcome: DatabaseMigrationRunFileOutcome
    error: DatabaseMigrationFileError | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.database_migration_file_error import DatabaseMigrationFileError # noqa: PLC0415
        name = self.name

        outcome: str = self.outcome

        error: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "outcome": outcome,
        })
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.database_migration_file_error import DatabaseMigrationFileError # noqa: PLC0415
        d = dict(src_dict)
        name = d.pop("name")

        outcome = check_database_migration_run_file_outcome(d.pop("outcome"))




        _error = d.pop("error", UNSET)
        error: DatabaseMigrationFileError | Unset
        if isinstance(_error,  Unset):
            error = UNSET
        else:
            error = DatabaseMigrationFileError.from_dict(_error)




        database_migration_run_file = cls(
            name=name,
            outcome=outcome,
            error=error,
        )


        database_migration_run_file.additional_properties = d
        return database_migration_run_file

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
