from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="GitRepository")



@_attrs_define
class GitRepository:
    """ 
        Attributes:
            id (int): Stable GitHub repository id (repository.id), unchanged by renames.
            full_name (str):
            default_branch (str):
            private (bool):
            is_empty (bool): Whether the repository has no commits and can receive an initial source export.
     """

    id: int
    full_name: str
    default_branch: str
    private: bool
    is_empty: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        full_name = self.full_name

        default_branch = self.default_branch

        private = self.private

        is_empty = self.is_empty


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "full_name": full_name,
            "default_branch": default_branch,
            "private": private,
            "is_empty": is_empty,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        full_name = d.pop("full_name")

        default_branch = d.pop("default_branch")

        private = d.pop("private")

        is_empty = d.pop("is_empty")

        git_repository = cls(
            id=id,
            full_name=full_name,
            default_branch=default_branch,
            private=private,
            is_empty=is_empty,
        )


        git_repository.additional_properties = d
        return git_repository

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
