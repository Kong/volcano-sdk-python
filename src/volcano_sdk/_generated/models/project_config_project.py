from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProjectConfigProject")



@_attrs_define
class ProjectConfigProject:
    """ Project-level settings. `name` renames the project.

        Attributes:
            name (str | Unset):
            all_regions (bool | Unset): Region policy. `false` requires `selected_regions` (PRO plan).
            selected_regions (list[str] | Unset): Region subset (bare region names). Requires `all_regions=false`.
     """

    name: str | Unset = UNSET
    all_regions: bool | Unset = UNSET
    selected_regions: list[str] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        all_regions = self.all_regions

        selected_regions: list[str] | Unset = UNSET
        if not isinstance(self.selected_regions, Unset):
            selected_regions = self.selected_regions




        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if all_regions is not UNSET:
            field_dict["all_regions"] = all_regions
        if selected_regions is not UNSET:
            field_dict["selected_regions"] = selected_regions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        all_regions = d.pop("all_regions", UNSET)

        selected_regions = cast(list[str], d.pop("selected_regions", UNSET))


        project_config_project = cls(
            name=name,
            all_regions=all_regions,
            selected_regions=selected_regions,
        )

        return project_config_project

