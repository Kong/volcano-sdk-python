from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="ProjectDeploymentSummary")



@_attrs_define
class ProjectDeploymentSummary:
    """ Aggregate deployment statistics for one resource pipeline.

        Attributes:
            deployment_count (int): All deployment attempts matching the filters.
            successful_count (int): Attempts that reached active or deleted.
            failed_count (int): Attempts that reached failed or degraded.
            canceled_count (int): Superseded attempts, excluded from success rate and duration.
            success_rate (float | None): Successful attempts divided by successful plus failed attempts.
            median_build_duration_seconds (float | None): Median CodeBuild duration across eligible completed attempts.
     """

    deployment_count: int
    successful_count: int
    failed_count: int
    canceled_count: int
    success_rate: float | None
    median_build_duration_seconds: float | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        deployment_count = self.deployment_count

        successful_count = self.successful_count

        failed_count = self.failed_count

        canceled_count = self.canceled_count

        success_rate: float | None
        success_rate = self.success_rate

        median_build_duration_seconds: float | None
        median_build_duration_seconds = self.median_build_duration_seconds


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "deployment_count": deployment_count,
            "successful_count": successful_count,
            "failed_count": failed_count,
            "canceled_count": canceled_count,
            "success_rate": success_rate,
            "median_build_duration_seconds": median_build_duration_seconds,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        deployment_count = d.pop("deployment_count")

        successful_count = d.pop("successful_count")

        failed_count = d.pop("failed_count")

        canceled_count = d.pop("canceled_count")

        def _parse_success_rate(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        success_rate = _parse_success_rate(d.pop("success_rate"))


        def _parse_median_build_duration_seconds(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        median_build_duration_seconds = _parse_median_build_duration_seconds(d.pop("median_build_duration_seconds"))


        project_deployment_summary = cls(
            deployment_count=deployment_count,
            successful_count=successful_count,
            failed_count=failed_count,
            canceled_count=canceled_count,
            success_rate=success_rate,
            median_build_duration_seconds=median_build_duration_seconds,
        )


        project_deployment_summary.additional_properties = d
        return project_deployment_summary

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
