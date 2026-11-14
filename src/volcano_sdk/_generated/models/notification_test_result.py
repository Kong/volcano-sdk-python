from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.notification_test_delivery import NotificationTestDelivery





T = TypeVar("T", bound="NotificationTestResult")



@_attrs_define
class NotificationTestResult:
    """ 
        Attributes:
            deliveries (list[NotificationTestDelivery]):
     """

    deliveries: list[NotificationTestDelivery]





    def to_dict(self) -> dict[str, Any]:
        from ..models.notification_test_delivery import NotificationTestDelivery # noqa: PLC0415
        deliveries = []
        for deliveries_item_data in self.deliveries:
            deliveries_item = deliveries_item_data.to_dict()
            deliveries.append(deliveries_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "deliveries": deliveries,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.notification_test_delivery import NotificationTestDelivery # noqa: PLC0415
        d = dict(src_dict)
        deliveries = []
        _deliveries = d.pop("deliveries")
        for deliveries_item_data in (_deliveries):
            deliveries_item = NotificationTestDelivery.from_dict(deliveries_item_data)



            deliveries.append(deliveries_item)


        notification_test_result = cls(
            deliveries=deliveries,
        )

        return notification_test_result

