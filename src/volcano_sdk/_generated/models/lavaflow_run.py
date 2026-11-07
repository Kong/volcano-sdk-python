from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_run_category import check_lavaflow_run_category
from ..models.lavaflow_run_category import LavaflowRunCategory
from ..models.lavaflow_run_mode import check_lavaflow_run_mode
from ..models.lavaflow_run_mode import LavaflowRunMode
from ..models.lavaflow_run_status import check_lavaflow_run_status
from ..models.lavaflow_run_status import LavaflowRunStatus
from ..models.lavaflow_skip_reason import check_lavaflow_skip_reason
from ..models.lavaflow_skip_reason import LavaflowSkipReason
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.lavaflow_allowed_workflow import LavaflowAllowedWorkflow
  from ..models.lavaflow_diagnosis import LavaflowDiagnosis
  from ..models.lavaflow_failure import LavaflowFailure
  from ..models.lavaflow_fix_outcome import LavaflowFixOutcome
  from ..models.lavaflow_held_workflows import LavaflowHeldWorkflows
  from ..models.lavaflow_involved_resource import LavaflowInvolvedResource
  from ..models.lavaflow_issue_summary import LavaflowIssueSummary
  from ..models.lavaflow_lineage import LavaflowLineage
  from ..models.lavaflow_lineage_evidence import LavaflowLineageEvidence
  from ..models.lavaflow_merge import LavaflowMerge
  from ..models.lavaflow_pull_request import LavaflowPullRequest
  from ..models.lavaflow_repository_checks import LavaflowRepositoryChecks
  from ..models.lavaflow_resource_reference import LavaflowResourceReference
  from ..models.lavaflow_review import LavaflowReview
  from ..models.lavaflow_run_progress import LavaflowRunProgress
  from ..models.lavaflow_source_commit import LavaflowSourceCommit





T = TypeVar("T", bound="LavaflowRun")



