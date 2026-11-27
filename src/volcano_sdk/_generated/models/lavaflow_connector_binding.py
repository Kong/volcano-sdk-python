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
  from ..models.lavaflow_aikido_binding import LavaflowAikidoBinding
  from ..models.lavaflow_slack_binding import LavaflowSlackBinding





T = TypeVar("T", bound="LavaflowConnectorBinding")



@_attrs_define
class LavaflowConnectorBinding:
    """ A place in a connector that reports problems to LavaFlow for a project: a Slack channel, or an Aikido workspace's
    issues on the project's repository.

        Attributes:
            id (UUID): The binding's ID, which removing it takes.
            project_id (UUID):
            connector_type (ConnectorType): The outside service a connector links to.
            created_at (datetime.datetime):
            connector_id (UUID | Unset): The connector the binding reports through. Omitted while the Volcano app is not
                installed in the binding's Slack workspace; the binding reports again once it is.
            slack (LavaflowSlackBinding | Unset): The Slack channel a binding reports from. Present when `connector_type` is
                `slack`.
            aikido (LavaflowAikidoBinding | Unset): The Aikido workspace a binding reports issues from. Present when
                `connector_type` is `aikido`.
     """

    id: UUID
    project_id: UUID
    connector_type: ConnectorType
    created_at: datetime.datetime
    connector_id: UUID | Unset = UNSET
    slack: LavaflowSlackBinding | Unset = UNSET
    aikido: LavaflowAikidoBinding | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_aikido_binding import LavaflowAikidoBinding # noqa: PLC0415
        from ..models.lavaflow_slack_binding import LavaflowSlackBinding # noqa: PLC0415
        id = str(self.id)

        project_id = str(self.project_id)

        connector_type: str = self.connector_type

        created_at = self.created_at.isoformat()

        connector_id: str | Unset = UNSET
        if not isinstance(self.connector_id, Unset):
            connector_id = str(self.connector_id)

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
            "project_id": project_id,
            "connector_type": connector_type,
            "created_at": created_at,
        })
        if connector_id is not UNSET:
            field_dict["connector_id"] = connector_id
        if slack is not UNSET:
            field_dict["slack"] = slack
        if aikido is not UNSET:
            field_dict["aikido"] = aikido

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_aikido_binding import LavaflowAikidoBinding # noqa: PLC0415
        from ..models.lavaflow_slack_binding import LavaflowSlackBinding # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        connector_type = check_connector_type(d.pop("connector_type"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        _connector_id = d.pop("connector_id", UNSET)
        connector_id: UUID | Unset
        if isinstance(_connector_id,  Unset):
            connector_id = UNSET
        else:
            connector_id = UUID(_connector_id)




        _slack = d.pop("slack", UNSET)
        slack: LavaflowSlackBinding | Unset
        if isinstance(_slack,  Unset):
            slack = UNSET
        else:
            slack = LavaflowSlackBinding.from_dict(_slack)




        _aikido = d.pop("aikido", UNSET)
        aikido: LavaflowAikidoBinding | Unset
        if isinstance(_aikido,  Unset):
            aikido = UNSET
        else:
            aikido = LavaflowAikidoBinding.from_dict(_aikido)




        lavaflow_connector_binding = cls(
            id=id,
            project_id=project_id,
            connector_type=connector_type,
            created_at=created_at,
            connector_id=connector_id,
            slack=slack,
            aikido=aikido,
        )


        lavaflow_connector_binding.additional_properties = d
        return lavaflow_connector_binding

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
