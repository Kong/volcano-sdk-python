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
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.lavaflow_code_quality_settings import LavaflowCodeQualitySettings
  from ..models.lavaflow_failure import LavaflowFailure
  from ..models.lavaflow_merge_policy import LavaflowMergePolicy
  from ..models.project_git_connection_summary import ProjectGitConnectionSummary





T = TypeVar("T", bound="LavaflowSettings")



@_attrs_define
class LavaflowSettings:
    """ A project's LavaFlow settings. LavaFlow sends this project's logs and source code to an AI service that Volcano
    operates.

        Attributes:
            project_id (UUID): The project the settings belong to.
            enabled (bool): Whether LavaFlow works on the project's issues. Off by default.
            autonomy (LavaflowAutonomy): How far LavaFlow goes on its own. `diagnose_only` stops at a diagnosis. `open_pr`
                also opens a pull request with a fix, and never merges it. `merge` also merges the fix once LavaFlow's reviewers
                pass it, its required checks pass, and nothing holds it; a held fix is handed to you for good. Turning on merge
                lets LavaFlow's fixes, including those from runs it starts on its own, run your CI with the secrets your pull
                request workflows get. Choosing `merge` needs the project's `lavaflow.merge` capability.
            merge_policy (LavaflowMergePolicy): Your rules for fixes LavaFlow must never merge. They apply with `autonomy:
                merge`; at another autonomy they are saved and do nothing.
            skill_learning (LavaflowSkillLearning): What LavaFlow will do with a skill it learns from a writer's correction
                of one of its fixes, once learning ships in a later release. `auto`, the default, activates it at once. `review`
                keeps it `proposed` until the owner activates it. `off` learns none and loads no project skill; the project's
                skills stay readable and deletable. A writer of the repository can steer LavaFlow through what it learns,
                outside the repository's history and branch protection, so a repository that protects its guidance, or relays CI
                output through a bot account with write access, should use `review`. Turning learning up needs the project's
                `lavaflow.skills` capability.
            custom_context (str): Context about the project for LavaFlow's runs. Empty when unset. Saved, but runs do not
                use it yet.
            system_prompt (str): Instructions for LavaFlow's runs, to follow after LavaFlow's own, which take precedence.
                Empty when unset. Saved, but runs do not use it yet.
            code_quality (LavaflowCodeQualitySettings): LavaFlow Code Quality: whether LavaFlow reviews the code each
                production deploy changes and opens pull requests that fix what it confirms.
            allow_ungated_workflows (bool): Whether LavaFlow opens a fix's pull request even where a workflow could run it,
                or put its text into a command, with the repository's secrets before a person approves it. Off by default; while
                off, such a fix stays on its run and no pull request opens. Only the project's owner turns it on, signed in as a
                person: with the platform token `volcano login` stores, or another platform token that expires. It applies to
                the repository their GitHub account can push to. Connecting the project to another repository, or disconnecting
                it, turns it off, and connecting the first one again doesn't turn it back on. Workflows in the repository may
                then run LavaFlow's pull requests, or put their text into commands, with the repository's secrets before a
                person reviews them. LavaFlow writes those changes from the project's error logs, which its users can influence.
                Turn it on only if those workflows keep secrets away from untrusted code; gating them on a label a person adds
                is safer.
            updated_at (datetime.datetime | None): When the settings were last saved, or last changed by connecting a
                repository. Null until they first are.
            updated_by (None | str): The user ID of the person who made the last save; null when no person made it, such as
                a project access token.
            can_update (bool): Whether the caller can save the settings: true only for the project's owner with a platform
                token while the owner's account is active; false for any project access token and for a read-only account.
            repository (None | ProjectGitConnectionSummary): The GitHub repository the project is linked to, as `GET
                /projects/{id}/git-connection` reports it. LavaFlow opens fix pull requests there, against `production_branch`.
                Null when the project has none.
            fix_blocker (LavaflowFailure | None): What in the project's repository setup stops LavaFlow from fixing issues
                although it is on. Null when the repository setup doesn't, and while the project's `lavaflow` capability isn't
                available; null doesn't mean nothing else stops LavaFlow. `message` is text to show as given.
                `repository_required`: the project has no linked repository. With `autonomy` `open_pr` or `merge`, LavaFlow
                diagnoses issues but fixes none; turned on for a repository the project no longer links, it starts no runs. Link
                a repository with `PUT /projects/{id}/git-connection` or `volcano git connect <git-url>`. Turned on with none,
                LavaFlow fixes issues in the first one linked, unless `message` asks to turn it on again after the link; linking
                the one it was turned on for resumes it. `repository_changed`: the project is linked to a repository LavaFlow
                wasn't turned on for. LavaFlow starts no runs until the owner turns it on again, with `{"enabled": true}` or
                `volcano cloud lavaflow enable`, which makes the linked repository the one it fixes. New codes may appear; show
                the `message` of one you don't know.
     """

    project_id: UUID
    enabled: bool
    autonomy: LavaflowAutonomy
    merge_policy: LavaflowMergePolicy
    skill_learning: LavaflowSkillLearning
    custom_context: str
    system_prompt: str
    code_quality: LavaflowCodeQualitySettings
    allow_ungated_workflows: bool
    updated_at: datetime.datetime | None
    updated_by: None | str
    can_update: bool
    repository: None | ProjectGitConnectionSummary
    fix_blocker: LavaflowFailure | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_code_quality_settings import LavaflowCodeQualitySettings # noqa: PLC0415
        from ..models.lavaflow_failure import LavaflowFailure # noqa: PLC0415
        from ..models.lavaflow_merge_policy import LavaflowMergePolicy # noqa: PLC0415
        from ..models.project_git_connection_summary import ProjectGitConnectionSummary # noqa: PLC0415
        project_id = str(self.project_id)

        enabled = self.enabled

        autonomy: str = self.autonomy

        merge_policy = self.merge_policy.to_dict()

        skill_learning: str = self.skill_learning

        custom_context = self.custom_context

        system_prompt = self.system_prompt

        code_quality = self.code_quality.to_dict()

        allow_ungated_workflows = self.allow_ungated_workflows

        updated_at: None | str
        if isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        updated_by: None | str
        updated_by = self.updated_by

        can_update = self.can_update

        repository: dict[str, Any] | None
        if isinstance(self.repository, ProjectGitConnectionSummary):
            repository = self.repository.to_dict()
        else:
            repository = self.repository

        fix_blocker: dict[str, Any] | None
        if isinstance(self.fix_blocker, LavaflowFailure):
            fix_blocker = self.fix_blocker.to_dict()
        else:
            fix_blocker = self.fix_blocker


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "project_id": project_id,
            "enabled": enabled,
            "autonomy": autonomy,
            "merge_policy": merge_policy,
            "skill_learning": skill_learning,
            "custom_context": custom_context,
            "system_prompt": system_prompt,
            "code_quality": code_quality,
            "allow_ungated_workflows": allow_ungated_workflows,
            "updated_at": updated_at,
            "updated_by": updated_by,
            "can_update": can_update,
            "repository": repository,
            "fix_blocker": fix_blocker,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_code_quality_settings import LavaflowCodeQualitySettings # noqa: PLC0415
        from ..models.lavaflow_failure import LavaflowFailure # noqa: PLC0415
        from ..models.lavaflow_merge_policy import LavaflowMergePolicy # noqa: PLC0415
        from ..models.project_git_connection_summary import ProjectGitConnectionSummary # noqa: PLC0415
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        enabled = d.pop("enabled")

        autonomy = check_lavaflow_autonomy(d.pop("autonomy"))




        merge_policy = LavaflowMergePolicy.from_dict(d.pop("merge_policy"))




        skill_learning = check_lavaflow_skill_learning(d.pop("skill_learning"))




        custom_context = d.pop("custom_context")

        system_prompt = d.pop("system_prompt")

        code_quality = LavaflowCodeQualitySettings.from_dict(d.pop("code_quality"))




        allow_ungated_workflows = d.pop("allow_ungated_workflows")

        def _parse_updated_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = datetime.datetime.fromisoformat(data)



                return updated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        updated_at = _parse_updated_at(d.pop("updated_at"))


        def _parse_updated_by(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        updated_by = _parse_updated_by(d.pop("updated_by"))


        can_update = d.pop("can_update")

        def _parse_repository(data: object) -> None | ProjectGitConnectionSummary:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                repository_type_1 = ProjectGitConnectionSummary.from_dict(data)



                return repository_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProjectGitConnectionSummary, data)

        repository = _parse_repository(d.pop("repository"))


        def _parse_fix_blocker(data: object) -> LavaflowFailure | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                fix_blocker_type_1 = LavaflowFailure.from_dict(data)



                return fix_blocker_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowFailure | None, data)

        fix_blocker = _parse_fix_blocker(d.pop("fix_blocker"))


        lavaflow_settings = cls(
            project_id=project_id,
            enabled=enabled,
            autonomy=autonomy,
            merge_policy=merge_policy,
            skill_learning=skill_learning,
            custom_context=custom_context,
            system_prompt=system_prompt,
            code_quality=code_quality,
            allow_ungated_workflows=allow_ungated_workflows,
            updated_at=updated_at,
            updated_by=updated_by,
            can_update=can_update,
            repository=repository,
            fix_blocker=fix_blocker,
        )


        lavaflow_settings.additional_properties = d
        return lavaflow_settings

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
