from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.function_kind import check_function_kind
from ..models.function_kind import FunctionKind
from ..models.project_deployment_resource_type import check_project_deployment_resource_type
from ..models.project_deployment_resource_type import ProjectDeploymentResourceType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ProjectDeploymentResource")



@_attrs_define
class ProjectDeploymentResource:
    """ The resource this deployment belongs to.

        Attributes:
            type_ (ProjectDeploymentResourceType):
            id (UUID):
            name (str):
            kind (FunctionKind | Unset): Which kind of function this is. `standard` runs once per invocation.
                `durable` checkpoints its progress and resumes from the last completed
                step, and is invoked asynchronously through its own executions
                collection. A function's kind is fixed when it is created and cannot be
                changed afterwards. Omitting this field means `standard`.
     """

    type_: ProjectDeploymentResourceType
    id: UUID
    name: str
    kind: FunctionKind | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        id = str(self.id)

        name = self.name

        kind: str | Unset = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "id": id,
            "name": name,
        })
        if kind is not UNSET:
            field_dict["kind"] = kind

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_project_deployment_resource_type(d.pop("type"))




        id = UUID(d.pop("id"))




        name = d.pop("name")

        _kind = d.pop("kind", UNSET)
        kind: FunctionKind | Unset
        if isinstance(_kind,  Unset):
            kind = UNSET
        else:
            kind = check_function_kind(_kind)




        project_deployment_resource = cls(
            type_=type_,
            id=id,
            name=name,
            kind=kind,
        )


        project_deployment_resource.additional_properties = d
        return project_deployment_resource

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
