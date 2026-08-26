from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.project_metrics_query import ProjectMetricsQuery
  from ..models.project_metrics_query_time_range import ProjectMetricsQueryTimeRange





T = TypeVar("T", bound="ProjectMetricsQueryRequest")



@_attrs_define
class ProjectMetricsQueryRequest:
    """ 
        Attributes:
            time_range (ProjectMetricsQueryTimeRange):
            queries (list[ProjectMetricsQuery]):
     """

    time_range: ProjectMetricsQueryTimeRange
    queries: list[ProjectMetricsQuery]





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_metrics_query import ProjectMetricsQuery
        from ..models.project_metrics_query_time_range import ProjectMetricsQueryTimeRange
        time_range = self.time_range.to_dict()

        queries = []
        for queries_item_data in self.queries:
            queries_item = queries_item_data.to_dict()
            queries.append(queries_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "time_range": time_range,
            "queries": queries,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_metrics_query import ProjectMetricsQuery
        from ..models.project_metrics_query_time_range import ProjectMetricsQueryTimeRange
        d = dict(src_dict)
        time_range = ProjectMetricsQueryTimeRange.from_dict(d.pop("time_range"))




        queries = []
        _queries = d.pop("queries")
        for queries_item_data in (_queries):
            queries_item = ProjectMetricsQuery.from_dict(queries_item_data)



            queries.append(queries_item)


        project_metrics_query_request = cls(
            time_range=time_range,
            queries=queries,
        )

        return project_metrics_query_request

