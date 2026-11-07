from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="LavaflowSlackChannelBinding")



@_attrs_define
class LavaflowSlackChannelBinding:
    """ 
        Attributes:
            project_id (UUID): The project the channel reports for.
            team_id (str): A Slack workspace ID, such as `T0123ABCD`.
            channel_id (str): A Slack channel ID, such as `C0123ABCD`.
     """

    project_id: UUID
    team_id: str
    channel_id: str





    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        team_id = self.team_id

        channel_id = self.channel_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "project_id": project_id,
            "team_id": team_id,
            "channel_id": channel_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        team_id = d.pop("team_id")

        channel_id = d.pop("channel_id")

        lavaflow_slack_channel_binding = cls(
            project_id=project_id,
            team_id=team_id,
            channel_id=channel_id,
        )

        return lavaflow_slack_channel_binding

