from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.notification_email_status import check_notification_email_status
from ..models.notification_email_status import NotificationEmailStatus
from typing import cast






T = TypeVar("T", bound="NotificationEmailSettings")



@_attrs_define
class NotificationEmailSettings:
    """ 
        Attributes:
            enabled (bool): Whether alerts are emailed.
            recipients (list[str]): Empty. Alerts are emailed to the project owner's verified account email address, the
                only recipient supported.
            status (NotificationEmailStatus): Whether alerts are being emailed. `owner_email_unverified` means email is
                enabled but the project owner has no active account with a verified email address, so no alert is emailed, and
                email does not count as a channel when deciding whether to announce a failing scheduler, until the owner
                verifies it. Changing the account email address needs a new verification.
     """

    enabled: bool
    recipients: list[str]
    status: NotificationEmailStatus





    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        recipients = self.recipients



        status: str = self.status


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "enabled": enabled,
            "recipients": recipients,
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        recipients = cast(list[str], d.pop("recipients"))


        status = check_notification_email_status(d.pop("status"))




        notification_email_settings = cls(
            enabled=enabled,
            recipients=recipients,
            status=status,
        )

        return notification_email_settings

