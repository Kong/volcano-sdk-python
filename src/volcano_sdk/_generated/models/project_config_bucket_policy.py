from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_config_bucket_policy_operation import check_project_config_bucket_policy_operation
from ..models.project_config_bucket_policy_operation import ProjectConfigBucketPolicyOperation
from typing import cast






T = TypeVar("T", bound="ProjectConfigBucketPolicy")



@_attrs_define
class ProjectConfigBucketPolicy:
    """ 
        Attributes:
            name (str):
            operation (ProjectConfigBucketPolicyOperation):
            definition (str): Policy expression
     """

    name: str
    operation: ProjectConfigBucketPolicyOperation
    definition: str





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        operation: str = self.operation

        definition = self.definition


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
            "operation": operation,
            "definition": definition,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        operation = check_project_config_bucket_policy_operation(d.pop("operation"))




        definition = d.pop("definition")

        project_config_bucket_policy = cls(
            name=name,
            operation=operation,
            definition=definition,
        )

        return project_config_bucket_policy

