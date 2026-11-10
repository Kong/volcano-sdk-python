from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SetProjectGitRootDirectoryRequest")



@_attrs_define
class SetProjectGitRootDirectoryRequest:
    """ 
        Attributes:
            root_directory (str): Monorepo subdirectory the project builds from, relative to the repository root. An empty
                string means the repository root.
     """

    root_directory: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        root_directory = self.root_directory


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "root_directory": root_directory,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        root_directory = d.pop("root_directory")

        set_project_git_root_directory_request = cls(
            root_directory=root_directory,
        )


        set_project_git_root_directory_request.additional_properties = d
        return set_project_git_root_directory_request

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
