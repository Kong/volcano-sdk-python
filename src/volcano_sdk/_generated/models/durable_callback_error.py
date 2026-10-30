from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="DurableCallbackError")



@_attrs_define
class DurableCallbackError:
    """ The error the waiting step raises.

        Attributes:
            type_ (str): A name workflows can branch on, such as `PaymentDeclined`. Up to
                256 characters, without control characters.
            message (str | Unset): A human-readable explanation of up to 32,768 bytes of UTF-8, with
                tab and newline as its only control characters. A character
                outside ASCII takes more than one byte, so such text reaches the
                limit before `maxLength`.
     """

    type_: str
    message: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        message = self.message


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
        })
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        message = d.pop("message", UNSET)

        durable_callback_error = cls(
            type_=type_,
            message=message,
        )

        return durable_callback_error

