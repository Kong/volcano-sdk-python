from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_config_bucket_policy import ProjectConfigBucketPolicy





T = TypeVar("T", bound="ProjectConfigBucket")



@_attrs_define
class ProjectConfigBucket:
    """ Settings for an existing storage bucket. Buckets are never created or
    deleted through the manifest. When `policies` is declared it is fully
    synced (policies absent from the list are deleted; an empty list
    deletes all); omitting `policies` leaves the bucket's policies
    untouched.

        Attributes:
            name (str):
            file_size_limit (int | Unset): Maximum file size in bytes
            allowed_mime_types (list[str] | Unset):
            policies (list[ProjectConfigBucketPolicy] | Unset):
     """

    name: str
    file_size_limit: int | Unset = UNSET
    allowed_mime_types: list[str] | Unset = UNSET
    policies: list[ProjectConfigBucketPolicy] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_bucket_policy import ProjectConfigBucketPolicy
        name = self.name

        file_size_limit = self.file_size_limit

        allowed_mime_types: list[str] | Unset = UNSET
        if not isinstance(self.allowed_mime_types, Unset):
            allowed_mime_types = self.allowed_mime_types



        policies: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.policies, Unset):
            policies = []
            for policies_item_data in self.policies:
                policies_item = policies_item_data.to_dict()
                policies.append(policies_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
        })
        if file_size_limit is not UNSET:
            field_dict["file_size_limit"] = file_size_limit
        if allowed_mime_types is not UNSET:
            field_dict["allowed_mime_types"] = allowed_mime_types
        if policies is not UNSET:
            field_dict["policies"] = policies

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_bucket_policy import ProjectConfigBucketPolicy
        d = dict(src_dict)
        name = d.pop("name")

        file_size_limit = d.pop("file_size_limit", UNSET)

        allowed_mime_types = cast(list[str], d.pop("allowed_mime_types", UNSET))


        _policies = d.pop("policies", UNSET)
        policies: list[ProjectConfigBucketPolicy] | Unset = UNSET
        if _policies is not UNSET:
            policies = []
            for policies_item_data in _policies:
                policies_item = ProjectConfigBucketPolicy.from_dict(policies_item_data)



                policies.append(policies_item)


        project_config_bucket = cls(
            name=name,
            file_size_limit=file_size_limit,
            allowed_mime_types=allowed_mime_types,
            policies=policies,
        )

        return project_config_bucket

