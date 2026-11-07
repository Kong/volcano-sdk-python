from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_autonomy import check_lavaflow_autonomy
from ..models.lavaflow_autonomy import LavaflowAutonomy
from ..models.lavaflow_skill_learning import check_lavaflow_skill_learning
from ..models.lavaflow_skill_learning import LavaflowSkillLearning
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.lavaflow_code_quality_update import LavaflowCodeQualityUpdate
  from ..models.lavaflow_merge_policy_update import LavaflowMergePolicyUpdate





T = TypeVar("T", bound="LavaflowSettingsUpdate")



@_attrs_define
class LavaflowSettingsUpdate:
    """ The project, and at least one field to change. An omitted field keeps its saved value.

        Attributes:
            project_id (UUID): The project whose settings to change.
            enabled (bool | Unset):
            autonomy (LavaflowAutonomy | Unset): How far LavaFlow goes on its own. `diagnose_only` stops at a diagnosis.
                `open_pr` also opens a pull request with a fix, and never merges it. `merge` also merges the fix once LavaFlow's
                reviewers pass it, its required checks pass, and nothing holds it; a held fix is handed to you for good. Turning
                on merge lets LavaFlow's fixes, including those from runs it starts on its own, run your CI with the secrets
                your pull request workflows get. Choosing `merge` needs the project's `lavaflow.merge` capability.
            merge_policy (LavaflowMergePolicyUpdate | Unset): The merge policy fields to change. An omitted field keeps its
                saved value. Send `human_review_paths: []` to clear the paths.
            skill_learning (LavaflowSkillLearning | Unset): What LavaFlow will do with a skill it learns from a writer's
                correction of one of its fixes, once learning ships in a later release. `auto`, the default, activates it at
                once. `review` keeps it `proposed` until the owner activates it. `off` learns none and loads no project skill;
                the project's skills stay readable and deletable. A writer of the repository can steer LavaFlow through what it
                learns, outside the repository's history and branch protection, so a repository that protects its guidance, or
                relays CI output through a bot account with write access, should use `review`. Turning learning up needs the
                project's `lavaflow.skills` capability.
            custom_context (str | Unset):
            system_prompt (str | Unset):
            code_quality (LavaflowCodeQualityUpdate | Unset): Turns Code Quality on or off. Only the project's owner, signed
                in, can turn it on; any credential that can save the settings can turn it off.
            allow_ungated_workflows (bool | Unset): Turns on opening fixes past ungated workflows, for the repository the
                project is connected to now; it applies only to that repository. Only the project's owner turns it on, signed in
                as a person: with the platform token `volcano login` stores, or another platform token that expires. Their
                GitHub account must be able to push to that repository. A project access token, a platform token that never
                expires, or anyone else gets `403` with `person_required`. Any of the owner's credentials turns it off.
                Workflows in the repository may then run LavaFlow's pull requests, or put their text into commands, with the
                repository's secrets before a person reviews them. LavaFlow writes those changes from the project's error logs,
                which its users can influence. Turn it on only if those workflows keep secrets away from untrusted code; gating
                them on a label a person adds is safer. While LavaFlow is not available, only `false` is saved, and only with
                `enabled: false`, `skill_learning: off` or both.
     """

    project_id: UUID
    enabled: bool | Unset = UNSET
    autonomy: LavaflowAutonomy | Unset = UNSET
    merge_policy: LavaflowMergePolicyUpdate | Unset = UNSET
    skill_learning: LavaflowSkillLearning | Unset = UNSET
    custom_context: str | Unset = UNSET
    system_prompt: str | Unset = UNSET
    code_quality: LavaflowCodeQualityUpdate | Unset = UNSET
    allow_ungated_workflows: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_code_quality_update import LavaflowCodeQualityUpdate # noqa: PLC0415
        from ..models.lavaflow_merge_policy_update import LavaflowMergePolicyUpdate # noqa: PLC0415
        project_id = str(self.project_id)

        enabled = self.enabled

        autonomy: str | Unset = UNSET
        if not isinstance(self.autonomy, Unset):
            autonomy = self.autonomy


        merge_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.merge_policy, Unset):
            merge_policy = self.merge_policy.to_dict()

        skill_learning: str | Unset = UNSET
        if not isinstance(self.skill_learning, Unset):
            skill_learning = self.skill_learning


        custom_context = self.custom_context

        system_prompt = self.system_prompt

        code_quality: dict[str, Any] | Unset = UNSET
        if not isinstance(self.code_quality, Unset):
            code_quality = self.code_quality.to_dict()

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
        if skill_learning is not UNSET:
            field_dict["skill_learning"] = skill_learning
        if custom_context is not UNSET:
            field_dict["custom_context"] = custom_context
        if system_prompt is not UNSET:
            field_dict["system_prompt"] = system_prompt
        if code_quality is not UNSET:
            field_dict["code_quality"] = code_quality
        if allow_ungated_workflows is not UNSET:
            field_dict["allow_ungated_workflows"] = allow_ungated_workflows

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_code_quality_update import LavaflowCodeQualityUpdate # noqa: PLC0415
        from ..models.lavaflow_merge_policy_update import LavaflowMergePolicyUpdate # noqa: PLC0415
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




        _skill_learning = d.pop("skill_learning", UNSET)
        skill_learning: LavaflowSkillLearning | Unset
        if isinstance(_skill_learning,  Unset):
            skill_learning = UNSET
        else:
            skill_learning = check_lavaflow_skill_learning(_skill_learning)




        custom_context = d.pop("custom_context", UNSET)

        system_prompt = d.pop("system_prompt", UNSET)

        _code_quality = d.pop("code_quality", UNSET)
        code_quality: LavaflowCodeQualityUpdate | Unset
        if isinstance(_code_quality,  Unset):
            code_quality = UNSET
        else:
            code_quality = LavaflowCodeQualityUpdate.from_dict(_code_quality)




        allow_ungated_workflows = d.pop("allow_ungated_workflows", UNSET)

        lavaflow_settings_update = cls(
            project_id=project_id,
            enabled=enabled,
            autonomy=autonomy,
            merge_policy=merge_policy,
            skill_learning=skill_learning,
            custom_context=custom_context,
            system_prompt=system_prompt,
            code_quality=code_quality,
            allow_ungated_workflows=allow_ungated_workflows,
        )

        return lavaflow_settings_update

