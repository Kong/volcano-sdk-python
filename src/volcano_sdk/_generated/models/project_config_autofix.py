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






T = TypeVar("T", bound="ProjectConfigAutofix")



@_attrs_define
class ProjectConfigAutofix:
    """ AI diagnosis and fix settings. Omitted fields keep their current value; a project that never saved settings starts
    from `max_stage: pull_request` and `auto_trigger: true`.

        Attributes:
            enabled (bool | Unset):
            max_stage (AutofixStage | Unset): How far a run may go. `diagnose` stops at a root-cause diagnosis.
                `pull_request` may also open a draft pull request with a fix in the project's connected repository.
            auto_trigger (bool | Unset):
     """

    enabled: bool | Unset = UNSET
    max_stage: AutofixStage | Unset = UNSET
    auto_trigger: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        max_stage: str | Unset = UNSET
        if not isinstance(self.max_stage, Unset):
            max_stage = self.max_stage


        auto_trigger = self.auto_trigger


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if max_stage is not UNSET:
            field_dict["max_stage"] = max_stage
        if auto_trigger is not UNSET:
            field_dict["auto_trigger"] = auto_trigger

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        _max_stage = d.pop("max_stage", UNSET)
        max_stage: AutofixStage | Unset
        if isinstance(_max_stage,  Unset):
            max_stage = UNSET
        else:
            max_stage = check_autofix_stage(_max_stage)




        auto_trigger = d.pop("auto_trigger", UNSET)

        project_config_autofix = cls(
            enabled=enabled,
            max_stage=max_stage,
            auto_trigger=auto_trigger,
        )

        return project_config_autofix

