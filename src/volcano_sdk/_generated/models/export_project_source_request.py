from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ExportProjectSourceRequest")



@_attrs_define
class ExportProjectSourceRequest:
    """ 
        Attributes:
            production_branch (str): The currently configured production branch the user confirmed for export.
            repo_id (int | Unset): The `repo_id` of the connected repository the user confirmed for
                export, as the git connection reports it. When set, export answers
                `409` if the project is now connected to a different repository, so
                source is written only to the repository the user was shown.
     """

    production_branch: str
    repo_id: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        production_branch = self.production_branch

        repo_id = self.repo_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "production_branch": production_branch,
        })
        if repo_id is not UNSET:
            field_dict["repo_id"] = repo_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        production_branch = d.pop("production_branch")

        repo_id = d.pop("repo_id", UNSET)

        export_project_source_request = cls(
            production_branch=production_branch,
            repo_id=repo_id,
        )

        return export_project_source_request

