from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="PublishDurableMessageRequest")



@_attrs_define
class PublishDurableMessageRequest:
    """ 
        Attributes:
            name (str): The name a workflow waits on or publishes under: up to 237 printable
                ASCII characters.
            data (Any | Unset): Any JSON value, up to 64 KiB. Omitted means null.
     """

    name: str
    data: Any | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        data = self.data


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
        })
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        data = d.pop("data", UNSET)

        publish_durable_message_request = cls(
            name=name,
            data=data,
        )

        return publish_durable_message_request

