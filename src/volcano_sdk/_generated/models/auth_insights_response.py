from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.auth_insights_series_point import AuthInsightsSeriesPoint
  from ..models.auth_insights_summary import AuthInsightsSummary
  from ..models.auth_insights_window import AuthInsightsWindow





T = TypeVar("T", bound="AuthInsightsResponse")



@_attrs_define
class AuthInsightsResponse:
    """ 
        Attributes:
            project_id (UUID):
            observed_at (datetime.datetime):
            window (AuthInsightsWindow):
            summary (AuthInsightsSummary):
            series (list[AuthInsightsSeriesPoint]):
     """

    project_id: UUID
    observed_at: datetime.datetime
    window: AuthInsightsWindow
    summary: AuthInsightsSummary
    series: list[AuthInsightsSeriesPoint]





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_insights_series_point import AuthInsightsSeriesPoint
        from ..models.auth_insights_summary import AuthInsightsSummary
        from ..models.auth_insights_window import AuthInsightsWindow
        project_id = str(self.project_id)

        observed_at = self.observed_at.isoformat()

        window = self.window.to_dict()

        summary = self.summary.to_dict()

        series = []
        for series_item_data in self.series:
            series_item = series_item_data.to_dict()
            series.append(series_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "project_id": project_id,
            "observed_at": observed_at,
            "window": window,
            "summary": summary,
            "series": series,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_insights_series_point import AuthInsightsSeriesPoint
        from ..models.auth_insights_summary import AuthInsightsSummary
        from ..models.auth_insights_window import AuthInsightsWindow
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        observed_at = datetime.datetime.fromisoformat(d.pop("observed_at"))




        window = AuthInsightsWindow.from_dict(d.pop("window"))




        summary = AuthInsightsSummary.from_dict(d.pop("summary"))




        series = []
        _series = d.pop("series")
        for series_item_data in (_series):
            series_item = AuthInsightsSeriesPoint.from_dict(series_item_data)



            series.append(series_item)


        auth_insights_response = cls(
            project_id=project_id,
            observed_at=observed_at,
            window=window,
            summary=summary,
            series=series,
        )

        return auth_insights_response

