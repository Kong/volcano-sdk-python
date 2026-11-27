from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowRepositoryExpectation")



@_attrs_define
class LavaflowRepositoryExpectation:
    """ The repository connection the caller expects. This is a save precondition, not an instruction to change the
    connection.

        Attributes:
            repo_id (int):
            repo_installation_id (int):
     """

    repo_id: int
    repo_installation_id: int





    def to_dict(self) -> dict[str, Any]:
        repo_id = self.repo_id

        repo_installation_id = self.repo_installation_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "repo_id": repo_id,
            "repo_installation_id": repo_installation_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        repo_id = d.pop("repo_id")

        repo_installation_id = d.pop("repo_installation_id")

        lavaflow_repository_expectation = cls(
            repo_id=repo_id,
            repo_installation_id=repo_installation_id,
        )

        return lavaflow_repository_expectation

