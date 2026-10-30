from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateNotificationWebhook")



@_attrs_define
class UpdateNotificationWebhook:
    """ 
        Attributes:
            url (str | Unset): An `http` or `https` URL. Surrounding whitespace is trimmed. An empty string removes the
                webhook and its secret.
     """

    url: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        url = self.url


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url", UNSET)

        update_notification_webhook = cls(
            url=url,
        )

        return update_notification_webhook

