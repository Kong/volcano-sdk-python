from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_metrics_data_status import check_project_metrics_data_status
from ..models.project_metrics_data_status import ProjectMetricsDataStatus
from ..models.project_metrics_metric import check_project_metrics_metric
from ..models.project_metrics_metric import ProjectMetricsMetric
from ..models.project_metrics_unit import check_project_metrics_unit
from ..models.project_metrics_unit import ProjectMetricsUnit
from typing import cast

if TYPE_CHECKING:
  from ..models.project_metrics_value import ProjectMetricsValue





T = TypeVar("T", bound="ProjectMetricsResult")



@_attrs_define
class ProjectMetricsResult:
    """ 
        Attributes:
            id (str):
            metric (ProjectMetricsMetric):
            unit (ProjectMetricsUnit):
            data_status (ProjectMetricsDataStatus):
            values (list[ProjectMetricsValue]):
     """

    id: str
    metric: ProjectMetricsMetric
    unit: ProjectMetricsUnit
    data_status: ProjectMetricsDataStatus
    values: list[ProjectMetricsValue]





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_metrics_value import ProjectMetricsValue
        id = self.id

        metric: str = self.metric

        unit: str = self.unit

        data_status: str = self.data_status

        values = []
        for values_item_data in self.values:
            values_item = values_item_data.to_dict()
            values.append(values_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "metric": metric,
            "unit": unit,
            "data_status": data_status,
            "values": values,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_metrics_value import ProjectMetricsValue
        d = dict(src_dict)
        id = d.pop("id")

        metric = check_project_metrics_metric(d.pop("metric"))




        unit = check_project_metrics_unit(d.pop("unit"))




        data_status = check_project_metrics_data_status(d.pop("data_status"))




        values = []
        _values = d.pop("values")
        for values_item_data in (_values):
            values_item = ProjectMetricsValue.from_dict(values_item_data)



            values.append(values_item)


        project_metrics_result = cls(
            id=id,
            metric=metric,
            unit=unit,
            data_status=data_status,
            values=values,
        )

        return project_metrics_result

