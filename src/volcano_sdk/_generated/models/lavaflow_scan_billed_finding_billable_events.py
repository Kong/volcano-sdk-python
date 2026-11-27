from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowScanBilledFindingBillableEvents")



@_attrs_define
class LavaflowScanBilledFindingBillableEvents:
    """ How many billable events of each kind the finding's runs recorded, keyed by kind, such as `issue_diagnosed` and
    `pull_request_opened`.

     """

    additional_properties: dict[str, int] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        lavaflow_scan_billed_finding_billable_events = cls(
        )


        lavaflow_scan_billed_finding_billable_events.additional_properties = d
        return lavaflow_scan_billed_finding_billable_events

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> int:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: int) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
