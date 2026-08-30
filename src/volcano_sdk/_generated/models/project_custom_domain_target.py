from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_custom_domain_target_type import check_project_custom_domain_target_type
from ..models.project_custom_domain_target_type import ProjectCustomDomainTargetType
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ProjectCustomDomainTarget")



@_attrs_define
class ProjectCustomDomainTarget:
    """ 
        Attributes:
            type_ (ProjectCustomDomainTargetType):
            id (UUID):
            name (str):
     """

    type_: ProjectCustomDomainTargetType
    id: UUID
    name: str





    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        id = str(self.id)

        name = self.name


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
            "id": id,
            "name": name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_project_custom_domain_target_type(d.pop("type"))




        id = UUID(d.pop("id"))




        name = d.pop("name")

        project_custom_domain_target = cls(
            type_=type_,
            id=id,
            name=name,
        )

        return project_custom_domain_target

