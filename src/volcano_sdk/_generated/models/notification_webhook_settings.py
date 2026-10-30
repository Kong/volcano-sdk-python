from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="NotificationWebhookSettings")



@_attrs_define
class NotificationWebhookSettings:
    """ 
        Attributes:
            secret_configured (bool): Whether a signing secret is set. The secret itself is returned only once.
            url (str | Unset): Where alerts are posted. Absent when no webhook is configured.
            secret (str | Unset): The signing secret, starting with `whsec_`. Present only in the response that generated
                it: the update that first set `url`, or a rotation. Store it then; it cannot be read again.
     """

    secret_configured: bool
    url: str | Unset = UNSET
    secret: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        secret_configured = self.secret_configured

        url = self.url

        secret = self.secret


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "secret_configured": secret_configured,
        })
        if url is not UNSET:
            field_dict["url"] = url
        if secret is not UNSET:
            field_dict["secret"] = secret

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        secret_configured = d.pop("secret_configured")

        url = d.pop("url", UNSET)

        secret = d.pop("secret", UNSET)

        notification_webhook_settings = cls(
            secret_configured=secret_configured,
            url=url,
            secret=secret,
        )

        return notification_webhook_settings

