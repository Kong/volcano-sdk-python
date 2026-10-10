from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="VariableEnvironment")



@_attrs_define
class VariableEnvironment:
    """ Stable identity for a Project-owned variable Environment.

        Attributes:
            id (UUID):
            project_id (UUID):
            name (str):
            is_global (bool): Whether this is the reserved Global Environment.
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
     """

    id: UUID
    project_id: UUID
    name: str
    is_global: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id = str(self.project_id)

        name = self.name

        is_global = self.is_global

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "project_id": project_id,
            "name": name,
            "is_global": is_global,
            "created_at": created_at,
            "updated_at": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        name = d.pop("name")

        is_global = d.pop("is_global")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        variable_environment = cls(
            id=id,
            project_id=project_id,
            name=name,
            is_global=is_global,
            created_at=created_at,
            updated_at=updated_at,
        )


        variable_environment.additional_properties = d
        return variable_environment

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
