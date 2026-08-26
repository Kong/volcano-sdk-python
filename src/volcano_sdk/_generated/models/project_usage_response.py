from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.frontend_usage_data import FrontendUsageData
  from ..models.metric_usage_data import MetricUsageData





T = TypeVar("T", bound="ProjectUsageResponse")



@_attrs_define
class ProjectUsageResponse:
    """ Aggregated usage metrics for a project.

        Attributes:
            project_id (UUID): Project ID
            month (str): Usage month in YYYY-MM format Example: 2026-02.
            metrics (list[MetricUsageData]): Usage metrics for the project
            frontends (list[FrontendUsageData] | Unset): Per-frontend request totals for the current usage month
     """

    project_id: UUID
    month: str
    metrics: list[MetricUsageData]
    frontends: list[FrontendUsageData] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.frontend_usage_data import FrontendUsageData
        from ..models.metric_usage_data import MetricUsageData
        project_id = str(self.project_id)

        month = self.month

        metrics = []
        for metrics_item_data in self.metrics:
            metrics_item = metrics_item_data.to_dict()
            metrics.append(metrics_item)



        frontends: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.frontends, Unset):
            frontends = []
            for frontends_item_data in self.frontends:
                frontends_item = frontends_item_data.to_dict()
                frontends.append(frontends_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "project_id": project_id,
            "month": month,
            "metrics": metrics,
        })
        if frontends is not UNSET:
            field_dict["frontends"] = frontends

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.frontend_usage_data import FrontendUsageData
        from ..models.metric_usage_data import MetricUsageData
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        month = d.pop("month")

        metrics = []
        _metrics = d.pop("metrics")
        for metrics_item_data in (_metrics):
            metrics_item = MetricUsageData.from_dict(metrics_item_data)



            metrics.append(metrics_item)


        _frontends = d.pop("frontends", UNSET)
        frontends: list[FrontendUsageData] | Unset = UNSET
        if _frontends is not UNSET:
            frontends = []
            for frontends_item_data in _frontends:
                frontends_item = FrontendUsageData.from_dict(frontends_item_data)



                frontends.append(frontends_item)


        project_usage_response = cls(
            project_id=project_id,
            month=month,
            metrics=metrics,
            frontends=frontends,
        )


        project_usage_response.additional_properties = d
        return project_usage_response

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
