from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowSlackBindingTarget")



@_attrs_define
class LavaflowSlackBindingTarget:
    """ The channel to bind, for a `slack` connector.

        Attributes:
            channel_id (str): A Slack channel ID, such as `C0123ABCD`.
     """

    channel_id: str





    def to_dict(self) -> dict[str, Any]:
        channel_id = self.channel_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "channel_id": channel_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        channel_id = d.pop("channel_id")

        lavaflow_slack_binding_target = cls(
            channel_id=channel_id,
        )

        return lavaflow_slack_binding_target

