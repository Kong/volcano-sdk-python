from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="LavaflowRunCreate")



@_attrs_define
class LavaflowRunCreate:
    """ The project, and the issue to start a run on.

        Attributes:
            project_id (UUID): The project the issue belongs to.
            issue_id (UUID): The issue to start a run on.
     """

    project_id: UUID
    issue_id: UUID





    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        issue_id = str(self.issue_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "project_id": project_id,
            "issue_id": issue_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        issue_id = UUID(d.pop("issue_id"))




        lavaflow_run_create = cls(
            project_id=project_id,
            issue_id=issue_id,
        )

        return lavaflow_run_create

