from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.database_migration_run_phase import check_database_migration_run_phase
from ..models.database_migration_run_phase import DatabaseMigrationRunPhase
from ..models.database_migration_run_source import check_database_migration_run_source
from ..models.database_migration_run_source import DatabaseMigrationRunSource
from ..models.database_migration_run_status import check_database_migration_run_status
from ..models.database_migration_run_status import DatabaseMigrationRunStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.database_migration_run_error import DatabaseMigrationRunError
  from ..models.database_migration_run_file import DatabaseMigrationRunFile
  from ..models.database_migration_warning import DatabaseMigrationWarning
  from ..models.resource_reference import ResourceReference





T = TypeVar("T", bound="DatabaseMigrationRun")



@_attrs_define
class DatabaseMigrationRun:
    """ One application of migration files to a database. A run plans the files
    against the database's history, rehearses the pending ones on a
    short-lived branch, takes a backup, and applies them.

        Attributes:
            id (UUID):
            database (ResourceReference): Stable reference to a Volcano resource.
            status (DatabaseMigrationRunStatus): `queued` and `running` mean the run has not ended; a run waiting
                to retry stays `running`. `succeeded`: every pending file was
                applied, or none was pending. `failed`: `error` says why.
            phase (DatabaseMigrationRunPhase): The step the run is on, or the one it ended on. `plan` compares the
                files with the history. `rehearse` applies the pending files to a
                short-lived branch of the database, which is deleted afterwards.
                `backup` takes the backup named by `backup_name`. `apply` applies
                the files to the database.
            source (DatabaseMigrationRunSource): What started the run.
            warnings (list[DatabaseMigrationWarning]): A run keeps at most 100 warnings, keeping those about the run, such
                as a skipped backup, ahead of those about files. A run that raised
                more ends the list with a `warnings_truncated` warning.
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            commit_sha (str | Unset): The commit whose files the run applies. Present for `git_deploy` runs.
            backup_name (str | Unset): The backup the run takes before it applies the files, named once
                the run starts taking it. It is listed with the database's backups
                with `source: migration`. A run that ended in its `backup` phase
                may name a backup that was never created.
                 Example: before-migration-7f3a1c2e-5d4b-4a91-8c6f-2b1e9d0a4c73.
            files (list[DatabaseMigrationRunFile] | Unset): The run's files, in the order they run, with what became of
                each.
                Absent when listing runs.
            error (DatabaseMigrationRunError | Unset): Why the run failed, or why its last attempt did.
            started_at (datetime.datetime | Unset): When a worker first picked the run up.
            completed_at (datetime.datetime | Unset):
     """

    id: UUID
    database: ResourceReference
    status: DatabaseMigrationRunStatus
    phase: DatabaseMigrationRunPhase
    source: DatabaseMigrationRunSource
    warnings: list[DatabaseMigrationWarning]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    commit_sha: str | Unset = UNSET
    backup_name: str | Unset = UNSET
    files: list[DatabaseMigrationRunFile] | Unset = UNSET
    error: DatabaseMigrationRunError | Unset = UNSET
    started_at: datetime.datetime | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.database_migration_run_error import DatabaseMigrationRunError # noqa: PLC0415
        from ..models.database_migration_run_file import DatabaseMigrationRunFile # noqa: PLC0415
        from ..models.database_migration_warning import DatabaseMigrationWarning # noqa: PLC0415
        from ..models.resource_reference import ResourceReference # noqa: PLC0415
        id = str(self.id)

        database = self.database.to_dict()

        status: str = self.status

        phase: str = self.phase

        source: str = self.source

        warnings = []
        for warnings_item_data in self.warnings:
            warnings_item = warnings_item_data.to_dict()
            warnings.append(warnings_item)



        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        commit_sha = self.commit_sha

        backup_name = self.backup_name

        files: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)



        error: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        started_at: str | Unset = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "database": database,
            "status": status,
            "phase": phase,
            "source": source,
            "warnings": warnings,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if commit_sha is not UNSET:
            field_dict["commit_sha"] = commit_sha
        if backup_name is not UNSET:
            field_dict["backup_name"] = backup_name
        if files is not UNSET:
            field_dict["files"] = files
        if error is not UNSET:
            field_dict["error"] = error
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.database_migration_run_error import DatabaseMigrationRunError # noqa: PLC0415
        from ..models.database_migration_run_file import DatabaseMigrationRunFile # noqa: PLC0415
        from ..models.database_migration_warning import DatabaseMigrationWarning # noqa: PLC0415
        from ..models.resource_reference import ResourceReference # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        database = ResourceReference.from_dict(d.pop("database"))




        status = check_database_migration_run_status(d.pop("status"))




        phase = check_database_migration_run_phase(d.pop("phase"))




        source = check_database_migration_run_source(d.pop("source"))




        warnings = []
        _warnings = d.pop("warnings")
        for warnings_item_data in (_warnings):
            warnings_item = DatabaseMigrationWarning.from_dict(warnings_item_data)



            warnings.append(warnings_item)


        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        commit_sha = d.pop("commit_sha", UNSET)

        backup_name = d.pop("backup_name", UNSET)

        _files = d.pop("files", UNSET)
        files: list[DatabaseMigrationRunFile] | Unset = UNSET
        if _files is not UNSET:
            files = []
            for files_item_data in _files:
                files_item = DatabaseMigrationRunFile.from_dict(files_item_data)



                files.append(files_item)


        _error = d.pop("error", UNSET)
        error: DatabaseMigrationRunError | Unset
        if isinstance(_error,  Unset):
            error = UNSET
        else:
            error = DatabaseMigrationRunError.from_dict(_error)




        _started_at = d.pop("started_at", UNSET)
        started_at: datetime.datetime | Unset
        if isinstance(_started_at,  Unset):
            started_at = UNSET
        else:
            started_at = datetime.datetime.fromisoformat(_started_at)




        _completed_at = d.pop("completed_at", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at,  Unset):
            completed_at = UNSET
        else:
            completed_at = datetime.datetime.fromisoformat(_completed_at)




        database_migration_run = cls(
            id=id,
            database=database,
            status=status,
            phase=phase,
            source=source,
            warnings=warnings,
            created_at=created_at,
            updated_at=updated_at,
            commit_sha=commit_sha,
            backup_name=backup_name,
            files=files,
            error=error,
            started_at=started_at,
            completed_at=completed_at,
        )


        database_migration_run.additional_properties = d
        return database_migration_run

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
