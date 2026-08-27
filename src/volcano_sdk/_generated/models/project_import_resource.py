from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_import_resource_kind import check_project_import_resource_kind
from ..models.project_import_resource_kind import ProjectImportResourceKind
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProjectImportResource")



@_attrs_define
class ProjectImportResource:
    """ 
        Attributes:
            kind (ProjectImportResourceKind):
            name (str):
            source_id (str | Unset): Stable provider identifier for a scoped source resource.
            scope (str | Unset): URL-encoded source scope, including target, branch, and custom environment identifiers.
     """

    kind: ProjectImportResourceKind
    name: str
    source_id: str | Unset = UNSET
    scope: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        name = self.name

        source_id = self.source_id

        scope = self.scope


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "kind": kind,
            "name": name,
        })
        if source_id is not UNSET:
            field_dict["source_id"] = source_id
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_project_import_resource_kind(d.pop("kind"))




        name = d.pop("name")

        source_id = d.pop("source_id", UNSET)

        scope = d.pop("scope", UNSET)

        project_import_resource = cls(
            kind=kind,
            name=name,
            source_id=source_id,
            scope=scope,
        )


        project_import_resource.additional_properties = d
        return project_import_resource

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
