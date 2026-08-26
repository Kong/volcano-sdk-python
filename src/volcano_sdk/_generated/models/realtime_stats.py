from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.realtime_plan_limits import RealtimePlanLimits





T = TypeVar("T", bound="RealtimeStats")



@_attrs_define
class RealtimeStats:
    """ Realtime usage statistics for a project

        Attributes:
            num_connections (int | Unset): Current number of active connections
            peak_connections (int | Unset): Peak concurrent connections this usage period
            last_invoked_at (datetime.datetime | Unset): Most recent realtime activity timestamp across channels
            limits (RealtimePlanLimits | Unset): Plan-based limits for realtime features
     """

    num_connections: int | Unset = UNSET
    peak_connections: int | Unset = UNSET
    last_invoked_at: datetime.datetime | Unset = UNSET
    limits: RealtimePlanLimits | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.realtime_plan_limits import RealtimePlanLimits
        num_connections = self.num_connections

        peak_connections = self.peak_connections

        last_invoked_at: str | Unset = UNSET
        if not isinstance(self.last_invoked_at, Unset):
            last_invoked_at = self.last_invoked_at.isoformat()

        limits: dict[str, Any] | Unset = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if num_connections is not UNSET:
            field_dict["num_connections"] = num_connections
        if peak_connections is not UNSET:
            field_dict["peak_connections"] = peak_connections
        if last_invoked_at is not UNSET:
            field_dict["last_invoked_at"] = last_invoked_at
        if limits is not UNSET:
            field_dict["limits"] = limits

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.realtime_plan_limits import RealtimePlanLimits
        d = dict(src_dict)
        num_connections = d.pop("num_connections", UNSET)

        peak_connections = d.pop("peak_connections", UNSET)

        _last_invoked_at = d.pop("last_invoked_at", UNSET)
        last_invoked_at: datetime.datetime | Unset
        if isinstance(_last_invoked_at,  Unset):
            last_invoked_at = UNSET
        else:
            last_invoked_at = datetime.datetime.fromisoformat(_last_invoked_at)




        _limits = d.pop("limits", UNSET)
        limits: RealtimePlanLimits | Unset
        if isinstance(_limits,  Unset):
            limits = UNSET
        else:
            limits = RealtimePlanLimits.from_dict(_limits)




        realtime_stats = cls(
            num_connections=num_connections,
            peak_connections=peak_connections,
            last_invoked_at=last_invoked_at,
            limits=limits,
        )


        realtime_stats.additional_properties = d
        return realtime_stats

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
