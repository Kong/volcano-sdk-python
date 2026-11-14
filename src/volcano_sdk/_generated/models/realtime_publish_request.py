from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="RealtimePublishRequest")



@_attrs_define
class RealtimePublishRequest:
    """ 
        Attributes:
            channel (str): The client channel, `broadcast:<name>` or `grant:<name>`, with a name of at most 64 characters.
            event (str): The message type subscribers match on.
            payload (Any): Any JSON value, sent to subscribers as `payload`.
     """

    channel: str
    event: str
    payload: Any





    def to_dict(self) -> dict[str, Any]:
        channel = self.channel

        event = self.event

        payload = self.payload


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "channel": channel,
            "event": event,
            "payload": payload,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        channel = d.pop("channel")

        event = d.pop("event")

        payload = d.pop("payload")

        realtime_publish_request = cls(
            channel=channel,
            event=event,
            payload=payload,
        )

        return realtime_publish_request

