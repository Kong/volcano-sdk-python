from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.lavaflow_outcome_coverage import LavaflowOutcomeCoverage





T = TypeVar("T", bound="LavaflowOutcomesCoverage")



@_attrs_define
class LavaflowOutcomesCoverage:
    """ 
        Attributes:
            pull_requests_merged (LavaflowOutcomeCoverage): Collection coverage for one metric. A migration or the earliest
                retained event establishes no complete interval. Undated observations are not assigned to the requested dates or
                totals.
            improvements_observed_live (LavaflowOutcomeCoverage): Collection coverage for one metric. A migration or the
                earliest retained event establishes no complete interval. Undated observations are not assigned to the requested
                dates or totals.
            issue_resolutions (LavaflowOutcomeCoverage): Collection coverage for one metric. A migration or the earliest
                retained event establishes no complete interval. Undated observations are not assigned to the requested dates or
                totals.
     """

    pull_requests_merged: LavaflowOutcomeCoverage
    improvements_observed_live: LavaflowOutcomeCoverage
    issue_resolutions: LavaflowOutcomeCoverage
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_outcome_coverage import LavaflowOutcomeCoverage # noqa: PLC0415
        pull_requests_merged = self.pull_requests_merged.to_dict()

        improvements_observed_live = self.improvements_observed_live.to_dict()

        issue_resolutions = self.issue_resolutions.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "pull_requests_merged": pull_requests_merged,
            "improvements_observed_live": improvements_observed_live,
            "issue_resolutions": issue_resolutions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_outcome_coverage import LavaflowOutcomeCoverage # noqa: PLC0415
        d = dict(src_dict)
        pull_requests_merged = LavaflowOutcomeCoverage.from_dict(d.pop("pull_requests_merged"))




        improvements_observed_live = LavaflowOutcomeCoverage.from_dict(d.pop("improvements_observed_live"))




        issue_resolutions = LavaflowOutcomeCoverage.from_dict(d.pop("issue_resolutions"))




        lavaflow_outcomes_coverage = cls(
            pull_requests_merged=pull_requests_merged,
            improvements_observed_live=improvements_observed_live,
            issue_resolutions=issue_resolutions,
        )


        lavaflow_outcomes_coverage.additional_properties = d
        return lavaflow_outcomes_coverage

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
