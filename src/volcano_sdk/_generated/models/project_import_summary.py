from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ProjectImportSummary")



@_attrs_define
class ProjectImportSummary:
    """ 
        Attributes:
            automatic (int):
            manual (int):
            deferred (int):
            unsupported (int):
            warnings (int):
            blocking (int):
     """

    automatic: int
    manual: int
    deferred: int
    unsupported: int
    warnings: int
    blocking: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        automatic = self.automatic

        manual = self.manual

        deferred = self.deferred

        unsupported = self.unsupported

        warnings = self.warnings

        blocking = self.blocking


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "automatic": automatic,
            "manual": manual,
            "deferred": deferred,
            "unsupported": unsupported,
            "warnings": warnings,
            "blocking": blocking,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        automatic = d.pop("automatic")

        manual = d.pop("manual")

        deferred = d.pop("deferred")

        unsupported = d.pop("unsupported")

        warnings = d.pop("warnings")

        blocking = d.pop("blocking")

        project_import_summary = cls(
            automatic=automatic,
            manual=manual,
            deferred=deferred,
            unsupported=unsupported,
            warnings=warnings,
            blocking=blocking,
        )


        project_import_summary.additional_properties = d
        return project_import_summary

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
