from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.frontend_domain_routing_record_record_type import check_frontend_domain_routing_record_record_type
from ..models.frontend_domain_routing_record_record_type import FrontendDomainRoutingRecordRecordType
from ..models.frontend_domain_routing_record_zone_apex_record_type import check_frontend_domain_routing_record_zone_apex_record_type
from ..models.frontend_domain_routing_record_zone_apex_record_type import FrontendDomainRoutingRecordZoneApexRecordType
from typing import cast






T = TypeVar("T", bound="FrontendDomainRoutingRecord")



@_attrs_define
class FrontendDomainRoutingRecord:
    """ 
        Attributes:
            record_type (FrontendDomainRoutingRecordRecordType): Use this record type when the hostname is not the apex of
                your DNS zone.
            zone_apex_record_type (FrontendDomainRoutingRecordZoneApexRecordType): At the apex of your DNS zone, use your
                provider's ALIAS, ANAME, or CNAME-flattening equivalent instead of a literal CNAME.
            name (str):
            value (str):
     """

    record_type: FrontendDomainRoutingRecordRecordType
    zone_apex_record_type: FrontendDomainRoutingRecordZoneApexRecordType
    name: str
    value: str





    def to_dict(self) -> dict[str, Any]:
        record_type: str = self.record_type

        zone_apex_record_type: str = self.zone_apex_record_type

        name = self.name

        value = self.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "record_type": record_type,
            "zone_apex_record_type": zone_apex_record_type,
            "name": name,
            "value": value,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        record_type = check_frontend_domain_routing_record_record_type(d.pop("record_type"))




        zone_apex_record_type = check_frontend_domain_routing_record_zone_apex_record_type(d.pop("zone_apex_record_type"))




        name = d.pop("name")

        value = d.pop("value")

        frontend_domain_routing_record = cls(
            record_type=record_type,
            zone_apex_record_type=zone_apex_record_type,
            name=name,
            value=value,
        )

        return frontend_domain_routing_record

