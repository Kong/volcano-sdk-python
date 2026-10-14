from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.autofix_model import AutofixModel
from ..models.autofix_model import check_autofix_model
from ..models.autofix_provider import AutofixProvider
from ..models.autofix_provider import check_autofix_provider
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
            auto_trigger (bool): Whether a new or reopened issue starts a run on its own. When false, runs start only on
                request.
            provider (AutofixProvider): Who serves the model. `volcano` runs on Volcano's models. `anthropic` runs on your
                own Anthropic API key.
            model (AutofixModel): The Claude model a run uses. `claude-opus-5-5` is the default.
            api_key_configured (bool): Whether your own API key is stored. The key itself is never returned.
            api_key_provider (AutofixProvider | Unset): Who serves the model. `volcano` runs on Volcano's models.
                `anthropic` runs on your own Anthropic API key.
            api_key_last4 (str | Unset): The stored key's last four characters, present when one is stored.
            plan_includes_autofix (bool | Unset): Whether the owner's plan includes autofix. When false, saved settings stay
                stored and no run starts. Absent when a save that needed no plan succeeded but the plan could not be resolved.
            updated_at (datetime.datetime | Unset): When the settings were last saved. Absent until the first save.
     """

    project_id: UUID
    enabled: bool
    max_stage: AutofixStage
    auto_trigger: bool
    provider: AutofixProvider
    model: AutofixModel
    api_key_configured: bool
    api_key_provider: AutofixProvider | Unset = UNSET
    api_key_last4: str | Unset = UNSET
    plan_includes_autofix: bool | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        enabled = self.enabled

        max_stage: str = self.max_stage

        auto_trigger = self.auto_trigger

        provider: str = self.provider

        model: str = self.model

        api_key_configured = self.api_key_configured

        api_key_provider: str | Unset = UNSET
        if not isinstance(self.api_key_provider, Unset):
            api_key_provider = self.api_key_provider


        api_key_last4 = self.api_key_last4

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
            "provider": provider,
            "model": model,
            "api_key_configured": api_key_configured,
        })
        if api_key_provider is not UNSET:
            field_dict["api_key_provider"] = api_key_provider
        if api_key_last4 is not UNSET:
            field_dict["api_key_last4"] = api_key_last4
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

        provider = check_autofix_provider(d.pop("provider"))




        model = check_autofix_model(d.pop("model"))




        api_key_configured = d.pop("api_key_configured")

        _api_key_provider = d.pop("api_key_provider", UNSET)
        api_key_provider: AutofixProvider | Unset
        if isinstance(_api_key_provider,  Unset):
            api_key_provider = UNSET
        else:
            api_key_provider = check_autofix_provider(_api_key_provider)




        api_key_last4 = d.pop("api_key_last4", UNSET)

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
            provider=provider,
            model=model,
            api_key_configured=api_key_configured,
            api_key_provider=api_key_provider,
            api_key_last4=api_key_last4,
            plan_includes_autofix=plan_includes_autofix,
            updated_at=updated_at,
        )

        return autofix_settings

