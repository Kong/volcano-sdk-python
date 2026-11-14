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
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.lavaflow_fix_outcome import LavaflowFixOutcome
  from ..models.lavaflow_involved_resource import LavaflowInvolvedResource
  from ..models.lavaflow_issue_summary import LavaflowIssueSummary
  from ..models.lavaflow_lineage import LavaflowLineage
  from ..models.lavaflow_merge import LavaflowMerge
  from ..models.lavaflow_pull_request import LavaflowPullRequest
  from ..models.lavaflow_resource_reference import LavaflowResourceReference
  from ..models.lavaflow_run_progress import LavaflowRunProgress





T = TypeVar("T", bound="LavaflowRunSummary")



@_attrs_define
class LavaflowRunSummary:
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
                the title of the fix it proposed, else the first line or sentence of its diagnosis' summary. A sentence too long
                for a title ends at its last clause that fits, or, with none, is cut at a word and ends with `…`. Null while
                none is known. Reads `Hidden: this field matched a secret.` when it or the text it comes from holds one of the
                project's secret values or a secret gitleaks detects.
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
                fix goes live with the `lavaflow.lineage` capability on. Also null, meaning unknown, when the fix is first found
                live only after its 14-day watch ended and its issue neither resolved as of go-live nor was last seen inside the
                watch.
            fix_summary (str | Unset): The saved proposed fix's title, on one line of at most 80 characters. This describes
                a proposal, not a verified fix, successful review, merge or deployment. It never falls back to the diagnosis.
                Omitted when no saved patch title is known. Reads `Hidden: this field matched a secret.` when the full title or
                the shortened one holds one of the project's secret values or a secret gitleaks detects, and `Hidden: the fix
                may add a credential.` when the fix is held for one. A shortened value ends with `…`.
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
    fix_summary: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_fix_outcome import LavaflowFixOutcome # noqa: PLC0415
        from ..models.lavaflow_involved_resource import LavaflowInvolvedResource # noqa: PLC0415
        from ..models.lavaflow_issue_summary import LavaflowIssueSummary # noqa: PLC0415
        from ..models.lavaflow_lineage import LavaflowLineage # noqa: PLC0415
        from ..models.lavaflow_merge import LavaflowMerge # noqa: PLC0415
        from ..models.lavaflow_pull_request import LavaflowPullRequest # noqa: PLC0415
        from ..models.lavaflow_resource_reference import LavaflowResourceReference # noqa: PLC0415
        from ..models.lavaflow_run_progress import LavaflowRunProgress # noqa: PLC0415
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

        fix_summary = self.fix_summary


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
        })
        if fix_summary is not UNSET:
            field_dict["fix_summary"] = fix_summary

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_fix_outcome import LavaflowFixOutcome # noqa: PLC0415
        from ..models.lavaflow_involved_resource import LavaflowInvolvedResource # noqa: PLC0415
        from ..models.lavaflow_issue_summary import LavaflowIssueSummary # noqa: PLC0415
        from ..models.lavaflow_lineage import LavaflowLineage # noqa: PLC0415
        from ..models.lavaflow_merge import LavaflowMerge # noqa: PLC0415
        from ..models.lavaflow_pull_request import LavaflowPullRequest # noqa: PLC0415
        from ..models.lavaflow_resource_reference import LavaflowResourceReference # noqa: PLC0415
        from ..models.lavaflow_run_progress import LavaflowRunProgress # noqa: PLC0415
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


        fix_summary = d.pop("fix_summary", UNSET)

        lavaflow_run_summary = cls(
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
            fix_summary=fix_summary,
        )


        lavaflow_run_summary.additional_properties = d
        return lavaflow_run_summary

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
