from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_skip_reason import check_lavaflow_skip_reason
from ..models.lavaflow_skip_reason import LavaflowSkipReason
from typing import cast
import datetime






T = TypeVar("T", bound="LavaflowDeliverySkip")



@_attrs_define
class LavaflowDeliverySkip:
    """ 
        Attributes:
            reason (LavaflowSkipReason): Why a finished run opened no pull request, with what you can do next.
                `diagnose_only`: the project's `autonomy` was `diagnose_only` when the run was queued, or became it before the
                pull request opened, so LavaFlow only diagnosed the issue; read the diagnosis. For later runs to open pull
                requests, send `"autonomy": "open_pr"` to `PATCH /lavaflow/settings`, or run `volcano cloud lavaflow settings
                set --autonomy open_pr`. `not_fixable`: the diagnosis found no change in the code that fixes the error, for
                example because the cause is outside it; read the diagnosis. `low_confidence`: the diagnosis is not confident
                enough to propose a fix; read the diagnosis. `no_patch`: LavaFlow proposed no change; read the diagnosis.
                `possible_credential`: the fix held what looks like a credential or a project secret, so LavaFlow pushed
                nothing; apply the fix yourself from the diagnosis. `possible_personal_data`: the fix adds an email address the
                repository lacks, and the repository isn't private, so LavaFlow pushed nothing; apply the fix yourself.
                `ungated_workflows`: on the earlier publication path or under automatic merging, a workflow could run the fix
                with the repository's secrets before a person approves it; gate the workflow on a label a person adds, or turn
                on `allow_ungated_workflows`. `convention_unsatisfiable`: LavaFlow would merge the fix, but no title can meet
                the repository's commit convention, so it kept the fix on the run; apply the fix yourself, or relax the
                convention. `pull_request_open`: when the run checked, before opening a pull request, another LavaFlow pull
                request for the issue was open, or merged and not yet deployed, so this run opened none; a fix it wrote stays on
                the run. That pull request may have closed since; find it with `GET /lavaflow/runs?project_id=…&issue_id=…`,
                whose runs carry their `pull_request`. Review it, or close it if you don't want it. `source_unavailable`:
                LavaFlow couldn't read, or open a fix on, the code that served the error; the run's `source_unavailable` says
                why and what to do. `permission_missing`: the Volcano GitHub App, or the project owner's GitHub account, lacks a
                permission LavaFlow needs; grant the App's requested permissions and make sure the owner can push to the
                repository. `repository_changed`: the project no longer deploys from the repository the run read; a new run uses
                the current one. `publish_failed`: opening the pull request failed; a new run tries again. `draft_unavailable`:
                GitHub refused a draft required for a proposal with outstanding external work. Check that the base branch exists
                and that the repository supports draft pull requests before trying again. `lineage_cap`: LavaFlow opened as many
                pull requests in this fix's lineage as it may; review the lineage's pull requests and fix the rest yourself.
                `lineage_held`: an earlier pull request in this fix's lineage was held, stopped or closed (one a person merges
                holds it only when closed), so LavaFlow opens no more in it; apply the fix yourself from the diagnosis.
                `review_unresolved`: LavaFlow's review didn't pass a Code Quality fix; read the diagnosis.
                `duplicate_in_repository`: when the run checked, another project on the repository already had the Code Quality
                pull request for the same finding; review that pull request in the repository. `security_finding`: the finding
                has security impact and the repository isn't private, so the fix would disclose it; fix it yourself. New reasons
                may appear.
            recorded_at (datetime.datetime | None):
     """

    reason: LavaflowSkipReason
    recorded_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        reason: str = self.reason

        recorded_at: None | str
        if isinstance(self.recorded_at, datetime.datetime):
            recorded_at = self.recorded_at.isoformat()
        else:
            recorded_at = self.recorded_at


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "reason": reason,
            "recorded_at": recorded_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = check_lavaflow_skip_reason(d.pop("reason"))




        def _parse_recorded_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                recorded_at_type_0 = datetime.datetime.fromisoformat(data)



                return recorded_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        recorded_at = _parse_recorded_at(d.pop("recorded_at"))


        lavaflow_delivery_skip = cls(
            reason=reason,
            recorded_at=recorded_at,
        )


        lavaflow_delivery_skip.additional_properties = d
        return lavaflow_delivery_skip

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
