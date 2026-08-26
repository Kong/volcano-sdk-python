from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_metrics_dimensions_resource_type import check_project_metrics_dimensions_resource_type
from ..models.project_metrics_dimensions_resource_type import ProjectMetricsDimensionsResourceType
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProjectMetricsDimensions")



@_attrs_define
class ProjectMetricsDimensions:
    """ 
        Attributes:
            region (str | Unset):
            resource_type (ProjectMetricsDimensionsResourceType | Unset):
     """

    region: str | Unset = UNSET
    resource_type: ProjectMetricsDimensionsResourceType | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        region = self.region

        resource_type: str | Unset = UNSET
        if not isinstance(self.resource_type, Unset):
            resource_type = self.resource_type



        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if region is not UNSET:
            field_dict["region"] = region
        if resource_type is not UNSET:
            field_dict["resource_type"] = resource_type

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        region = d.pop("region", UNSET)

        _resource_type = d.pop("resource_type", UNSET)
        resource_type: ProjectMetricsDimensionsResourceType | Unset
        if isinstance(_resource_type,  Unset):
            resource_type = UNSET
        else:
            resource_type = check_project_metrics_dimensions_resource_type(_resource_type)




        project_metrics_dimensions = cls(
            region=region,
            resource_type=resource_type,
        )

        return project_metrics_dimensions

