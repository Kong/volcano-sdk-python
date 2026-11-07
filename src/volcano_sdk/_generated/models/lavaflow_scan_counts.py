from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowScanCounts")



@_attrs_define
class LavaflowScanCounts:
    """ What the scan did with the problems it found.

        Attributes:
            found (int): Candidates the scan found in the changed lines.
            created (int): New issues the scan opened.
            duplicate (int): Candidates that matched an issue the project already has, or a finding the scan already kept.
            suppressed (int): Candidates a person had already turned down, by closing their pull request or ignoring their
                issue.
            capped (int): Confirmed findings past the plan's findings per scan, which no later scan reports again.
            rejected (int): Candidates LavaFlow's second check didn't confirm, or that it couldn't report.
     """

    found: int
    created: int
    duplicate: int
    suppressed: int
    capped: int
    rejected: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        found = self.found

        created = self.created

        duplicate = self.duplicate

        suppressed = self.suppressed

        capped = self.capped

        rejected = self.rejected


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "found": found,
            "created": created,
            "duplicate": duplicate,
            "suppressed": suppressed,
            "capped": capped,
            "rejected": rejected,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        found = d.pop("found")

        created = d.pop("created")

        duplicate = d.pop("duplicate")

        suppressed = d.pop("suppressed")

        capped = d.pop("capped")

        rejected = d.pop("rejected")

        lavaflow_scan_counts = cls(
            found=found,
            created=created,
            duplicate=duplicate,
            suppressed=suppressed,
            capped=capped,
            rejected=rejected,
        )


        lavaflow_scan_counts.additional_properties = d
        return lavaflow_scan_counts

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
