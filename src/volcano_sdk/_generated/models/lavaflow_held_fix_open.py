from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="LavaflowHeldFixOpen")



@_attrs_define
class LavaflowHeldFixOpen:
    """ The project, the run, and the diff and jobs of the held fix you read, by the digests the run served them with.

        Attributes:
            project_id (UUID): The project the run belongs to.
            run_id (UUID): The run whose held fix to open.
            diff_sha256 (str): The run's `diff_sha256`, as it served it. Example:
                9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08.
            jobs_sha256 (str): The run's `held_workflows.jobs_sha256`, as it served it. Example:
                2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae.
     """

    project_id: UUID
    run_id: UUID
    diff_sha256: str
    jobs_sha256: str





    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        run_id = str(self.run_id)

        diff_sha256 = self.diff_sha256

        jobs_sha256 = self.jobs_sha256


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "project_id": project_id,
            "run_id": run_id,
            "diff_sha256": diff_sha256,
            "jobs_sha256": jobs_sha256,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        run_id = UUID(d.pop("run_id"))




        diff_sha256 = d.pop("diff_sha256")

        jobs_sha256 = d.pop("jobs_sha256")

        lavaflow_held_fix_open = cls(
            project_id=project_id,
            run_id=run_id,
            diff_sha256=diff_sha256,
            jobs_sha256=jobs_sha256,
        )

        return lavaflow_held_fix_open

