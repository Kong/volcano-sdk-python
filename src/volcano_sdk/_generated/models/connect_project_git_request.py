from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="ConnectProjectGitRequest")



@_attrs_define
class ConnectProjectGitRequest:
    """ 
        Attributes:
            connection_id (UUID): The caller's user_git_connections row (see /user/git/connections).
            installation_id (int):
            repository_id (int | Unset): Stable GitHub repository id (repository.id), the preferred selector. Either
                repository_id or repo_full_name is required; when both are given they must identify the same live repository.
            repo_full_name (str | Unset): Deprecated selector kept for a compatibility window; prefer repository_id. Either
                repository_id or repo_full_name is required.
            root_directory (str | Unset): Monorepo subdirectory the project builds from. Omit for the repo root.
            production_branch (str | Unset): The branch a push must land on to deploy, with three cases, because this is a
                full replace and a read-modify-write client sends back whatever it read. Omit it to follow the repository's
                GitHub default branch, which also discards a branch set earlier. Send back the branch the project already
                deploys from, when that is the repository's default, and nothing changes either way — a project pinned to that
                branch stays pinned. Sending the default branch when the project deploys from something else returns it to
                following the default, including on a rebind, where a pin describes a branch chosen for the repository being
                left. Any other branch becomes the project's own choice, exempt from later default-branch renames. Validated as
                a Git branch name only: it does not have to exist yet, so a project can be pointed at a branch about to be
                pushed. Changing repository and naming a branch other than the new repository's default in one request is
                refused with 400, because the branch named is almost always the previous repository's, echoed back — connect
                first, then set the branch.
     """

    connection_id: UUID
    installation_id: int
    repository_id: int | Unset = UNSET
    repo_full_name: str | Unset = UNSET
    root_directory: str | Unset = UNSET
    production_branch: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        connection_id = str(self.connection_id)

        installation_id = self.installation_id

        repository_id = self.repository_id

        repo_full_name = self.repo_full_name

        root_directory = self.root_directory

        production_branch = self.production_branch


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "connection_id": connection_id,
            "installation_id": installation_id,
        })
        if repository_id is not UNSET:
            field_dict["repository_id"] = repository_id
        if repo_full_name is not UNSET:
            field_dict["repo_full_name"] = repo_full_name
        if root_directory is not UNSET:
            field_dict["root_directory"] = root_directory
        if production_branch is not UNSET:
            field_dict["production_branch"] = production_branch

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        connection_id = UUID(d.pop("connection_id"))




        installation_id = d.pop("installation_id")

        repository_id = d.pop("repository_id", UNSET)

        repo_full_name = d.pop("repo_full_name", UNSET)

        root_directory = d.pop("root_directory", UNSET)

        production_branch = d.pop("production_branch", UNSET)

        connect_project_git_request = cls(
            connection_id=connection_id,
            installation_id=installation_id,
            repository_id=repository_id,
            repo_full_name=repo_full_name,
            root_directory=root_directory,
            production_branch=production_branch,
        )


        connect_project_git_request.additional_properties = d
        return connect_project_git_request

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
