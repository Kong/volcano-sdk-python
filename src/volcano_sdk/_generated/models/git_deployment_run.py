from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.git_deployment_run_status import check_git_deployment_run_status
from ..models.git_deployment_run_status import GitDeploymentRunStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.git_deployment_migration_run import GitDeploymentMigrationRun
  from ..models.git_deployment_run_error import GitDeploymentRunError





T = TypeVar("T", bound="GitDeploymentRun")



@_attrs_define
class GitDeploymentRun:
    """ One push's deployment through Git auto deploy.

        Attributes:
            id (UUID):
            status (GitDeploymentRunStatus): Where a run is. `pending` and `running` have not ended. `succeeded`: every
                deployment the run dispatched succeeded, or the commit only had migrations to apply. `failed`: `error` says why.
                `superseded`: a newer push replaced the run before it started. `skipped`: there was nothing to deploy; `error`
                says why.
            branch (str): The branch the push updated, the project's production branch at the time.
            commit_sha (str): The commit the run deploys.
            apply_migrations (bool): Whether the run applies the commit's migrations: the project's `apply_migrations` Git
                deploy setting when the push arrived.
            migration_runs (list[GitDeploymentMigrationRun]): The migration runs the run started, one per database, ordered
                by database name. Empty when it started none.
            created_at (datetime.datetime): When the push was recorded.
            error (GitDeploymentRunError | Unset): Why a run failed or was skipped.
            started_at (datetime.datetime | Unset): When a worker first picked the run up.
            completed_at (datetime.datetime | Unset): When the run ended.
     """

    id: UUID
    status: GitDeploymentRunStatus
    branch: str
    commit_sha: str
    apply_migrations: bool
    migration_runs: list[GitDeploymentMigrationRun]
    created_at: datetime.datetime
    error: GitDeploymentRunError | Unset = UNSET
    started_at: datetime.datetime | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.git_deployment_migration_run import GitDeploymentMigrationRun # noqa: PLC0415
        from ..models.git_deployment_run_error import GitDeploymentRunError # noqa: PLC0415
        id = str(self.id)

        status: str = self.status

        branch = self.branch

        commit_sha = self.commit_sha

        apply_migrations = self.apply_migrations

        migration_runs = []
        for migration_runs_item_data in self.migration_runs:
            migration_runs_item = migration_runs_item_data.to_dict()
            migration_runs.append(migration_runs_item)



        created_at = self.created_at.isoformat()

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
            "status": status,
            "branch": branch,
            "commit_sha": commit_sha,
            "apply_migrations": apply_migrations,
            "migration_runs": migration_runs,
            "created_at": created_at,
        })
        if error is not UNSET:
            field_dict["error"] = error
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.git_deployment_migration_run import GitDeploymentMigrationRun # noqa: PLC0415
        from ..models.git_deployment_run_error import GitDeploymentRunError # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        status = check_git_deployment_run_status(d.pop("status"))




        branch = d.pop("branch")

        commit_sha = d.pop("commit_sha")

        apply_migrations = d.pop("apply_migrations")

        migration_runs = []
        _migration_runs = d.pop("migration_runs")
        for migration_runs_item_data in (_migration_runs):
            migration_runs_item = GitDeploymentMigrationRun.from_dict(migration_runs_item_data)



            migration_runs.append(migration_runs_item)


        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        _error = d.pop("error", UNSET)
        error: GitDeploymentRunError | Unset
        if isinstance(_error,  Unset):
            error = UNSET
        else:
            error = GitDeploymentRunError.from_dict(_error)




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




        git_deployment_run = cls(
            id=id,
            status=status,
            branch=branch,
            commit_sha=commit_sha,
            apply_migrations=apply_migrations,
            migration_runs=migration_runs,
            created_at=created_at,
            error=error,
            started_at=started_at,
            completed_at=completed_at,
        )


        git_deployment_run.additional_properties = d
        return git_deployment_run

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
