from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="LavaflowMergePolicyUpdate")



@_attrs_define
class LavaflowMergePolicyUpdate:
    """ The merge policy fields to change. An omitted field keeps its saved value. Send `human_review_paths: []` to clear
    the paths.

        Attributes:
            human_review_paths (list[str] | Unset):
     """

    human_review_paths: list[str] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        human_review_paths: list[str] | Unset = UNSET
        if not isinstance(self.human_review_paths, Unset):
            human_review_paths = self.human_review_paths




        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if human_review_paths is not UNSET:
            field_dict["human_review_paths"] = human_review_paths

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        human_review_paths = cast(list[str], d.pop("human_review_paths", UNSET))


        lavaflow_merge_policy_update = cls(
            human_review_paths=human_review_paths,
        )

        return lavaflow_merge_policy_update

