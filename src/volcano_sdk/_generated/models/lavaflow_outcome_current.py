from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_outcome_current_scope import check_lavaflow_outcome_current_scope
from ..models.lavaflow_outcome_current_scope import LavaflowOutcomeCurrentScope
from typing import cast






T = TypeVar("T", bound="LavaflowOutcomeCurrent")



@_attrs_define
class LavaflowOutcomeCurrent:
    """ Current known open critical Code Quality findings, including findings without a fix run. The historical window and
    run-category filter do not narrow this inventory. Zero is not an exhaustive security assessment.

        Attributes:
            known_open_critical_count (int):
            scope (LavaflowOutcomeCurrentScope):
            inventory_not_exhaustive (bool):
            category_filter_applied (bool):
     """

    known_open_critical_count: int
    scope: LavaflowOutcomeCurrentScope
    inventory_not_exhaustive: bool
    category_filter_applied: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        known_open_critical_count = self.known_open_critical_count

        scope: str = self.scope

        inventory_not_exhaustive = self.inventory_not_exhaustive

        category_filter_applied = self.category_filter_applied


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "known_open_critical_count": known_open_critical_count,
            "scope": scope,
            "inventory_not_exhaustive": inventory_not_exhaustive,
            "category_filter_applied": category_filter_applied,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        known_open_critical_count = d.pop("known_open_critical_count")

        scope = check_lavaflow_outcome_current_scope(d.pop("scope"))




        inventory_not_exhaustive = d.pop("inventory_not_exhaustive")

        category_filter_applied = d.pop("category_filter_applied")

        lavaflow_outcome_current = cls(
            known_open_critical_count=known_open_critical_count,
            scope=scope,
            inventory_not_exhaustive=inventory_not_exhaustive,
            category_filter_applied=category_filter_applied,
        )


        lavaflow_outcome_current.additional_properties = d
        return lavaflow_outcome_current

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
