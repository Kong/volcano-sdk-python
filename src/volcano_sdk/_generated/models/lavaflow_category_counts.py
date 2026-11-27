from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowCategoryCounts")



@_attrs_define
class LavaflowCategoryCounts:
    """ Matching runs in each category, zeros included. `uncategorized` counts runs whose `category` is null.

        Attributes:
            bug (int):
            performance (int):
            security (int):
            improvement (int):
            configuration (int):
            dependency (int):
            external (int):
            uncategorized (int):
     """

    bug: int
    performance: int
    security: int
    improvement: int
    configuration: int
    dependency: int
    external: int
    uncategorized: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        bug = self.bug

        performance = self.performance

        security = self.security

        improvement = self.improvement

        configuration = self.configuration

        dependency = self.dependency

        external = self.external

        uncategorized = self.uncategorized


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "bug": bug,
            "performance": performance,
            "security": security,
            "improvement": improvement,
            "configuration": configuration,
            "dependency": dependency,
            "external": external,
            "uncategorized": uncategorized,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bug = d.pop("bug")

        performance = d.pop("performance")

        security = d.pop("security")

        improvement = d.pop("improvement")

        configuration = d.pop("configuration")

        dependency = d.pop("dependency")

        external = d.pop("external")

        uncategorized = d.pop("uncategorized")

        lavaflow_category_counts = cls(
            bug=bug,
            performance=performance,
            security=security,
            improvement=improvement,
            configuration=configuration,
            dependency=dependency,
            external=external,
            uncategorized=uncategorized,
        )


        lavaflow_category_counts.additional_properties = d
        return lavaflow_category_counts

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