@_attrs_define
class LavaflowRun:
    """ 
        Attributes:
            id (UUID):
            project_id (UUID): The project the run belongs to.
            status (LavaflowRunStatus): Where a run is. `diagnosing`, `fixing` and `reviewing` are the stages of a running
                run. `pr_open` means its pull request is open; `completed` means it finished, with no pull request or one that
                was merged or closed.
            resource (LavaflowResourceReference): A function, durable function or frontend in the project, or the project of
                a user-reported problem.
            issue_id (UUID):
            title (None | str): Names the problem the run worked on, in at most 80 characters: its diagnosis' title, else
                the title of the fix it proposed, else the first line or sentence of its diagnosis' summary. Null while none is
                known.
            created_at (datetime.datetime):
            finished_at (datetime.datetime | None):
            pull_request (LavaflowPullRequest | None):
            merge (LavaflowMerge | None):
            mode (LavaflowRunMode): What the run works on: `live` for an issue seen in the project's logs, `code_quality`
                for a Code Quality finding.
            category (LavaflowRunCategory | None): A Code Quality run carries its finding's from the start. Any other run's
                is null until LavaFlow records a diagnosis. Runs from before categories get one when their diagnosis names one
                or their saved fix's paths imply one, and stay null only when neither does.
            resources (list[LavaflowInvolvedResource]): Every resource the run involves: the issue's first, then by name. A
                run without a recorded diagnosis lists only the issue's. For a run whose report came from what it saved rather
                than its source, such as one from before involved resources were recorded, the list may leave out frontends and
                the functions involved through shared code or the build root's dependency files.
            issue (LavaflowIssueSummary | None): Null only for a run that works on no issue.
            progress (LavaflowRunProgress | None): Where a run LavaFlow is still working on stands; null once it has nothing
                left to do.
            pull_request_skipped (LavaflowSkipReason | None): Why a finished run opened no pull request. A `completed` run
                without `pull_request` always has one; it is `diagnose_only` when the project's `autonomy` stopped the run at
                its diagnosis. Null when the run opened a pull request, while it is queued or runs, and when it failed or was
                cancelled.
            lineage (LavaflowLineage | None): The fix lineage the run belongs to. Null for a run in no lineage.
            fix_outcome (LavaflowFixOutcome | None): How the run's merged fix fared once it went live. Null until a merged
                fix goes live with the `lavaflow.lineage` capability on.
            source_commit (LavaflowSourceCommit | None): The commit the run read the code at. Null when it read none, as for
                a run that diagnosed from the logs alone.
            diagnosis (LavaflowDiagnosis | None):
            diff (None | str): The fix LavaFlow saved, as the unified diff its reviewers read, cut short past 256 KiB as
                they read it, with a last line that starts with `[diff truncated`. When a file's content, before or after the
                fix, or any change to it may hold a credential, or the file is too long for LavaFlow to read whole (over 64 KiB,
                or past 256 KiB across the fix's files), every change to that file is left out, with one line in their place
                that starts with `# LavaFlow withheld` and names the file. A run held with `possible_credential` leaves out
                every file. Null for a run with no saved fix, or one saved before LavaFlow kept its diff.
            diff_sha256 (None | str): The SHA-256, in hex, of `diff` exactly as served, its UTF-8 bytes. Null whenever
                `diff` is. Example: 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08.
            diff_truncated (bool): `diff` was cut short, so it does not show the whole fix. False when `diff` is null.
            diff_withheld (list[str]): The files whose changes `diff` leaves out, by path, as its `# LavaFlow withheld`
                lines name them; an empty string for a file whose path may itself hold a credential. Empty when `diff` shows
                every file, or is null.
            review (LavaflowReview | None): The review of the run's fix. When no reviewer could run, it still says why in
                `stopped`. Null when no review ran.
            repository_checks (LavaflowRepositoryChecks | None): Whether LavaFlow ran the repository's own checks on the fix
                itself. Null for a run with no fix.
            failure (LavaflowFailure | None): Why the run stopped or waits, null when nothing went wrong.
            changed_files (list[str]): Repository paths the fix changes, sorted; empty without a fix. A path that may itself
                hold a credential is listed as "", as `diff_withheld` lists it, and so is every path when `diff` can't tell the
                fix's files apart. A file past a truncated `diff`'s cut is listed.
            ungated_workflows (list[LavaflowAllowedWorkflow] | None): The workflow jobs the run's pull request opened past
                because the project's owner allowed ungated workflows, the first one on each branch or commit checked. Empty
                when none or when the run opened no pull request. Null when there is no record of the workflows its pull request
                opened past, as for pull requests opened before LavaFlow recorded them. Under the merge stage, LavaFlow holds
                such a fix as unchecked, with `ungated_workflows`.
            lineage_evidence (LavaflowLineageEvidence | None): What tied the run's issue to a recent LavaFlow fix's deploy.
                Null when nothing did, and for a recurrence, whose issue came back after the fix.
            held_workflows (LavaflowHeldWorkflows | None): For a run whose `pull_request_skipped` is `ungated_workflows`,
                every workflow job that held its fix. Null for any other run, and for a held run whose workflows LavaFlow
                couldn't read to the end, such as one with a workflow it couldn't parse, or more than 256 such jobs.
     """

    id: UUID
    project_id: UUID
    status: LavaflowRunStatus
    resource: LavaflowResourceReference
    issue_id: UUID
    title: None | str
    created_at: datetime.datetime
    finished_at: datetime.datetime | None
    pull_request: LavaflowPullRequest | None
    merge: LavaflowMerge | None
    mode: LavaflowRunMode
    category: LavaflowRunCategory | None
    resources: list[LavaflowInvolvedResource]
    issue: LavaflowIssueSummary | None
    progress: LavaflowRunProgress | None
    pull_request_skipped: LavaflowSkipReason | None
    lineage: LavaflowLineage | None
    fix_outcome: LavaflowFixOutcome | None
    source_commit: LavaflowSourceCommit | None
    diagnosis: LavaflowDiagnosis | None
    diff: None | str
    diff_sha256: None | str
    diff_truncated: bool
    diff_withheld: list[str]
    review: LavaflowReview | None
    repository_checks: LavaflowRepositoryChecks | None
    failure: LavaflowFailure | None
    changed_files: list[str]
    ungated_workflows: list[LavaflowAllowedWorkflow] | None
    lineage_evidence: LavaflowLineageEvidence | None
    held_workflows: LavaflowHeldWorkflows | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_allowed_workflow import LavaflowAllowedWorkflow # noqa: PLC0415
        from ..models.lavaflow_diagnosis import LavaflowDiagnosis # noqa: PLC0415
        from ..models.lavaflow_failure import LavaflowFailure # noqa: PLC0415
        from ..models.lavaflow_fix_outcome import LavaflowFixOutcome # noqa: PLC0415
        from ..models.lavaflow_held_workflows import LavaflowHeldWorkflows # noqa: PLC0415
        from ..models.lavaflow_involved_resource import LavaflowInvolvedResource # noqa: PLC0415
        from ..models.lavaflow_issue_summary import LavaflowIssueSummary # noqa: PLC0415
        from ..models.lavaflow_lineage import LavaflowLineage # noqa: PLC0415
        from ..models.lavaflow_lineage_evidence import LavaflowLineageEvidence # noqa: PLC0415
        from ..models.lavaflow_merge import LavaflowMerge # noqa: PLC0415
        from ..models.lavaflow_pull_request import LavaflowPullRequest # noqa: PLC0415
        from ..models.lavaflow_repository_checks import LavaflowRepositoryChecks # noqa: PLC0415
        from ..models.lavaflow_resource_reference import LavaflowResourceReference # noqa: PLC0415
        from ..models.lavaflow_review import LavaflowReview # noqa: PLC0415
        from ..models.lavaflow_run_progress import LavaflowRunProgress # noqa: PLC0415
        from ..models.lavaflow_source_commit import LavaflowSourceCommit # noqa: PLC0415
        id = str(self.id)

        project_id = str(self.project_id)

        status: str = self.status

        resource = self.resource.to_dict()

        issue_id = str(self.issue_id)

        title: None | str
        title = self.title

        created_at = self.created_at.isoformat()

        finished_at: None | str
        if isinstance(self.finished_at, datetime.datetime):
            finished_at = self.finished_at.isoformat()
        else:
            finished_at = self.finished_at

        pull_request: dict[str, Any] | None
        if isinstance(self.pull_request, LavaflowPullRequest):
            pull_request = self.pull_request.to_dict()
        else:
            pull_request = self.pull_request

        merge: dict[str, Any] | None
        if isinstance(self.merge, LavaflowMerge):
            merge = self.merge.to_dict()
        else:
            merge = self.merge

        mode: str = self.mode

        category: None | str
        if isinstance(self.category, str):
            category = self.category
        else:
            category = self.category

        resources = []
        for resources_item_data in self.resources:
            resources_item = resources_item_data.to_dict()
            resources.append(resources_item)



        issue: dict[str, Any] | None
        if isinstance(self.issue, LavaflowIssueSummary):
            issue = self.issue.to_dict()
        else:
            issue = self.issue

        progress: dict[str, Any] | None
        if isinstance(self.progress, LavaflowRunProgress):
            progress = self.progress.to_dict()
        else:
            progress = self.progress

        pull_request_skipped: None | str
        if isinstance(self.pull_request_skipped, str):
            pull_request_skipped = self.pull_request_skipped
        else:
            pull_request_skipped = self.pull_request_skipped

        lineage: dict[str, Any] | None
        if isinstance(self.lineage, LavaflowLineage):
            lineage = self.lineage.to_dict()
        else:
            lineage = self.lineage

        fix_outcome: dict[str, Any] | None
        if isinstance(self.fix_outcome, LavaflowFixOutcome):
            fix_outcome = self.fix_outcome.to_dict()
        else:
            fix_outcome = self.fix_outcome

        source_commit: dict[str, Any] | None
        if isinstance(self.source_commit, LavaflowSourceCommit):
            source_commit = self.source_commit.to_dict()
        else:
            source_commit = self.source_commit

        diagnosis: dict[str, Any] | None
        if isinstance(self.diagnosis, LavaflowDiagnosis):
            diagnosis = self.diagnosis.to_dict()
        else:
            diagnosis = self.diagnosis

        diff: None | str
        diff = self.diff

        diff_sha256: None | str
        diff_sha256 = self.diff_sha256

        diff_truncated = self.diff_truncated

        diff_withheld = self.diff_withheld



        review: dict[str, Any] | None
        if isinstance(self.review, LavaflowReview):
            review = self.review.to_dict()
        else:
            review = self.review

        repository_checks: dict[str, Any] | None
        if isinstance(self.repository_checks, LavaflowRepositoryChecks):
            repository_checks = self.repository_checks.to_dict()
        else:
            repository_checks = self.repository_checks

        failure: dict[str, Any] | None
        if isinstance(self.failure, LavaflowFailure):
            failure = self.failure.to_dict()
        else:
            failure = self.failure

        changed_files = self.changed_files



        ungated_workflows: list[dict[str, Any]] | None
        if isinstance(self.ungated_workflows, list):
            ungated_workflows = []
            for ungated_workflows_type_0_item_data in self.ungated_workflows:
                ungated_workflows_type_0_item = ungated_workflows_type_0_item_data.to_dict()
                ungated_workflows.append(ungated_workflows_type_0_item)


        else:
            ungated_workflows = self.ungated_workflows

        lineage_evidence: dict[str, Any] | None
        if isinstance(self.lineage_evidence, LavaflowLineageEvidence):
            lineage_evidence = self.lineage_evidence.to_dict()
        else:
            lineage_evidence = self.lineage_evidence

        held_workflows: dict[str, Any] | None
        if isinstance(self.held_workflows, LavaflowHeldWorkflows):
            held_workflows = self.held_workflows.to_dict()
        else:
            held_workflows = self.held_workflows


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "project_id": project_id,
            "status": status,
            "resource": resource,
            "issue_id": issue_id,
            "title": title,
            "created_at": created_at,
            "finished_at": finished_at,
            "pull_request": pull_request,
            "merge": merge,
            "mode": mode,
            "category": category,
            "resources": resources,
            "issue": issue,
            "progress": progress,
            "pull_request_skipped": pull_request_skipped,
            "lineage": lineage,
            "fix_outcome": fix_outcome,
            "source_commit": source_commit,
            "diagnosis": diagnosis,
            "diff": diff,
            "diff_sha256": diff_sha256,
            "diff_truncated": diff_truncated,
            "diff_withheld": diff_withheld,
            "review": review,
            "repository_checks": repository_checks,
            "failure": failure,
            "changed_files": changed_files,
            "ungated_workflows": ungated_workflows,
            "lineage_evidence": lineage_evidence,
            "held_workflows": held_workflows,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_allowed_workflow import LavaflowAllowedWorkflow # noqa: PLC0415
        from ..models.lavaflow_diagnosis import LavaflowDiagnosis # noqa: PLC0415
        from ..models.lavaflow_failure import LavaflowFailure # noqa: PLC0415
        from ..models.lavaflow_fix_outcome import LavaflowFixOutcome # noqa: PLC0415
        from ..models.lavaflow_held_workflows import LavaflowHeldWorkflows # noqa: PLC0415
        from ..models.lavaflow_involved_resource import LavaflowInvolvedResource # noqa: PLC0415
        from ..models.lavaflow_issue_summary import LavaflowIssueSummary # noqa: PLC0415
        from ..models.lavaflow_lineage import LavaflowLineage # noqa: PLC0415
        from ..models.lavaflow_lineage_evidence import LavaflowLineageEvidence # noqa: PLC0415
        from ..models.lavaflow_merge import LavaflowMerge # noqa: PLC0415
        from ..models.lavaflow_pull_request import LavaflowPullRequest # noqa: PLC0415
        from ..models.lavaflow_repository_checks import LavaflowRepositoryChecks # noqa: PLC0415
        from ..models.lavaflow_resource_reference import LavaflowResourceReference # noqa: PLC0415
        from ..models.lavaflow_review import LavaflowReview # noqa: PLC0415
        from ..models.lavaflow_run_progress import LavaflowRunProgress # noqa: PLC0415
        from ..models.lavaflow_source_commit import LavaflowSourceCommit # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        status = check_lavaflow_run_status(d.pop("status"))




        resource = LavaflowResourceReference.from_dict(d.pop("resource"))




        issue_id = UUID(d.pop("issue_id"))




        def _parse_title(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        title = _parse_title(d.pop("title"))


        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        def _parse_finished_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finished_at_type_0 = datetime.datetime.fromisoformat(data)



                return finished_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        finished_at = _parse_finished_at(d.pop("finished_at"))


        def _parse_pull_request(data: object) -> LavaflowPullRequest | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                pull_request_type_1 = LavaflowPullRequest.from_dict(data)



                return pull_request_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowPullRequest | None, data)

        pull_request = _parse_pull_request(d.pop("pull_request"))


        def _parse_merge(data: object) -> LavaflowMerge | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                merge_type_1 = LavaflowMerge.from_dict(data)



                return merge_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowMerge | None, data)

        merge = _parse_merge(d.pop("merge"))


        mode = check_lavaflow_run_mode(d.pop("mode"))




        def _parse_category(data: object) -> LavaflowRunCategory | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                category_type_1 = check_lavaflow_run_category(data)



                return category_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowRunCategory | None, data)

        category = _parse_category(d.pop("category"))


        resources = []
        _resources = d.pop("resources")
        for resources_item_data in (_resources):
            resources_item = LavaflowInvolvedResource.from_dict(resources_item_data)



            resources.append(resources_item)


        def _parse_issue(data: object) -> LavaflowIssueSummary | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                issue_type_1 = LavaflowIssueSummary.from_dict(data)



                return issue_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowIssueSummary | None, data)

        issue = _parse_issue(d.pop("issue"))


        def _parse_progress(data: object) -> LavaflowRunProgress | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                progress_type_1 = LavaflowRunProgress.from_dict(data)



                return progress_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowRunProgress | None, data)

        progress = _parse_progress(d.pop("progress"))


        def _parse_pull_request_skipped(data: object) -> LavaflowSkipReason | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pull_request_skipped_type_1 = check_lavaflow_skip_reason(data)



                return pull_request_skipped_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowSkipReason | None, data)

        pull_request_skipped = _parse_pull_request_skipped(d.pop("pull_request_skipped"))


        def _parse_lineage(data: object) -> LavaflowLineage | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                lineage_type_1 = LavaflowLineage.from_dict(data)



                return lineage_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowLineage | None, data)

        lineage = _parse_lineage(d.pop("lineage"))


        def _parse_fix_outcome(data: object) -> LavaflowFixOutcome | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                fix_outcome_type_1 = LavaflowFixOutcome.from_dict(data)



                return fix_outcome_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowFixOutcome | None, data)

        fix_outcome = _parse_fix_outcome(d.pop("fix_outcome"))


        def _parse_source_commit(data: object) -> LavaflowSourceCommit | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                source_commit_type_1 = LavaflowSourceCommit.from_dict(data)



                return source_commit_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowSourceCommit | None, data)

        source_commit = _parse_source_commit(d.pop("source_commit"))


        def _parse_diagnosis(data: object) -> LavaflowDiagnosis | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                diagnosis_type_1 = LavaflowDiagnosis.from_dict(data)



                return diagnosis_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowDiagnosis | None, data)

        diagnosis = _parse_diagnosis(d.pop("diagnosis"))


        def _parse_diff(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        diff = _parse_diff(d.pop("diff"))


        def _parse_diff_sha256(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        diff_sha256 = _parse_diff_sha256(d.pop("diff_sha256"))


        diff_truncated = d.pop("diff_truncated")

        diff_withheld = cast(list[str], d.pop("diff_withheld"))


        def _parse_review(data: object) -> LavaflowReview | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                review_type_1 = LavaflowReview.from_dict(data)



                return review_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowReview | None, data)

        review = _parse_review(d.pop("review"))


        def _parse_repository_checks(data: object) -> LavaflowRepositoryChecks | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                repository_checks_type_1 = LavaflowRepositoryChecks.from_dict(data)



                return repository_checks_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowRepositoryChecks | None, data)

        repository_checks = _parse_repository_checks(d.pop("repository_checks"))


        def _parse_failure(data: object) -> LavaflowFailure | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                failure_type_1 = LavaflowFailure.from_dict(data)



                return failure_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowFailure | None, data)

        failure = _parse_failure(d.pop("failure"))


        changed_files = cast(list[str], d.pop("changed_files"))


        def _parse_ungated_workflows(data: object) -> list[LavaflowAllowedWorkflow] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                ungated_workflows_type_0 = []
                _ungated_workflows_type_0 = data
                for ungated_workflows_type_0_item_data in (_ungated_workflows_type_0):
                    ungated_workflows_type_0_item = LavaflowAllowedWorkflow.from_dict(ungated_workflows_type_0_item_data)



                    ungated_workflows_type_0.append(ungated_workflows_type_0_item)

                return ungated_workflows_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[LavaflowAllowedWorkflow] | None, data)

        ungated_workflows = _parse_ungated_workflows(d.pop("ungated_workflows"))


        def _parse_lineage_evidence(data: object) -> LavaflowLineageEvidence | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                lineage_evidence_type_1 = LavaflowLineageEvidence.from_dict(data)



                return lineage_evidence_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowLineageEvidence | None, data)

        lineage_evidence = _parse_lineage_evidence(d.pop("lineage_evidence"))


        def _parse_held_workflows(data: object) -> LavaflowHeldWorkflows | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                held_workflows_type_1 = LavaflowHeldWorkflows.from_dict(data)



                return held_workflows_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowHeldWorkflows | None, data)

        held_workflows = _parse_held_workflows(d.pop("held_workflows"))


        lavaflow_run = cls(
            id=id,
            project_id=project_id,
            status=status,
            resource=resource,
            issue_id=issue_id,
            title=title,
            created_at=created_at,
            finished_at=finished_at,
            pull_request=pull_request,
            merge=merge,
            mode=mode,
            category=category,
            resources=resources,
            issue=issue,
            progress=progress,
            pull_request_skipped=pull_request_skipped,
            lineage=lineage,
            fix_outcome=fix_outcome,
            source_commit=source_commit,
            diagnosis=diagnosis,
            diff=diff,
            diff_sha256=diff_sha256,
            diff_truncated=diff_truncated,
            diff_withheld=diff_withheld,
            review=review,
            repository_checks=repository_checks,
            failure=failure,
            changed_files=changed_files,
            ungated_workflows=ungated_workflows,
            lineage_evidence=lineage_evidence,
            held_workflows=held_workflows,
        )


        lavaflow_run.additional_properties = d
        return lavaflow_run

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
