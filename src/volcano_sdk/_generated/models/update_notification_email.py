from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="UpdateNotificationEmail")



@_attrs_define
class UpdateNotificationEmail:
    """ 
        Attributes:
            enabled (bool | Unset):
            recipients (list[str] | Unset): Only the project owner's verified account email address is supported. An empty
                list, or one naming only that address, emails the owner and is saved as an empty list. Any other list is refused
                as invalid.
     """

    enabled: bool | Unset = UNSET
    recipients: list[str] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        recipients: list[str] | Unset = UNSET
        if not isinstance(self.recipients, Unset):
            recipients = self.recipients




        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if recipients is not UNSET:
            field_dict["recipients"] = recipients

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        recipients = cast(list[str], d.pop("recipients", UNSET))


        update_notification_email = cls(
            enabled=enabled,
            recipients=recipients,
        )

        return update_notification_email

