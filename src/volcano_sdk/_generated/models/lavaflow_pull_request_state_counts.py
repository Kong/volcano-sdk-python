from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowPullRequestStateCounts")



@_attrs_define
class LavaflowPullRequestStateCounts:
    """ Matching runs by the state of their pull request, zeros included. `none` counts runs without one.

        Attributes:
            open_ (int):
            merged (int):
            closed (int):
            none (int):
     """

    open_: int
    merged: int
    closed: int
    none: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        open_ = self.open_

        merged = self.merged

        closed = self.closed

        none = self.none


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "open": open_,
            "merged": merged,
            "closed": closed,
            "none": none,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        open_ = d.pop("open")

        merged = d.pop("merged")

        closed = d.pop("closed")

        none = d.pop("none")

        lavaflow_pull_request_state_counts = cls(
            open_=open_,
            merged=merged,
            closed=closed,
            none=none,
        )


        lavaflow_pull_request_state_counts.additional_properties = d
        return lavaflow_pull_request_state_counts

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
