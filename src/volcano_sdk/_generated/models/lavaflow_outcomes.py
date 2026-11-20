from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.lavaflow_outcome_counts import LavaflowOutcomeCounts
  from ..models.lavaflow_outcome_current import LavaflowOutcomeCurrent
  from ..models.lavaflow_outcome_day import LavaflowOutcomeDay
  from ..models.lavaflow_outcome_values import LavaflowOutcomeValues
  from ..models.lavaflow_outcomes_coverage import LavaflowOutcomesCoverage





T = TypeVar("T", bound="LavaflowOutcomes")



@_attrs_define
class LavaflowOutcomes:
    """ Separate confirmed merges, live improvements and actual automatic issue-resolution episodes. A live improvement is
    counted once per project, repository and pull request when inclusion is first durably confirmed on a tracked
    function or frontend. Resolution includes automatic open or ignored to resolved transitions, preserves the reason
    and category, and excludes manual actions. The primary issue resolution count includes every category, even when a
    category filter narrows merge and live counts. Only the first qualifying automatic resolution of a metric episode
    contributes a count. Recurrence and manual reopen start new metric episodes without erasing previous resolutions;
    moving resolved to ignored does not start an episode. Existing activity counts remain separate. Older servers omit
    this object; absence is unavailable, never zero.

        Attributes:
            as_of (datetime.datetime): The UTC timestamp of the consistent database snapshot.
            days (list[LavaflowOutcomeDay]): The same ordered UTC date domain as the activity series, with unknown counts
                distinct from zero retained confirmations.
            totals (LavaflowOutcomeValues): Exact counts only when collection coverage is complete. Null means unknown,
                including days with no retained observations.
            confirmed_totals (LavaflowOutcomeCounts): Retained confirmations in the requested interval. These are lower
                bounds when collection coverage is incomplete.
            coverage (LavaflowOutcomesCoverage):
            current (LavaflowOutcomeCurrent): Current known open critical Code Quality findings, including findings without
                a fix run. The historical window and run-category filter do not narrow this inventory. Zero is not an exhaustive
                security assessment.
     """

    as_of: datetime.datetime
    days: list[LavaflowOutcomeDay]
    totals: LavaflowOutcomeValues
    confirmed_totals: LavaflowOutcomeCounts
    coverage: LavaflowOutcomesCoverage
    current: LavaflowOutcomeCurrent
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_outcome_counts import LavaflowOutcomeCounts # noqa: PLC0415
        from ..models.lavaflow_outcome_current import LavaflowOutcomeCurrent # noqa: PLC0415
        from ..models.lavaflow_outcome_day import LavaflowOutcomeDay # noqa: PLC0415
        from ..models.lavaflow_outcome_values import LavaflowOutcomeValues # noqa: PLC0415
        from ..models.lavaflow_outcomes_coverage import LavaflowOutcomesCoverage # noqa: PLC0415
        as_of = self.as_of.isoformat()

        days = []
        for days_item_data in self.days:
            days_item = days_item_data.to_dict()
            days.append(days_item)



        totals = self.totals.to_dict()

        confirmed_totals = self.confirmed_totals.to_dict()

        coverage = self.coverage.to_dict()

        current = self.current.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "as_of": as_of,
            "days": days,
            "totals": totals,
            "confirmed_totals": confirmed_totals,
            "coverage": coverage,
            "current": current,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_outcome_counts import LavaflowOutcomeCounts # noqa: PLC0415
        from ..models.lavaflow_outcome_current import LavaflowOutcomeCurrent # noqa: PLC0415
        from ..models.lavaflow_outcome_day import LavaflowOutcomeDay # noqa: PLC0415
        from ..models.lavaflow_outcome_values import LavaflowOutcomeValues # noqa: PLC0415
        from ..models.lavaflow_outcomes_coverage import LavaflowOutcomesCoverage # noqa: PLC0415
        d = dict(src_dict)
        as_of = datetime.datetime.fromisoformat(d.pop("as_of"))




        days = []
        _days = d.pop("days")
        for days_item_data in (_days):
            days_item = LavaflowOutcomeDay.from_dict(days_item_data)



            days.append(days_item)


        totals = LavaflowOutcomeValues.from_dict(d.pop("totals"))




        confirmed_totals = LavaflowOutcomeCounts.from_dict(d.pop("confirmed_totals"))




        coverage = LavaflowOutcomesCoverage.from_dict(d.pop("coverage"))




        current = LavaflowOutcomeCurrent.from_dict(d.pop("current"))




        lavaflow_outcomes = cls(
            as_of=as_of,
            days=days,
            totals=totals,
            confirmed_totals=confirmed_totals,
            coverage=coverage,
            current=current,
        )


        lavaflow_outcomes.additional_properties = d
        return lavaflow_outcomes

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
