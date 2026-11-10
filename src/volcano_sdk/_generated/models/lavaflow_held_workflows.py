from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.lavaflow_allowed_workflow import LavaflowAllowedWorkflow
  from ..models.lavaflow_workflow_source import LavaflowWorkflowSource





T = TypeVar("T", bound="LavaflowHeldWorkflows")



@_attrs_define
class LavaflowHeldWorkflows:
    """ Every workflow job that could run a held fix's pull request with the repository's secrets before a person approves
    it, as LavaFlow found them when it held the fix, and the commits it read the workflows at.

        Attributes:
            read_at (list[LavaflowWorkflowSource]): Each branch or commit whose workflows LavaFlow read: the project's
                production branch, the repository's default branch, and the commit the fix is cut from.
            jobs (list[LavaflowAllowedWorkflow]): Every such job, at most 256, sorted by source, path and job. Empty when
                LavaFlow read every workflow to the end and found none, such as when they changed between the hold and the read.
            jobs_sha256 (str): Identifies `read_at` and `jobs` together. Treat it as opaque: it changes when a listed job,
                or a commit the workflows were read at, does. Example:
                2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae.
     """

    read_at: list[LavaflowWorkflowSource]
    jobs: list[LavaflowAllowedWorkflow]
    jobs_sha256: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_allowed_workflow import LavaflowAllowedWorkflow # noqa: PLC0415
        from ..models.lavaflow_workflow_source import LavaflowWorkflowSource # noqa: PLC0415
        read_at = []
        for read_at_item_data in self.read_at:
            read_at_item = read_at_item_data.to_dict()
            read_at.append(read_at_item)



        jobs = []
        for jobs_item_data in self.jobs:
            jobs_item = jobs_item_data.to_dict()
            jobs.append(jobs_item)



        jobs_sha256 = self.jobs_sha256


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "read_at": read_at,
            "jobs": jobs,
            "jobs_sha256": jobs_sha256,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_allowed_workflow import LavaflowAllowedWorkflow # noqa: PLC0415
        from ..models.lavaflow_workflow_source import LavaflowWorkflowSource # noqa: PLC0415
        d = dict(src_dict)
        read_at = []
        _read_at = d.pop("read_at")
        for read_at_item_data in (_read_at):
            read_at_item = LavaflowWorkflowSource.from_dict(read_at_item_data)



            read_at.append(read_at_item)


        jobs = []
        _jobs = d.pop("jobs")
        for jobs_item_data in (_jobs):
            jobs_item = LavaflowAllowedWorkflow.from_dict(jobs_item_data)



            jobs.append(jobs_item)


        jobs_sha256 = d.pop("jobs_sha256")

        lavaflow_held_workflows = cls(
            read_at=read_at,
            jobs=jobs,
            jobs_sha256=jobs_sha256,
        )


        lavaflow_held_workflows.additional_properties = d
        return lavaflow_held_workflows

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
