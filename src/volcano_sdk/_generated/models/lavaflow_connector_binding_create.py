from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.lavaflow_slack_binding_target import LavaflowSlackBindingTarget





T = TypeVar("T", bound="LavaflowConnectorBindingCreate")



@_attrs_define
class LavaflowConnectorBindingCreate:
    """ 
        Attributes:
            project_id (UUID): The project the place reports for.
            connector_id (UUID): The connector to bind, from `GET /connectors`.
            slack (LavaflowSlackBindingTarget): The channel to bind, for a `slack` connector.
     """

    project_id: UUID
    connector_id: UUID
    slack: LavaflowSlackBindingTarget





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_slack_binding_target import LavaflowSlackBindingTarget # noqa: PLC0415
        project_id = str(self.project_id)

        connector_id = str(self.connector_id)

        slack = self.slack.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "project_id": project_id,
            "connector_id": connector_id,
            "slack": slack,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_slack_binding_target import LavaflowSlackBindingTarget # noqa: PLC0415
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        connector_id = UUID(d.pop("connector_id"))




        slack = LavaflowSlackBindingTarget.from_dict(d.pop("slack"))




        lavaflow_connector_binding_create = cls(
            project_id=project_id,
            connector_id=connector_id,
            slack=slack,
        )

        return lavaflow_connector_binding_create

