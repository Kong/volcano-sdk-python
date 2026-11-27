from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_outcome_coverage_event_time_basis import check_lavaflow_outcome_coverage_event_time_basis
from ..models.lavaflow_outcome_coverage_event_time_basis import LavaflowOutcomeCoverageEventTimeBasis
from ..models.lavaflow_outcome_coverage_status import check_lavaflow_outcome_coverage_status
from ..models.lavaflow_outcome_coverage_status import LavaflowOutcomeCoverageStatus
from typing import cast
import datetime






T = TypeVar("T", bound="LavaflowOutcomeCoverage")



@_attrs_define
class LavaflowOutcomeCoverage:
    """ Collection coverage for one metric. A migration or the earliest retained event establishes no complete interval.
    Undated observations are not assigned to the requested dates or totals.

        Attributes:
            status (LavaflowOutcomeCoverageStatus):
            complete_from (datetime.datetime | None):
            complete_through (datetime.datetime | None):
            reason (str):
            event_time_basis (LavaflowOutcomeCoverageEventTimeBasis):
            supported_sources (list[str]):
            undated_confirmed_events (int):
     """

    status: LavaflowOutcomeCoverageStatus
    complete_from: datetime.datetime | None
    complete_through: datetime.datetime | None
    reason: str
    event_time_basis: LavaflowOutcomeCoverageEventTimeBasis
    supported_sources: list[str]
    undated_confirmed_events: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        status: str = self.status

        complete_from: None | str
        if isinstance(self.complete_from, datetime.datetime):
            complete_from = self.complete_from.isoformat()
        else:
            complete_from = self.complete_from

        complete_through: None | str
        if isinstance(self.complete_through, datetime.datetime):
            complete_through = self.complete_through.isoformat()
        else:
            complete_through = self.complete_through

        reason = self.reason

        event_time_basis: str = self.event_time_basis

        supported_sources = self.supported_sources



        undated_confirmed_events = self.undated_confirmed_events


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "status": status,
            "complete_from": complete_from,
            "complete_through": complete_through,
            "reason": reason,
            "event_time_basis": event_time_basis,
            "supported_sources": supported_sources,
            "undated_confirmed_events": undated_confirmed_events,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = check_lavaflow_outcome_coverage_status(d.pop("status"))




        def _parse_complete_from(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                complete_from_type_0 = datetime.datetime.fromisoformat(data)



                return complete_from_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        complete_from = _parse_complete_from(d.pop("complete_from"))


        def _parse_complete_through(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                complete_through_type_0 = datetime.datetime.fromisoformat(data)



                return complete_through_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        complete_through = _parse_complete_through(d.pop("complete_through"))


        reason = d.pop("reason")

        event_time_basis = check_lavaflow_outcome_coverage_event_time_basis(d.pop("event_time_basis"))




        supported_sources = cast(list[str], d.pop("supported_sources"))


        undated_confirmed_events = d.pop("undated_confirmed_events")

        lavaflow_outcome_coverage = cls(
            status=status,
            complete_from=complete_from,
            complete_through=complete_through,
            reason=reason,
            event_time_basis=event_time_basis,
            supported_sources=supported_sources,
            undated_confirmed_events=undated_confirmed_events,
        )


        lavaflow_outcome_coverage.additional_properties = d
        return lavaflow_outcome_coverage

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
