from typing import Literal

FrontendDomainRoutingRecordRecordType = Literal['CNAME']

FRONTEND_DOMAIN_ROUTING_RECORD_RECORD_TYPE_VALUES: set[FrontendDomainRoutingRecordRecordType] = { 'CNAME',  }

def check_frontend_domain_routing_record_record_type(value: str) -> FrontendDomainRoutingRecordRecordType:
    if value in FRONTEND_DOMAIN_ROUTING_RECORD_RECORD_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_DOMAIN_ROUTING_RECORD_RECORD_TYPE_VALUES!r}")
