from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.scheduler_failure_notify_on import check_scheduler_failure_notify_on
from ..models.scheduler_failure_notify_on import SchedulerFailureNotifyOn
from typing import cast






T = TypeVar("T", bound="SchedulerFailureAlertPolicy")



@_attrs_define
class SchedulerFailureAlertPolicy:
    """ 
        Attributes:
            notify_on (SchedulerFailureNotifyOn): When a failing scheduler is announced: on its first failed run, or once
                `threshold` runs in a row have failed. Either way a streak is announced once, and a scheduler is announced
                failing at most once an hour.
            threshold (int): How many runs in a row have to fail before a `consecutive_failures` alert. Ignored for
                `first_failure`.
            notify_on_recovery (bool): Whether a successful run after an alerted failure streak sends a
                `scheduler.recovered` alert.
     """

    notify_on: SchedulerFailureNotifyOn
    threshold: int
    notify_on_recovery: bool





    def to_dict(self) -> dict[str, Any]:
        notify_on: str = self.notify_on

        threshold = self.threshold

        notify_on_recovery = self.notify_on_recovery


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "notify_on": notify_on,
            "threshold": threshold,
            "notify_on_recovery": notify_on_recovery,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        notify_on = check_scheduler_failure_notify_on(d.pop("notify_on"))




        threshold = d.pop("threshold")

        notify_on_recovery = d.pop("notify_on_recovery")

        scheduler_failure_alert_policy = cls(
            notify_on=notify_on,
            threshold=threshold,
            notify_on_recovery=notify_on_recovery,
        )

        return scheduler_failure_alert_policy

