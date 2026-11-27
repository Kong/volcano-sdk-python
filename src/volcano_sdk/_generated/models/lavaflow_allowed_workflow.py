from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="LavaflowAllowedWorkflow")



@_attrs_define
class LavaflowAllowedWorkflow:
    """ A workflow job that could run a fix's pull request with the repository's secrets before a person approves it.

        Attributes:
            source (str): The branch or commit whose workflows run it. Example: main.
            path (str):  Example: .github/workflows/preview.yml.
            job (str | Unset): The job, absent for a workflow that could not be read. Example: deploy-preview.
            trigger (str | Unset): The event that runs it, absent for a workflow that could not be read. Example:
                pull_request_target.
     """

    source: str
    path: str
    job: str | Unset = UNSET
    trigger: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        source = self.source

        path = self.path

        job = self.job

        trigger = self.trigger


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "source": source,
            "path": path,
        })
        if job is not UNSET:
            field_dict["job"] = job
        if trigger is not UNSET:
            field_dict["trigger"] = trigger

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = d.pop("source")

        path = d.pop("path")

        job = d.pop("job", UNSET)

        trigger = d.pop("trigger", UNSET)

        lavaflow_allowed_workflow = cls(
            source=source,
            path=path,
            job=job,
            trigger=trigger,
        )


        lavaflow_allowed_workflow.additional_properties = d
        return lavaflow_allowed_workflow

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
