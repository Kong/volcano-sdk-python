from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.project_metrics_result import ProjectMetricsResult
  from ..models.project_metrics_window import ProjectMetricsWindow





T = TypeVar("T", bound="ProjectMetricsQueryResponse")



@_attrs_define
class ProjectMetricsQueryResponse:
    """ 
        Attributes:
            observed_at (datetime.datetime):
            window (ProjectMetricsWindow):
            results (list[ProjectMetricsResult]):
            fresh_through (datetime.datetime | Unset):
     """

    observed_at: datetime.datetime
    window: ProjectMetricsWindow
    results: list[ProjectMetricsResult]
    fresh_through: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_metrics_result import ProjectMetricsResult
        from ..models.project_metrics_window import ProjectMetricsWindow
        observed_at = self.observed_at.isoformat()

        window = self.window.to_dict()

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)



        fresh_through: str | Unset = UNSET
        if not isinstance(self.fresh_through, Unset):
            fresh_through = self.fresh_through.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "observed_at": observed_at,
            "window": window,
            "results": results,
        })
        if fresh_through is not UNSET:
            field_dict["fresh_through"] = fresh_through

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_metrics_result import ProjectMetricsResult
        from ..models.project_metrics_window import ProjectMetricsWindow
        d = dict(src_dict)
        observed_at = datetime.datetime.fromisoformat(d.pop("observed_at"))




        window = ProjectMetricsWindow.from_dict(d.pop("window"))




        results = []
        _results = d.pop("results")
        for results_item_data in (_results):
            results_item = ProjectMetricsResult.from_dict(results_item_data)



            results.append(results_item)


        _fresh_through = d.pop("fresh_through", UNSET)
        fresh_through: datetime.datetime | Unset
        if isinstance(_fresh_through,  Unset):
            fresh_through = UNSET
        else:
            fresh_through = datetime.datetime.fromisoformat(_fresh_through)




        project_metrics_query_response = cls(
            observed_at=observed_at,
            window=window,
            results=results,
            fresh_through=fresh_through,
        )

        return project_metrics_query_response

