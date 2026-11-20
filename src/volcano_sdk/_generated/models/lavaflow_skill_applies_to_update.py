from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="LavaflowSkillAppliesToUpdate")



@_attrs_define
class LavaflowSkillAppliesToUpdate:
    """ The members of `applies_to` to change. An omitted member keeps its value, and a list you send replaces it, so `[]`
    clears it.

        Attributes:
            resource_ids (list[UUID] | Unset): Functions, durable functions and frontends it applies to.
            paths (list[str] | Unset): Repository path globs it applies to, relative to the repository root.
     """

    resource_ids: list[UUID] | Unset = UNSET
    paths: list[str] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        resource_ids: list[str] | Unset = UNSET
        if not isinstance(self.resource_ids, Unset):
            resource_ids = []
            for resource_ids_item_data in self.resource_ids:
                resource_ids_item = str(resource_ids_item_data)
                resource_ids.append(resource_ids_item)



        paths: list[str] | Unset = UNSET
        if not isinstance(self.paths, Unset):
            paths = self.paths




        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if resource_ids is not UNSET:
            field_dict["resource_ids"] = resource_ids
        if paths is not UNSET:
            field_dict["paths"] = paths

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _resource_ids = d.pop("resource_ids", UNSET)
        resource_ids: list[UUID] | Unset = UNSET
        if _resource_ids is not UNSET:
            resource_ids = []
            for resource_ids_item_data in _resource_ids:
                resource_ids_item = UUID(resource_ids_item_data)



                resource_ids.append(resource_ids_item)


        paths = cast(list[str], d.pop("paths", UNSET))


        lavaflow_skill_applies_to_update = cls(
            resource_ids=resource_ids,
            paths=paths,
        )

        return lavaflow_skill_applies_to_update

