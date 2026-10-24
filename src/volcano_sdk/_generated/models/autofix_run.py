from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.autofix_pull_request_skipped import AutofixPullRequestSkipped
from ..models.autofix_pull_request_skipped import check_autofix_pull_request_skipped
from ..models.autofix_run_status import AutofixRunStatus
from ..models.autofix_run_status import check_autofix_run_status
from ..models.autofix_run_trigger import AutofixRunTrigger
from ..models.autofix_run_trigger import check_autofix_run_trigger
from ..models.autofix_stage import AutofixStage
from ..models.autofix_stage import check_autofix_stage
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.autofix_diagnosis import AutofixDiagnosis
  from ..models.autofix_patch import AutofixPatch
  from ..models.autofix_pull_request import AutofixPullRequest





T = TypeVar("T", bound="AutofixRun")



@_attrs_define
class AutofixRun:
    """ 
        Attributes:
            id (UUID):
            project_id (UUID):
            issue_id (UUID):
            trigger (AutofixRunTrigger): What started the run. `manual` is a request; `new_issue` and `regression` are
                automatic runs for an issue that appeared or reopened.
            status (AutofixRunStatus): Where a run is. `canceled` means the project's settings or plan stopped allowing the
                run before it finished; `failure_code` says which.
            max_stage (AutofixStage): How far a run may go. `diagnose` stops at a root-cause diagnosis. `pull_request` may
                also open a draft pull request with a fix in the project's connected repository.
            created_at (datetime.datetime):
            stage_reached (AutofixStage | Unset): How far a run may go. `diagnose` stops at a root-cause diagnosis.
                `pull_request` may also open a draft pull request with a fix in the project's connected repository.
            diagnosis (AutofixDiagnosis | Unset):
            patch (AutofixPatch | Unset): The fix the model proposed, applied to the deployed commit. Present whenever the
                run opened a pull request, and when a valid fix could not be published.
            pull_request (AutofixPullRequest | Unset): The draft pull request the run opened on the connected repository.
            pull_request_skipped (AutofixPullRequestSkipped | Unset): Why a run whose `max_stage` is `pull_request` opened
                no pull request. The diagnosis stands either way.
            commit_sha (str | Unset): The commit the diagnosis read, when a push to the connected repository deployed the
                resource. Absent when the run read logs only.
            failure_code (str | Unset): Why the run failed or was canceled, or why its last attempt will be retried. A
                queued run paused while Autofix is unavailable reports `feature_unavailable`; it resumes without spending an
                attempt when Autofix returns. Other values are `model_request_rejected`, `model_unavailable`, `model_refused`,
                `no_diagnosis`, `budget_exhausted`, `timed_out`, `attempts_exhausted`, `autofix_disabled`, `plan_required`,
                `issue_not_found`, or `internal_error`. Runs that ended before Volcano picked the models for every run may also
                report `api_key_rejected`, `settings_changed`, or `managed_models_unavailable`; no new run reports them.
            failure_message (str | Unset):
            started_at (datetime.datetime | Unset):
            completed_at (datetime.datetime | Unset):
     """

    id: UUID
    project_id: UUID
    issue_id: UUID
    trigger: AutofixRunTrigger
    status: AutofixRunStatus
    max_stage: AutofixStage
    created_at: datetime.datetime
    stage_reached: AutofixStage | Unset = UNSET
    diagnosis: AutofixDiagnosis | Unset = UNSET
    patch: AutofixPatch | Unset = UNSET
    pull_request: AutofixPullRequest | Unset = UNSET
    pull_request_skipped: AutofixPullRequestSkipped | Unset = UNSET
    commit_sha: str | Unset = UNSET
    failure_code: str | Unset = UNSET
    failure_message: str | Unset = UNSET
    started_at: datetime.datetime | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.autofix_diagnosis import AutofixDiagnosis # noqa: PLC0415
        from ..models.autofix_patch import AutofixPatch # noqa: PLC0415
        from ..models.autofix_pull_request import AutofixPullRequest # noqa: PLC0415
        id = str(self.id)

        project_id = str(self.project_id)

        issue_id = str(self.issue_id)

        trigger: str = self.trigger

        status: str = self.status

        max_stage: str = self.max_stage

        created_at = self.created_at.isoformat()

        stage_reached: str | Unset = UNSET
        if not isinstance(self.stage_reached, Unset):
            stage_reached = self.stage_reached


        diagnosis: dict[str, Any] | Unset = UNSET
        if not isinstance(self.diagnosis, Unset):
            diagnosis = self.diagnosis.to_dict()

        patch: dict[str, Any] | Unset = UNSET
        if not isinstance(self.patch, Unset):
            patch = self.patch.to_dict()

        pull_request: dict[str, Any] | Unset = UNSET
        if not isinstance(self.pull_request, Unset):
            pull_request = self.pull_request.to_dict()

        pull_request_skipped: str | Unset = UNSET
        if not isinstance(self.pull_request_skipped, Unset):
            pull_request_skipped = self.pull_request_skipped


        commit_sha = self.commit_sha

        failure_code = self.failure_code

        failure_message = self.failure_message

        started_at: str | Unset = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "project_id": project_id,
            "issue_id": issue_id,
            "trigger": trigger,
            "status": status,
            "max_stage": max_stage,
            "created_at": created_at,
        })
        if stage_reached is not UNSET:
            field_dict["stage_reached"] = stage_reached
        if diagnosis is not UNSET:
            field_dict["diagnosis"] = diagnosis
        if patch is not UNSET:
            field_dict["patch"] = patch
        if pull_request is not UNSET:
            field_dict["pull_request"] = pull_request
        if pull_request_skipped is not UNSET:
            field_dict["pull_request_skipped"] = pull_request_skipped
        if commit_sha is not UNSET:
            field_dict["commit_sha"] = commit_sha
        if failure_code is not UNSET:
            field_dict["failure_code"] = failure_code
        if failure_message is not UNSET:
            field_dict["failure_message"] = failure_message
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.autofix_diagnosis import AutofixDiagnosis # noqa: PLC0415
        from ..models.autofix_patch import AutofixPatch # noqa: PLC0415
        from ..models.autofix_pull_request import AutofixPullRequest # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        issue_id = UUID(d.pop("issue_id"))




        trigger = check_autofix_run_trigger(d.pop("trigger"))




        status = check_autofix_run_status(d.pop("status"))




        max_stage = check_autofix_stage(d.pop("max_stage"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        _stage_reached = d.pop("stage_reached", UNSET)
        stage_reached: AutofixStage | Unset
        if isinstance(_stage_reached,  Unset):
            stage_reached = UNSET
        else:
            stage_reached = check_autofix_stage(_stage_reached)




        _diagnosis = d.pop("diagnosis", UNSET)
        diagnosis: AutofixDiagnosis | Unset
        if isinstance(_diagnosis,  Unset):
            diagnosis = UNSET
        else:
            diagnosis = AutofixDiagnosis.from_dict(_diagnosis)




        _patch = d.pop("patch", UNSET)
        patch: AutofixPatch | Unset
        if isinstance(_patch,  Unset):
            patch = UNSET
        else:
            patch = AutofixPatch.from_dict(_patch)




        _pull_request = d.pop("pull_request", UNSET)
        pull_request: AutofixPullRequest | Unset
        if isinstance(_pull_request,  Unset):
            pull_request = UNSET
        else:
            pull_request = AutofixPullRequest.from_dict(_pull_request)




        _pull_request_skipped = d.pop("pull_request_skipped", UNSET)
        pull_request_skipped: AutofixPullRequestSkipped | Unset
        if isinstance(_pull_request_skipped,  Unset):
            pull_request_skipped = UNSET
        else:
            pull_request_skipped = check_autofix_pull_request_skipped(_pull_request_skipped)




        commit_sha = d.pop("commit_sha", UNSET)

        failure_code = d.pop("failure_code", UNSET)

        failure_message = d.pop("failure_message", UNSET)

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




        autofix_run = cls(
            id=id,
            project_id=project_id,
            issue_id=issue_id,
            trigger=trigger,
            status=status,
            max_stage=max_stage,
            created_at=created_at,
            stage_reached=stage_reached,
            diagnosis=diagnosis,
            patch=patch,
            pull_request=pull_request,
            pull_request_skipped=pull_request_skipped,
            commit_sha=commit_sha,
            failure_code=failure_code,
            failure_message=failure_message,
            started_at=started_at,
            completed_at=completed_at,
        )

        return autofix_run

