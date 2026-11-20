from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowSlackBinding")



@_attrs_define
class LavaflowSlackBinding:
    """ The Slack channel a binding reports from. Present when `connector_type` is `slack`.

        Attributes:
            team_id (str): A Slack workspace ID, such as `T0123ABCD`.
            team_name (str): The workspace's name, or empty while the Volcano app is not installed in it.
            channel_id (str): A Slack channel ID, such as `C0123ABCD`.
     """

    team_id: str
    team_name: str
    channel_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        team_id = self.team_id

        team_name = self.team_name

        channel_id = self.channel_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "team_id": team_id,
            "team_name": team_name,
            "channel_id": channel_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        team_id = d.pop("team_id")

        team_name = d.pop("team_name")

        channel_id = d.pop("channel_id")

        lavaflow_slack_binding = cls(
            team_id=team_id,
            team_name=team_name,
            channel_id=channel_id,
        )


        lavaflow_slack_binding.additional_properties = d
        return lavaflow_slack_binding

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
