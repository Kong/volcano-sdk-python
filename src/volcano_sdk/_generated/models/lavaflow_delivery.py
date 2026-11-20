from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_delivery_state import check_lavaflow_delivery_state
from ..models.lavaflow_delivery_state import LavaflowDeliveryState
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.lavaflow_delivery_coverage import LavaflowDeliveryCoverage
  from ..models.lavaflow_delivery_skip import LavaflowDeliverySkip





T = TypeVar("T", bound="LavaflowDelivery")



@_attrs_define
class LavaflowDelivery:
    """ Pull request delivery recorded independently of run execution and live recovery.

        Attributes:
            state (LavaflowDeliveryState): Where pull request delivery stands. `pending` means LavaFlow is still working.
                `pr_created` includes drafts. `covered` means another run owns the verified pull request.
                `waiting_for_prerequisite` means delivery can resume on this run. `terminal_miss` means this run ended without
                delivery and can include guidance for future work. `stopped` includes runs deliberately limited to diagnosis.
            recorded_at (datetime.datetime | None): When the current delivery result was recorded, if known.
            prior_skips (list[LavaflowDeliverySkip]): Reasons recorded before the run resumed, in order.
            reason (str | Unset): Recorded skip or failure code, `no_recorded_pr` if none was recorded, or
                `external_prerequisite` for an open proposal that still needs external action. New codes may appear.
            next_action (str | Unset): Action to resume delivery, address an undelivered issue, or complete the setup for a
                draft proposal, when known.
            coverage (LavaflowDeliveryCoverage | Unset): Another run's verified covering pull request. That run owns the
                pull request.
     """

    state: LavaflowDeliveryState
    recorded_at: datetime.datetime | None
    prior_skips: list[LavaflowDeliverySkip]
    reason: str | Unset = UNSET
    next_action: str | Unset = UNSET
    coverage: LavaflowDeliveryCoverage | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_delivery_coverage import LavaflowDeliveryCoverage # noqa: PLC0415
        from ..models.lavaflow_delivery_skip import LavaflowDeliverySkip # noqa: PLC0415
        state: str = self.state

        recorded_at: None | str
        if isinstance(self.recorded_at, datetime.datetime):
            recorded_at = self.recorded_at.isoformat()
        else:
            recorded_at = self.recorded_at

        prior_skips = []
        for prior_skips_item_data in self.prior_skips:
            prior_skips_item = prior_skips_item_data.to_dict()
            prior_skips.append(prior_skips_item)



        reason = self.reason

        next_action = self.next_action

        coverage: dict[str, Any] | Unset = UNSET
        if not isinstance(self.coverage, Unset):
            coverage = self.coverage.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "state": state,
            "recorded_at": recorded_at,
            "prior_skips": prior_skips,
        })
        if reason is not UNSET:
            field_dict["reason"] = reason
        if next_action is not UNSET:
            field_dict["next_action"] = next_action
        if coverage is not UNSET:
            field_dict["coverage"] = coverage

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_delivery_coverage import LavaflowDeliveryCoverage # noqa: PLC0415
        from ..models.lavaflow_delivery_skip import LavaflowDeliverySkip # noqa: PLC0415
        d = dict(src_dict)
        state = check_lavaflow_delivery_state(d.pop("state"))




        def _parse_recorded_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                recorded_at_type_0 = datetime.datetime.fromisoformat(data)



                return recorded_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        recorded_at = _parse_recorded_at(d.pop("recorded_at"))


        prior_skips = []
        _prior_skips = d.pop("prior_skips")
        for prior_skips_item_data in (_prior_skips):
            prior_skips_item = LavaflowDeliverySkip.from_dict(prior_skips_item_data)



            prior_skips.append(prior_skips_item)


        reason = d.pop("reason", UNSET)

        next_action = d.pop("next_action", UNSET)

        _coverage = d.pop("coverage", UNSET)
        coverage: LavaflowDeliveryCoverage | Unset
        if isinstance(_coverage,  Unset):
            coverage = UNSET
        else:
            coverage = LavaflowDeliveryCoverage.from_dict(_coverage)




        lavaflow_delivery = cls(
            state=state,
            recorded_at=recorded_at,
            prior_skips=prior_skips,
            reason=reason,
            next_action=next_action,
            coverage=coverage,
        )


        lavaflow_delivery.additional_properties = d
        return lavaflow_delivery

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
