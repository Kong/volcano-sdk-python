from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.connector_create_type import check_connector_create_type
from ..models.connector_create_type import ConnectorCreateType
from typing import cast

if TYPE_CHECKING:
  from ..models.aikido_connector_create import AikidoConnectorCreate





T = TypeVar("T", bound="ConnectorCreate")



@_attrs_define
class ConnectorCreate:
    """ 
        Attributes:
            type_ (ConnectorCreateType): The service to connect. Slack installs with `POST /user/slack/installations`.
            aikido (AikidoConnectorCreate): The Aikido workspace's REST API client and webhook signing secret.
     """

    type_: ConnectorCreateType
    aikido: AikidoConnectorCreate





    def to_dict(self) -> dict[str, Any]:
        from ..models.aikido_connector_create import AikidoConnectorCreate # noqa: PLC0415
        type_: str = self.type_

        aikido = self.aikido.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
            "aikido": aikido,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aikido_connector_create import AikidoConnectorCreate # noqa: PLC0415
        d = dict(src_dict)
        type_ = check_connector_create_type(d.pop("type"))




        aikido = AikidoConnectorCreate.from_dict(d.pop("aikido"))




        connector_create = cls(
            type_=type_,
            aikido=aikido,
        )

        return connector_create

