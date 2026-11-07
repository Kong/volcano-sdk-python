from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.lavaflow_slack_channel import LavaflowSlackChannel





T = TypeVar("T", bound="LavaflowSlackChannelsResponse")



@_attrs_define
class LavaflowSlackChannelsResponse:
    """ 
        Attributes:
            channels (list[LavaflowSlackChannel]):
     """

    channels: list[LavaflowSlackChannel]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_slack_channel import LavaflowSlackChannel # noqa: PLC0415
        channels = []
        for channels_item_data in self.channels:
            channels_item = channels_item_data.to_dict()
            channels.append(channels_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "channels": channels,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_slack_channel import LavaflowSlackChannel # noqa: PLC0415
        d = dict(src_dict)
        channels = []
        _channels = d.pop("channels")
        for channels_item_data in (_channels):
            channels_item = LavaflowSlackChannel.from_dict(channels_item_data)



            channels.append(channels_item)


        lavaflow_slack_channels_response = cls(
            channels=channels,
        )


        lavaflow_slack_channels_response.additional_properties = d
        return lavaflow_slack_channels_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
