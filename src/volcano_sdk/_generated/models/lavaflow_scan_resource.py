from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_scan_resource_resource_type import check_lavaflow_scan_resource_resource_type
from ..models.lavaflow_scan_resource_resource_type import LavaflowScanResourceResourceType
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="LavaflowScanResource")



@_attrs_define
class LavaflowScanResource:
    """ A resource whose production deploy the scan covers. Only frontend deploys ask for a scan for now.

        Attributes:
            resource_type (LavaflowScanResourceResourceType):
            resource_id (UUID):
            deployment_id (UUID):
     """

    resource_type: LavaflowScanResourceResourceType
    resource_id: UUID
    deployment_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        resource_type: str = self.resource_type

        resource_id = str(self.resource_id)

        deployment_id = str(self.deployment_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "resource_type": resource_type,
            "resource_id": resource_id,
            "deployment_id": deployment_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource_type = check_lavaflow_scan_resource_resource_type(d.pop("resource_type"))




        resource_id = UUID(d.pop("resource_id"))




        deployment_id = UUID(d.pop("deployment_id"))




        lavaflow_scan_resource = cls(
            resource_type=resource_type,
            resource_id=resource_id,
            deployment_id=deployment_id,
        )


        lavaflow_scan_resource.additional_properties = d
        return lavaflow_scan_resource

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
