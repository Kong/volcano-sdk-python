from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="RealtimePublishResult")



@_attrs_define
class RealtimePublishResult:
    """ 
        Attributes:
            channel (str): The channel the message was sent to.
     """

    channel: str





    def to_dict(self) -> dict[str, Any]:
        channel = self.channel


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "channel": channel,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        channel = d.pop("channel")

        realtime_publish_result = cls(
            channel=channel,
        )

        return realtime_publish_result

