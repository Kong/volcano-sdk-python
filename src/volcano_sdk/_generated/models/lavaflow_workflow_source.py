from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowWorkflowSource")



@_attrs_define
class LavaflowWorkflowSource:
    """ A branch or commit whose workflows LavaFlow read, and the commit it read them at.

        Attributes:
            source (str): The branch, or the commit SHA for a commit. Example: main.
            commit_sha (str): The commit LavaFlow read the workflows at. Example: 3f786850e387550fdab836ed7e6dc881de23001b.
     """

    source: str
    commit_sha: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        source = self.source

        commit_sha = self.commit_sha


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "source": source,
            "commit_sha": commit_sha,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = d.pop("source")

        commit_sha = d.pop("commit_sha")

        lavaflow_workflow_source = cls(
            source=source,
            commit_sha=commit_sha,
        )


        lavaflow_workflow_source.additional_properties = d
        return lavaflow_workflow_source

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
