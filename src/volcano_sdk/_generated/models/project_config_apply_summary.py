from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ProjectConfigApplySummary")



@_attrs_define
class ProjectConfigApplySummary:
    """ 
        Attributes:
            created (int):
            updated (int):
            deleted (int):
            unchanged (int):
            errors (int):
            skipped (int):
            missing (int):
     """

    created: int
    updated: int
    deleted: int
    unchanged: int
    errors: int
    skipped: int
    missing: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        created = self.created

        updated = self.updated

        deleted = self.deleted

        unchanged = self.unchanged

        errors = self.errors

        skipped = self.skipped

        missing = self.missing


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created": created,
            "updated": updated,
            "deleted": deleted,
            "unchanged": unchanged,
            "errors": errors,
            "skipped": skipped,
            "missing": missing,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created = d.pop("created")

        updated = d.pop("updated")

        deleted = d.pop("deleted")

        unchanged = d.pop("unchanged")

        errors = d.pop("errors")

        skipped = d.pop("skipped")

        missing = d.pop("missing")

        project_config_apply_summary = cls(
            created=created,
            updated=updated,
            deleted=deleted,
            unchanged=unchanged,
            errors=errors,
            skipped=skipped,
            missing=missing,
        )


        project_config_apply_summary.additional_properties = d
        return project_config_apply_summary

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
