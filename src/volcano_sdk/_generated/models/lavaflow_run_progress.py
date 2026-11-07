from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_run_progress_stage import check_lavaflow_run_progress_stage
from ..models.lavaflow_run_progress_stage import LavaflowRunProgressStage
from typing import cast






T = TypeVar("T", bound="LavaflowRunProgress")



@_attrs_define
class LavaflowRunProgress:
    """ How far an active run has come. The steps are `queued`, `diagnosing`, `fixing`, `reviewing`, `waiting_for_checks`
    and `merge_queued`, in that order, and a run takes as many as its autonomy when it was queued allows: 2 for
    `diagnose_only`, 4 for `open_pr` (opening the pull request ends it), 6 for `merge` (the merge ends it).

        Attributes:
            stage (LavaflowRunProgressStage): New stages may appear.
            step (int): The stage's place among the run's steps, from 1.
            steps (int): How many steps the run takes.
     """

    stage: LavaflowRunProgressStage
    step: int
    steps: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        stage: str = self.stage

        step = self.step

        steps = self.steps


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "stage": stage,
            "step": step,
            "steps": steps,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        stage = check_lavaflow_run_progress_stage(d.pop("stage"))




        step = d.pop("step")

        steps = d.pop("steps")

        lavaflow_run_progress = cls(
            stage=stage,
            step=step,
            steps=steps,
        )


        lavaflow_run_progress.additional_properties = d
        return lavaflow_run_progress

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
