from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="LavaflowOutcomeValues")



@_attrs_define
class LavaflowOutcomeValues:
    """ Exact counts only when collection coverage is complete. Null means unknown, including days with no retained
    observations.

        Attributes:
            pull_requests_merged (int | None):
            improvements_observed_live (int | None):
            issue_resolutions (int | None):
     """

    pull_requests_merged: int | None
    improvements_observed_live: int | None
    issue_resolutions: int | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        pull_requests_merged: int | None
        pull_requests_merged = self.pull_requests_merged

        improvements_observed_live: int | None
        improvements_observed_live = self.improvements_observed_live

        issue_resolutions: int | None
        issue_resolutions = self.issue_resolutions


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
        d = dict(src_dict)
        def _parse_pull_requests_merged(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        pull_requests_merged = _parse_pull_requests_merged(d.pop("pull_requests_merged"))


        def _parse_improvements_observed_live(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        improvements_observed_live = _parse_improvements_observed_live(d.pop("improvements_observed_live"))


        def _parse_issue_resolutions(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        issue_resolutions = _parse_issue_resolutions(d.pop("issue_resolutions"))


        lavaflow_outcome_values = cls(
            pull_requests_merged=pull_requests_merged,
            improvements_observed_live=improvements_observed_live,
            issue_resolutions=issue_resolutions,
        )


        lavaflow_outcome_values.additional_properties = d
        return lavaflow_outcome_values

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
