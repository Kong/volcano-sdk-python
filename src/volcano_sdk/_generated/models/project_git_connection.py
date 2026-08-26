from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="ProjectGitConnection")



@_attrs_define
class ProjectGitConnection:
    """ 
        Attributes:
            repo_installation_id (int):
            repo_id (int): Stable GitHub repository id (repository.id), the authoritative binding.
            repo_full_name (str):
            root_directory (str):
            production_branch (str): The branch a push must land on to deploy. Follows the repository's GitHub default
                branch unless the project set its own, which a default-branch rename on GitHub then leaves alone.
            updated_at (datetime.datetime):
     """

    repo_installation_id: int
    repo_id: int
    repo_full_name: str
    root_directory: str
    production_branch: str
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        repo_installation_id = self.repo_installation_id

        repo_id = self.repo_id

        repo_full_name = self.repo_full_name

        root_directory = self.root_directory

        production_branch = self.production_branch

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "repo_installation_id": repo_installation_id,
            "repo_id": repo_id,
            "repo_full_name": repo_full_name,
            "root_directory": root_directory,
            "production_branch": production_branch,
            "updated_at": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        repo_installation_id = d.pop("repo_installation_id")

        repo_id = d.pop("repo_id")

        repo_full_name = d.pop("repo_full_name")

        root_directory = d.pop("root_directory")

        production_branch = d.pop("production_branch")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        project_git_connection = cls(
            repo_installation_id=repo_installation_id,
            repo_id=repo_id,
            repo_full_name=repo_full_name,
            root_directory=root_directory,
            production_branch=production_branch,
            updated_at=updated_at,
        )


        project_git_connection.additional_properties = d
        return project_git_connection

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
