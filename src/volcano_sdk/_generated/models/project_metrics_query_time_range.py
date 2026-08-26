from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_metrics_query_time_range_window import check_project_metrics_query_time_range_window
from ..models.project_metrics_query_time_range_window import ProjectMetricsQueryTimeRangeWindow
from typing import cast






T = TypeVar("T", bound="ProjectMetricsQueryTimeRange")



@_attrs_define
class ProjectMetricsQueryTimeRange:
    """ 
        Attributes:
            window (ProjectMetricsQueryTimeRangeWindow):
     """

    window: ProjectMetricsQueryTimeRangeWindow





    def to_dict(self) -> dict[str, Any]:
        window: str = self.window


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "window": window,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        window = check_project_metrics_query_time_range_window(d.pop("window"))




        project_metrics_query_time_range = cls(
            window=window,
        )

        return project_metrics_query_time_range

