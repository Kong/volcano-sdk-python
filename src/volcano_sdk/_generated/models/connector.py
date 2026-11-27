from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.connector_type import check_connector_type
from ..models.connector_type import ConnectorType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.aikido_connector import AikidoConnector
  from ..models.slack_connector import SlackConnector





T = TypeVar("T", bound="Connector")



@_attrs_define
class Connector:
    """ A link from Volcano to an outside service. A `slack` connector is a Slack workspace the Volcano app is installed in,
    shared by every Volcano account with a Slack identity connected there. An `aikido` connector is an Aikido workspace
    one Volcano account connected with its own credentials.

        Attributes:
            id (UUID):
            type_ (ConnectorType): The outside service a connector links to.
            name (str): The connector's name in its service, such as the Slack or Aikido workspace's name.
            removable (bool): Whether the caller can remove the connector. Only the person who installed the Volcano app in
                a Slack workspace can; an `aikido` connector is always the caller's own.
            created_at (datetime.datetime):
            slack (SlackConnector | Unset): A `slack` connector's workspace. Present when `type` is `slack`.
            aikido (AikidoConnector | Unset): An `aikido` connector's workspace. Present when `type` is `aikido`.
     """

    id: UUID
    type_: ConnectorType
    name: str
    removable: bool
    created_at: datetime.datetime
    slack: SlackConnector | Unset = UNSET
    aikido: AikidoConnector | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.aikido_connector import AikidoConnector # noqa: PLC0415
        from ..models.slack_connector import SlackConnector # noqa: PLC0415
        id = str(self.id)

        type_: str = self.type_

        name = self.name

        removable = self.removable

        created_at = self.created_at.isoformat()

        slack: dict[str, Any] | Unset = UNSET
        if not isinstance(self.slack, Unset):
            slack = self.slack.to_dict()

        aikido: dict[str, Any] | Unset = UNSET
        if not isinstance(self.aikido, Unset):
            aikido = self.aikido.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "type": type_,
            "name": name,
            "removable": removable,
            "created_at": created_at,
        })
        if slack is not UNSET:
            field_dict["slack"] = slack
        if aikido is not UNSET:
            field_dict["aikido"] = aikido

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aikido_connector import AikidoConnector # noqa: PLC0415
        from ..models.slack_connector import SlackConnector # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        type_ = check_connector_type(d.pop("type"))




        name = d.pop("name")

        removable = d.pop("removable")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        _slack = d.pop("slack", UNSET)
        slack: SlackConnector | Unset
        if isinstance(_slack,  Unset):
            slack = UNSET
        else:
            slack = SlackConnector.from_dict(_slack)




        _aikido = d.pop("aikido", UNSET)
        aikido: AikidoConnector | Unset
        if isinstance(_aikido,  Unset):
            aikido = UNSET
        else:
            aikido = AikidoConnector.from_dict(_aikido)




        connector = cls(
            id=id,
            type_=type_,
            name=name,
            removable=removable,
            created_at=created_at,
            slack=slack,
            aikido=aikido,
        )


        connector.additional_properties = d
        return connector

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
