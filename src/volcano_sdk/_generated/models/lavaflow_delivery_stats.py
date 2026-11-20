from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="LavaflowDeliveryStats")



@_attrs_define
class LavaflowDeliveryStats:
    """ Delivery for retained runs created in the requested UTC window and category, evaluated at as_of.

        Attributes:
            as_of (datetime.datetime):
            runs (int):
            runs_without_owned_pr (int): All runs in the cohort without a pull request of their own, including active,
                stopped, and covered runs.
            finished_without_owned_pr (int): Runs without a pull request of their own that were no longer queued or running
                at as_of.
            issues_with_runs (int): Distinct issues represented by runs in the cohort.
            issues_with_pr_coverage (int): Distinct issues with a pull request on the project's current repository. For
                owned pull requests and verified duplicate-run links, counts open pull requests, merges with a recorded
                deployment, and merges within the past seven days still awaiting deployment. Verified fix-lineage links count
                while their pull request is open or merged.
            time_to_pr_samples (int): Runs with a recorded opening time at or after run creation.
            mean_time_to_pr_seconds (int | None): Mean seconds from run creation to opening its own pull request. Null when
                there are no samples.
            time_to_coverage_samples (int): Runs with a recorded duplicate-PR observation or lineage attribution time at or
                after run creation.
            mean_time_to_coverage_seconds (int | None): Mean seconds from run creation to recorded coverage by another pull
                request. Null when there are no samples.
     """

    as_of: datetime.datetime
    runs: int
    runs_without_owned_pr: int
    finished_without_owned_pr: int
    issues_with_runs: int
    issues_with_pr_coverage: int
    time_to_pr_samples: int
    mean_time_to_pr_seconds: int | None
    time_to_coverage_samples: int
    mean_time_to_coverage_seconds: int | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        as_of = self.as_of.isoformat()

        runs = self.runs

        runs_without_owned_pr = self.runs_without_owned_pr

        finished_without_owned_pr = self.finished_without_owned_pr

        issues_with_runs = self.issues_with_runs

        issues_with_pr_coverage = self.issues_with_pr_coverage

        time_to_pr_samples = self.time_to_pr_samples

        mean_time_to_pr_seconds: int | None
        mean_time_to_pr_seconds = self.mean_time_to_pr_seconds

        time_to_coverage_samples = self.time_to_coverage_samples

        mean_time_to_coverage_seconds: int | None
        mean_time_to_coverage_seconds = self.mean_time_to_coverage_seconds


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "as_of": as_of,
            "runs": runs,
            "runs_without_owned_pr": runs_without_owned_pr,
            "finished_without_owned_pr": finished_without_owned_pr,
            "issues_with_runs": issues_with_runs,
            "issues_with_pr_coverage": issues_with_pr_coverage,
            "time_to_pr_samples": time_to_pr_samples,
            "mean_time_to_pr_seconds": mean_time_to_pr_seconds,
            "time_to_coverage_samples": time_to_coverage_samples,
            "mean_time_to_coverage_seconds": mean_time_to_coverage_seconds,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        as_of = datetime.datetime.fromisoformat(d.pop("as_of"))




        runs = d.pop("runs")

        runs_without_owned_pr = d.pop("runs_without_owned_pr")

        finished_without_owned_pr = d.pop("finished_without_owned_pr")

        issues_with_runs = d.pop("issues_with_runs")

        issues_with_pr_coverage = d.pop("issues_with_pr_coverage")

        time_to_pr_samples = d.pop("time_to_pr_samples")

        def _parse_mean_time_to_pr_seconds(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        mean_time_to_pr_seconds = _parse_mean_time_to_pr_seconds(d.pop("mean_time_to_pr_seconds"))


        time_to_coverage_samples = d.pop("time_to_coverage_samples")

        def _parse_mean_time_to_coverage_seconds(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        mean_time_to_coverage_seconds = _parse_mean_time_to_coverage_seconds(d.pop("mean_time_to_coverage_seconds"))


        lavaflow_delivery_stats = cls(
            as_of=as_of,
            runs=runs,
            runs_without_owned_pr=runs_without_owned_pr,
            finished_without_owned_pr=finished_without_owned_pr,
            issues_with_runs=issues_with_runs,
            issues_with_pr_coverage=issues_with_pr_coverage,
            time_to_pr_samples=time_to_pr_samples,
            mean_time_to_pr_seconds=mean_time_to_pr_seconds,
            time_to_coverage_samples=time_to_coverage_samples,
            mean_time_to_coverage_seconds=mean_time_to_coverage_seconds,
        )


        lavaflow_delivery_stats.additional_properties = d
        return lavaflow_delivery_stats

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
