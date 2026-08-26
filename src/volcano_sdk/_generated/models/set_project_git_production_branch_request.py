from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SetProjectGitProductionBranchRequest")



@_attrs_define
class SetProjectGitProductionBranchRequest:
    """ 
        Attributes:
            production_branch (str): The branch a push must land on to deploy. Validated as a Git branch name only — it does
                not have to exist yet.
     """

    production_branch: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        production_branch = self.production_branch


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "production_branch": production_branch,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        production_branch = d.pop("production_branch")

        set_project_git_production_branch_request = cls(
            production_branch=production_branch,
        )


        set_project_git_production_branch_request.additional_properties = d
        return set_project_git_production_branch_request

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
