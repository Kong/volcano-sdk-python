from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.aikido_region import AikidoRegion
from ..models.aikido_region import check_aikido_region
from typing import cast






T = TypeVar("T", bound="AikidoConnectorCreate")



@_attrs_define
class AikidoConnectorCreate:
    """ The Aikido workspace's REST API client and webhook signing secret.

        Attributes:
            region (AikidoRegion): The Aikido region the workspace lives in: `eu` for app.aikido.dev, `us` for
                app.us.aikido.dev, `au` for app.au.aikido.dev, and `me` for app.me.aikido.dev.
            client_id (str):
            client_secret (str):
            webhook_secret (str): The signing secret from Aikido's webhooks page, which verifies its deliveries.
     """

    region: AikidoRegion
    client_id: str
    client_secret: str
    webhook_secret: str





    def to_dict(self) -> dict[str, Any]:
        region: str = self.region

        client_id = self.client_id

        client_secret = self.client_secret

        webhook_secret = self.webhook_secret


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "region": region,
            "client_id": client_id,
            "client_secret": client_secret,
            "webhook_secret": webhook_secret,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        region = check_aikido_region(d.pop("region"))




        client_id = d.pop("client_id")

        client_secret = d.pop("client_secret")

        webhook_secret = d.pop("webhook_secret")

        aikido_connector_create = cls(
            region=region,
            client_id=client_id,
            client_secret=client_secret,
            webhook_secret=webhook_secret,
        )

        return aikido_connector_create

