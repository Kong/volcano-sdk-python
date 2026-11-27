from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_commit_origin import check_lavaflow_commit_origin
from ..models.lavaflow_commit_origin import LavaflowCommitOrigin
from typing import cast






T = TypeVar("T", bound="LavaflowSourceCommit")



@_attrs_define
class LavaflowSourceCommit:
    """ The commit a run read its source at.

        Attributes:
            sha (str): The commit's full SHA.
            origin (LavaflowCommitOrigin | None): Where the commit came from. Null for a run recorded before Volcano kept
                it.
     """

    sha: str
    origin: LavaflowCommitOrigin | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        sha = self.sha

        origin: None | str
        if isinstance(self.origin, str):
            origin = self.origin
        else:
            origin = self.origin


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "sha": sha,
            "origin": origin,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sha = d.pop("sha")

        def _parse_origin(data: object) -> LavaflowCommitOrigin | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                origin_type_1 = check_lavaflow_commit_origin(data)



                return origin_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowCommitOrigin | None, data)

        origin = _parse_origin(d.pop("origin"))


        lavaflow_source_commit = cls(
            sha=sha,
            origin=origin,
        )


        lavaflow_source_commit.additional_properties = d
        return lavaflow_source_commit

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
