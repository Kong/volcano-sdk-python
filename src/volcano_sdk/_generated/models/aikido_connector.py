from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.aikido_region import AikidoRegion
from ..models.aikido_region import check_aikido_region
from typing import cast






T = TypeVar("T", bound="AikidoConnector")



@_attrs_define
class AikidoConnector:
    """ An `aikido` connector's workspace. Present when `type` is `aikido`.

        Attributes:
            region (AikidoRegion): The Aikido region the workspace lives in: `eu` for app.aikido.dev, `us` for
                app.us.aikido.dev, `au` for app.au.aikido.dev, and `me` for app.me.aikido.dev.
            workspace_id (int): The workspace's ID in Aikido, which its webhook deliveries name.
     """

    region: AikidoRegion
    workspace_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        region: str = self.region

        workspace_id = self.workspace_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "region": region,
            "workspace_id": workspace_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        region = check_aikido_region(d.pop("region"))




        workspace_id = d.pop("workspace_id")

        aikido_connector = cls(
            region=region,
            workspace_id=workspace_id,
        )


        aikido_connector.additional_properties = d
        return aikido_connector

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
