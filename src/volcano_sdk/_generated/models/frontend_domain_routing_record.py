from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.frontend_domain_routing_record_record_type import check_frontend_domain_routing_record_record_type
from ..models.frontend_domain_routing_record_record_type import FrontendDomainRoutingRecordRecordType
from typing import cast






T = TypeVar("T", bound="FrontendDomainRoutingRecord")



@_attrs_define
class FrontendDomainRoutingRecord:
    """ 
        Attributes:
            record_type (FrontendDomainRoutingRecordRecordType):
            name (str):
            value (str):
     """

    record_type: FrontendDomainRoutingRecordRecordType
    name: str
    value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        record_type: str = self.record_type

        name = self.name

        value = self.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "record_type": record_type,
            "name": name,
            "value": value,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        record_type = check_frontend_domain_routing_record_record_type(d.pop("record_type"))




        name = d.pop("name")

        value = d.pop("value")

        frontend_domain_routing_record = cls(
            record_type=record_type,
            name=name,
            value=value,
        )


        frontend_domain_routing_record.additional_properties = d
        return frontend_domain_routing_record

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
