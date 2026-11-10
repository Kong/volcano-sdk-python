from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_fix_outcome_state import check_lavaflow_fix_outcome_state
from ..models.lavaflow_fix_outcome_state import LavaflowFixOutcomeState
from typing import cast
import datetime






T = TypeVar("T", bound="LavaflowFixOutcome")



@_attrs_define
class LavaflowFixOutcome:
    """ How a merged LavaFlow fix fared once it went live.

        Attributes:
            state (LavaflowFixOutcomeState): `watching` for 14 days after the fix goes live, then `effective` unless its
                issue came back (`ineffective`) or a new issue was traced to its deploy (`regressed`). An outcome never moves
                back. `reverted` is reserved and not produced yet.
            live_at (datetime.datetime | None):
            watch_until (datetime.datetime | None):
            follow_ups (int): Runs linked to this fix.
     """

    state: LavaflowFixOutcomeState
    live_at: datetime.datetime | None
    watch_until: datetime.datetime | None
    follow_ups: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        state: str = self.state

        live_at: None | str
        if isinstance(self.live_at, datetime.datetime):
            live_at = self.live_at.isoformat()
        else:
            live_at = self.live_at

        watch_until: None | str
        if isinstance(self.watch_until, datetime.datetime):
            watch_until = self.watch_until.isoformat()
        else:
            watch_until = self.watch_until

        follow_ups = self.follow_ups


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "state": state,
            "live_at": live_at,
            "watch_until": watch_until,
            "follow_ups": follow_ups,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = check_lavaflow_fix_outcome_state(d.pop("state"))




        def _parse_live_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                live_at_type_0 = datetime.datetime.fromisoformat(data)



                return live_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        live_at = _parse_live_at(d.pop("live_at"))


        def _parse_watch_until(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                watch_until_type_0 = datetime.datetime.fromisoformat(data)



                return watch_until_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        watch_until = _parse_watch_until(d.pop("watch_until"))


        follow_ups = d.pop("follow_ups")

        lavaflow_fix_outcome = cls(
            state=state,
            live_at=live_at,
            watch_until=watch_until,
            follow_ups=follow_ups,
        )


        lavaflow_fix_outcome.additional_properties = d
        return lavaflow_fix_outcome

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
