from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.project_metrics_dimensions import ProjectMetricsDimensions





T = TypeVar("T", bound="ProjectMetricsValue")



@_attrs_define
class ProjectMetricsValue:
    """ 
        Attributes:
            dimensions (ProjectMetricsDimensions):
            value (float):
     """

    dimensions: ProjectMetricsDimensions
    value: float





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_metrics_dimensions import ProjectMetricsDimensions
        dimensions = self.dimensions.to_dict()

        value = self.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "dimensions": dimensions,
            "value": value,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_metrics_dimensions import ProjectMetricsDimensions
        d = dict(src_dict)
        dimensions = ProjectMetricsDimensions.from_dict(d.pop("dimensions"))




        value = d.pop("value")

        project_metrics_value = cls(
            dimensions=dimensions,
            value=value,
        )

        return project_metrics_value

