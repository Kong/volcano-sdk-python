from typing import Literal

FrontendDomainRoutingRecordZoneApexRecordType = Literal['ALIAS']

FRONTEND_DOMAIN_ROUTING_RECORD_ZONE_APEX_RECORD_TYPE_VALUES: set[FrontendDomainRoutingRecordZoneApexRecordType] = { 'ALIAS',  }

def check_frontend_domain_routing_record_zone_apex_record_type(value: str) -> FrontendDomainRoutingRecordZoneApexRecordType:
    if value in FRONTEND_DOMAIN_ROUTING_RECORD_ZONE_APEX_RECORD_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_DOMAIN_ROUTING_RECORD_ZONE_APEX_RECORD_TYPE_VALUES!r}")
