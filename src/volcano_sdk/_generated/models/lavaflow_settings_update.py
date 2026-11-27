from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_autonomy import check_lavaflow_autonomy
from ..models.lavaflow_autonomy import LavaflowAutonomy
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.lavaflow_code_quality_update import LavaflowCodeQualityUpdate
  from ..models.lavaflow_merge_policy_update import LavaflowMergePolicyUpdate
  from ..models.lavaflow_repository_expectation import LavaflowRepositoryExpectation





T = TypeVar("T", bound="LavaflowSettingsUpdate")



@_attrs_define
class LavaflowSettingsUpdate:
    """ The project, and at least one field to change. An omitted field keeps its saved value. A repository precondition
    alone is not a setting change.

        Attributes:
            project_id (UUID): The project whose settings to change.
            enabled (bool | Unset):
            autonomy (LavaflowAutonomy | Unset): How far LavaFlow goes on its own. `diagnose_only` stops at a diagnosis.
                `open_pr` also opens a pull request with a fix, and never merges it. `merge` also merges the fix once LavaFlow's
                reviewers pass it, its required checks pass, and nothing holds it; a held fix is handed to you for good.
                LavaFlow merges only into a base branch that requires at least one status check, through branch protection or a
                ruleset; on any other branch it holds every fix with `no_required_checks`. Turning on merge lets LavaFlow's
                fixes, including those from runs it starts on its own, run your CI with the secrets your pull request workflows
                get. Choosing `merge` needs the project's `lavaflow.merge` capability.
            merge_policy (LavaflowMergePolicyUpdate | Unset): The merge policy fields to change. An omitted field keeps its
                saved value. Send `human_review_paths: []` to clear the paths.
            code_quality (LavaflowCodeQualityUpdate | Unset): Turns Code Quality on or off. Only the project's owner, signed
                in, can turn it on; any credential that can save the settings can turn it off.
            expected_repository (LavaflowRepositoryExpectation | Unset): The repository connection the caller expects. This
                is a save precondition, not an instruction to change the connection.
            allow_ungated_workflows (bool | Unset): Grants or revokes repository CI permission for the current repository
                and GitHub App installation. Normal repository CI requires both this permission and lavaflow.repository_ci
                availability. Only the project owner can grant it, using a live login credential or an expiring platform token;
                their GitHub account must have push access to the connected repository. Project tokens, non-expiring platform
                tokens, and other users cannot grant it (403 person_required). Any owner credential can revoke it. Generated
                fixes may be influenced by untrusted issue and log input, and configured CI and previews may execute those fixes
                with their credentials before human review. This includes draft PRs, fixes whose LavaFlow review did not pass,
                and fixes held for a person to review. In Merge mode, eligible fixes from connected issue sources can use this
                grant while LavaFlow follows them through the repository's required reviews and checks. Changing or
                disconnecting the repository or installation revokes the grant; returning to an earlier binding does not restore
                it. Revocation does not cancel existing PRs or CI runs. While LavaFlow is unavailable, only false is saved,
                together with enabled: false.
     """

    project_id: UUID
    enabled: bool | Unset = UNSET
    autonomy: LavaflowAutonomy | Unset = UNSET
    merge_policy: LavaflowMergePolicyUpdate | Unset = UNSET
    code_quality: LavaflowCodeQualityUpdate | Unset = UNSET
    expected_repository: LavaflowRepositoryExpectation | Unset = UNSET
    allow_ungated_workflows: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_code_quality_update import LavaflowCodeQualityUpdate # noqa: PLC0415
        from ..models.lavaflow_merge_policy_update import LavaflowMergePolicyUpdate # noqa: PLC0415
        from ..models.lavaflow_repository_expectation import LavaflowRepositoryExpectation # noqa: PLC0415
        project_id = str(self.project_id)

        enabled = self.enabled

        autonomy: str | Unset = UNSET
        if not isinstance(self.autonomy, Unset):
            autonomy = self.autonomy


        merge_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.merge_policy, Unset):
            merge_policy = self.merge_policy.to_dict()

        code_quality: dict[str, Any] | Unset = UNSET
        if not isinstance(self.code_quality, Unset):
            code_quality = self.code_quality.to_dict()

        expected_repository: dict[str, Any] | Unset = UNSET
        if not isinstance(self.expected_repository, Unset):
            expected_repository = self.expected_repository.to_dict()

        allow_ungated_workflows = self.allow_ungated_workflows


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "project_id": project_id,
        })
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if autonomy is not UNSET:
            field_dict["autonomy"] = autonomy
        if merge_policy is not UNSET:
            field_dict["merge_policy"] = merge_policy
        if code_quality is not UNSET:
            field_dict["code_quality"] = code_quality
        if expected_repository is not UNSET:
            field_dict["expected_repository"] = expected_repository
        if allow_ungated_workflows is not UNSET:
            field_dict["allow_ungated_workflows"] = allow_ungated_workflows

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_code_quality_update import LavaflowCodeQualityUpdate # noqa: PLC0415
        from ..models.lavaflow_merge_policy_update import LavaflowMergePolicyUpdate # noqa: PLC0415
        from ..models.lavaflow_repository_expectation import LavaflowRepositoryExpectation # noqa: PLC0415
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        enabled = d.pop("enabled", UNSET)

        _autonomy = d.pop("autonomy", UNSET)
        autonomy: LavaflowAutonomy | Unset
        if isinstance(_autonomy,  Unset):
            autonomy = UNSET
        else:
            autonomy = check_lavaflow_autonomy(_autonomy)




        _merge_policy = d.pop("merge_policy", UNSET)
        merge_policy: LavaflowMergePolicyUpdate | Unset
        if isinstance(_merge_policy,  Unset):
            merge_policy = UNSET
        else:
            merge_policy = LavaflowMergePolicyUpdate.from_dict(_merge_policy)




        _code_quality = d.pop("code_quality", UNSET)
        code_quality: LavaflowCodeQualityUpdate | Unset
        if isinstance(_code_quality,  Unset):
            code_quality = UNSET
        else:
            code_quality = LavaflowCodeQualityUpdate.from_dict(_code_quality)




        _expected_repository = d.pop("expected_repository", UNSET)
        expected_repository: LavaflowRepositoryExpectation | Unset
        if isinstance(_expected_repository,  Unset):
            expected_repository = UNSET
        else:
            expected_repository = LavaflowRepositoryExpectation.from_dict(_expected_repository)




        allow_ungated_workflows = d.pop("allow_ungated_workflows", UNSET)

        lavaflow_settings_update = cls(
            project_id=project_id,
            enabled=enabled,
            autonomy=autonomy,
            merge_policy=merge_policy,
            code_quality=code_quality,
            expected_repository=expected_repository,
            allow_ungated_workflows=allow_ungated_workflows,
        )

        return lavaflow_settings_update

