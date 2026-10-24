from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.autofix_stage import AutofixStage
from ..models.autofix_stage import check_autofix_stage
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="AutofixSettings")



@_attrs_define
class AutofixSettings:
    """ 
        Attributes:
            project_id (UUID):
            enabled (bool): Whether Volcano diagnoses the project's issues with AI.
            max_stage (AutofixStage): How far a run may go. `diagnose` stops at a root-cause diagnosis. `pull_request` may
                also open a draft pull request with a fix in the project's connected repository.
            auto_trigger (bool): Whether a new or regressed issue starts a run on its own. Defaults to true. When false,
                runs start only on request.
            plan_includes_autofix (bool | Unset): Whether the owner's plan includes autofix. When false, saved settings stay
                stored and no run starts. Absent when a save that needed no plan succeeded but the plan could not be resolved.
            updated_at (datetime.datetime | Unset): When the settings were last saved. Absent until the first save.
     """

    project_id: UUID
    enabled: bool
    max_stage: AutofixStage
    auto_trigger: bool
    plan_includes_autofix: bool | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        enabled = self.enabled

        max_stage: str = self.max_stage

        auto_trigger = self.auto_trigger

        plan_includes_autofix = self.plan_includes_autofix

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "project_id": project_id,
            "enabled": enabled,
            "max_stage": max_stage,
            "auto_trigger": auto_trigger,
        })
        if plan_includes_autofix is not UNSET:
            field_dict["plan_includes_autofix"] = plan_includes_autofix
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        enabled = d.pop("enabled")

        max_stage = check_autofix_stage(d.pop("max_stage"))




        auto_trigger = d.pop("auto_trigger")

        plan_includes_autofix = d.pop("plan_includes_autofix", UNSET)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at,  Unset):
            updated_at = UNSET
        else:
            updated_at = datetime.datetime.fromisoformat(_updated_at)




        autofix_settings = cls(
            project_id=project_id,
            enabled=enabled,
            max_stage=max_stage,
            auto_trigger=auto_trigger,
            plan_includes_autofix=plan_includes_autofix,
            updated_at=updated_at,
        )

        return autofix_settings

