from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="LavaflowMergePolicy")



@_attrs_define
class LavaflowMergePolicy:
    """ Your rules for fixes LavaFlow must never merge. They apply with `autonomy: merge`; at another autonomy they are
    saved and do nothing.

        Attributes:
            human_review_paths (list[str]): Globs of paths whose change LavaFlow never merges: a fix that changes one is
                held and handed to you. Paths are relative to the repository root, such as `db/migrations/**`. `*` and `?` match
                within one directory, `**/` spans any number of directories, and a final `**` matches the rest. A pattern that
                starts with `/`, `./` or `../`, ends with `/`, holds an empty, `.` or `..` segment, or holds a NUL character
                answers `400`. Volcano's own held paths, such as deploy configuration and authentication code, are always held
                too. Defaults to none.
     """

    human_review_paths: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        human_review_paths = self.human_review_paths




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "human_review_paths": human_review_paths,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        human_review_paths = cast(list[str], d.pop("human_review_paths"))


        lavaflow_merge_policy = cls(
            human_review_paths=human_review_paths,
        )


        lavaflow_merge_policy.additional_properties = d
        return lavaflow_merge_policy

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
