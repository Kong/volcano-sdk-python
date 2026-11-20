from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.scheduler_failure_notify_on import check_scheduler_failure_notify_on
from ..models.scheduler_failure_notify_on import SchedulerFailureNotifyOn
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="UpdateSchedulerFailureAlertPolicy")



@_attrs_define
class UpdateSchedulerFailureAlertPolicy:
    """ 
        Attributes:
            notify_on (SchedulerFailureNotifyOn | Unset): When a failing scheduler is announced: on its first failed run, or
                once `threshold` runs in a row have failed. Either way a streak is announced once, and a scheduler is announced
                failing at most once an hour.
            threshold (int | Unset):
            notify_on_recovery (bool | Unset):
     """

    notify_on: SchedulerFailureNotifyOn | Unset = UNSET
    threshold: int | Unset = UNSET
    notify_on_recovery: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        notify_on: str | Unset = UNSET
        if not isinstance(self.notify_on, Unset):
            notify_on = self.notify_on


        threshold = self.threshold

        notify_on_recovery = self.notify_on_recovery


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if notify_on is not UNSET:
            field_dict["notify_on"] = notify_on
        if threshold is not UNSET:
            field_dict["threshold"] = threshold
        if notify_on_recovery is not UNSET:
            field_dict["notify_on_recovery"] = notify_on_recovery

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _notify_on = d.pop("notify_on", UNSET)
        notify_on: SchedulerFailureNotifyOn | Unset
        if isinstance(_notify_on,  Unset):
            notify_on = UNSET
        else:
            notify_on = check_scheduler_failure_notify_on(_notify_on)




        threshold = d.pop("threshold", UNSET)

        notify_on_recovery = d.pop("notify_on_recovery", UNSET)

        update_scheduler_failure_alert_policy = cls(
            notify_on=notify_on,
            threshold=threshold,
            notify_on_recovery=notify_on_recovery,
        )

        return update_scheduler_failure_alert_policy

