from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_metrics_group_by import check_project_metrics_group_by
from ..models.project_metrics_group_by import ProjectMetricsGroupBy
from ..models.project_metrics_metric import check_project_metrics_metric
from ..models.project_metrics_metric import ProjectMetricsMetric
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProjectMetricsQuery")



@_attrs_define
class ProjectMetricsQuery:
    """ 
        Attributes:
            id (str):
            metric (ProjectMetricsMetric):
            group_by (ProjectMetricsGroupBy | Unset):
     """

    id: str
    metric: ProjectMetricsMetric
    group_by: ProjectMetricsGroupBy | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        metric: str = self.metric

        group_by: str | Unset = UNSET
        if not isinstance(self.group_by, Unset):
            group_by = self.group_by



        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "metric": metric,
        })
        if group_by is not UNSET:
            field_dict["group_by"] = group_by

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        metric = check_project_metrics_metric(d.pop("metric"))




        _group_by = d.pop("group_by", UNSET)
        group_by: ProjectMetricsGroupBy | Unset
        if isinstance(_group_by,  Unset):
            group_by = UNSET
        else:
            group_by = check_project_metrics_group_by(_group_by)




        project_metrics_query = cls(
            id=id,
            metric=metric,
            group_by=group_by,
        )

        return project_metrics_query

