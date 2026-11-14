from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowStatsTotals")



@_attrs_define
class LavaflowStatsTotals:
    """ 
        Attributes:
            issues_opened (int):
            pull_requests_opened (int):
     """

    issues_opened: int
    pull_requests_opened: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        issues_opened = self.issues_opened

        pull_requests_opened = self.pull_requests_opened


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "issues_opened": issues_opened,
            "pull_requests_opened": pull_requests_opened,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        issues_opened = d.pop("issues_opened")

        pull_requests_opened = d.pop("pull_requests_opened")

        lavaflow_stats_totals = cls(
            issues_opened=issues_opened,
            pull_requests_opened=pull_requests_opened,
        )


        lavaflow_stats_totals.additional_properties = d
        return lavaflow_stats_totals

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
