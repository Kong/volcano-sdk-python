from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.notification_test_delivery_channel import check_notification_test_delivery_channel
from ..models.notification_test_delivery_channel import NotificationTestDeliveryChannel
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="NotificationTestDelivery")



@_attrs_define
class NotificationTestDelivery:
    """ 
        Attributes:
            channel (NotificationTestDeliveryChannel):
            delivered (bool):
            status_code (int | Unset): The webhook's response status. Absent for email, and when no response arrived.
            error (str | Unset): Why the delivery failed. Absent when it arrived.
     """

    channel: NotificationTestDeliveryChannel
    delivered: bool
    status_code: int | Unset = UNSET
    error: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        channel: str = self.channel

        delivered = self.delivered

        status_code = self.status_code

        error = self.error


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "channel": channel,
            "delivered": delivered,
        })
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        channel = check_notification_test_delivery_channel(d.pop("channel"))




        delivered = d.pop("delivered")

        status_code = d.pop("status_code", UNSET)

        error = d.pop("error", UNSET)

        notification_test_delivery = cls(
            channel=channel,
            delivered=delivered,
            status_code=status_code,
            error=error,
        )

        return notification_test_delivery

