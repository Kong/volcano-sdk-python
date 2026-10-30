from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="DeploymentCommit")



@_attrs_define
class DeploymentCommit:
    """ The commit a deploy client reported for the deployment's source. Absent when the client reported none. A frontend
    deployment that publishes another deployment's build carries that deployment's commit.

        Attributes:
            repository (str): GitHub repository as `owner/name`, normalized from what the client sent. Example: acme/app.
            sha (str): Full commit ID.
            dirty (bool): `true` when the client reported that the uploaded files differ from the commit, or Volcano found
                an uploaded file in the project's root directory that the commit does not hold, so the deployed code may differ
                from the commit.
            verified (bool): `true` when Volcano confirmed, through the project's GitHub connection, that `repository` is
                the project's connected repository, `sha` is on its production branch, every uploaded file is the commit's file
                at its path, and the upload holds the commit's files under its root but those deploy clients leave out. Only
                frontend uploads are checked; a function deployment's commit, one the client reports dirty, and one from another
                branch, repository, or a project without a connection, is recorded unverified.
     """

    repository: str
    sha: str
    dirty: bool
    verified: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        repository = self.repository

        sha = self.sha

        dirty = self.dirty

        verified = self.verified


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "repository": repository,
            "sha": sha,
            "dirty": dirty,
            "verified": verified,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        repository = d.pop("repository")

        sha = d.pop("sha")

        dirty = d.pop("dirty")

        verified = d.pop("verified")

        deployment_commit = cls(
            repository=repository,
            sha=sha,
            dirty=dirty,
            verified=verified,
        )


        deployment_commit.additional_properties = d
        return deployment_commit

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
