from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_git_owner_push_reason import check_project_git_owner_push_reason
from ..models.project_git_owner_push_reason import ProjectGitOwnerPushReason
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProjectGitOwnerPush")



@_attrs_define
class ProjectGitOwnerPush:
    """ Whether the project owner can push to the project's connected repository.

        Attributes:
            repository_id (int): Stable GitHub repository id of the connected repository, the `repo_id` of the project's git
                connection.
            can_push (bool): True when the project owner's GitHub account can push to the repository.
            reason (ProjectGitOwnerPushReason | Unset): Why `can_push` is false; absent when it is true.
                `owner_not_connected`: the owner has not connected a GitHub account. `owner_reconnect_required`: the owner's
                GitHub connection expired or was revoked; the owner reconnects GitHub. `repository_access_lost`: the owner's
                GitHub account can no longer see the repository. `no_push_permission`: the owner's GitHub account can read the
                repository but not push to it.
     """

    repository_id: int
    can_push: bool
    reason: ProjectGitOwnerPushReason | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        repository_id = self.repository_id

        can_push = self.can_push

        reason: str | Unset = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "repository_id": repository_id,
            "can_push": can_push,
        })
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        repository_id = d.pop("repository_id")

        can_push = d.pop("can_push")

        _reason = d.pop("reason", UNSET)
        reason: ProjectGitOwnerPushReason | Unset
        if isinstance(_reason,  Unset):
            reason = UNSET
        else:
            reason = check_project_git_owner_push_reason(_reason)




        project_git_owner_push = cls(
            repository_id=repository_id,
            can_push=can_push,
            reason=reason,
        )


        project_git_owner_push.additional_properties = d
        return project_git_owner_push

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
