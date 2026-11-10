from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="SlackConnection")



@_attrs_define
class SlackConnection:
    """ A Slack identity connected to the caller's Volcano account.

        Attributes:
            id (UUID):
            team_id (str): A Slack workspace ID, such as `T0123ABCD`.
            team_name (str): The workspace's name, or empty until the Volcano app is installed in it.
            slack_user_id (str): The Slack user ID Slack verified.
            installed (bool): Whether the Volcano app is installed in the workspace.
            created_at (datetime.datetime):
     """

    id: UUID
    team_id: str
    team_name: str
    slack_user_id: str
    installed: bool
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        team_id = self.team_id

        team_name = self.team_name

        slack_user_id = self.slack_user_id

        installed = self.installed

        created_at = self.created_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "team_id": team_id,
            "team_name": team_name,
            "slack_user_id": slack_user_id,
            "installed": installed,
            "created_at": created_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        team_id = d.pop("team_id")

        team_name = d.pop("team_name")

        slack_user_id = d.pop("slack_user_id")

        installed = d.pop("installed")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        slack_connection = cls(
            id=id,
            team_id=team_id,
            team_name=team_name,
            slack_user_id=slack_user_id,
            installed=installed,
            created_at=created_at,
        )


        slack_connection.additional_properties = d
        return slack_connection

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
