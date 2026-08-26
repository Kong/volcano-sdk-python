from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.frontend_custom_domain_response_domain_status import check_frontend_custom_domain_response_domain_status
from ..models.frontend_custom_domain_response_domain_status import FrontendCustomDomainResponseDomainStatus
from ..models.frontend_custom_domain_response_tls_mode import check_frontend_custom_domain_response_tls_mode
from ..models.frontend_custom_domain_response_tls_mode import FrontendCustomDomainResponseTlsMode
from ..models.frontend_custom_domain_response_verification_status import check_frontend_custom_domain_response_verification_status
from ..models.frontend_custom_domain_response_verification_status import FrontendCustomDomainResponseVerificationStatus
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.frontend_domain_routing_record import FrontendDomainRoutingRecord
  from ..models.frontend_domain_verification_record import FrontendDomainVerificationRecord
  from ..models.project_frontend_custom_domain_frontend import ProjectFrontendCustomDomainFrontend





T = TypeVar("T", bound="ProjectFrontendCustomDomain")



@_attrs_define
class ProjectFrontendCustomDomain:
    """ 
        Attributes:
            domain (str):
            tls_mode (FrontendCustomDomainResponseTlsMode):
            domain_status (FrontendCustomDomainResponseDomainStatus):
            verification_status (FrontendCustomDomainResponseVerificationStatus):
            effective_urls (list[str]):
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            frontend (ProjectFrontendCustomDomainFrontend): The frontend this custom domain is attached to. Inlined to
                avoid a second fetch from the project-scoped feed.
            verification_records (list[FrontendDomainVerificationRecord] | Unset):
            required_routing_record (FrontendDomainRoutingRecord | Unset):
     """

    domain: str
    tls_mode: FrontendCustomDomainResponseTlsMode
    domain_status: FrontendCustomDomainResponseDomainStatus
    verification_status: FrontendCustomDomainResponseVerificationStatus
    effective_urls: list[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    frontend: ProjectFrontendCustomDomainFrontend
    verification_records: list[FrontendDomainVerificationRecord] | Unset = UNSET
    required_routing_record: FrontendDomainRoutingRecord | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.frontend_domain_routing_record import FrontendDomainRoutingRecord
        from ..models.frontend_domain_verification_record import FrontendDomainVerificationRecord
        from ..models.project_frontend_custom_domain_frontend import ProjectFrontendCustomDomainFrontend
        domain = self.domain

        tls_mode: str = self.tls_mode

        domain_status: str = self.domain_status

        verification_status: str = self.verification_status

        effective_urls = self.effective_urls



        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        frontend = self.frontend.to_dict()

        verification_records: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.verification_records, Unset):
            verification_records = []
            for verification_records_item_data in self.verification_records:
                verification_records_item = verification_records_item_data.to_dict()
                verification_records.append(verification_records_item)



        required_routing_record: dict[str, Any] | Unset = UNSET
        if not isinstance(self.required_routing_record, Unset):
            required_routing_record = self.required_routing_record.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "domain": domain,
            "tls_mode": tls_mode,
            "domain_status": domain_status,
            "verification_status": verification_status,
            "effective_urls": effective_urls,
            "created_at": created_at,
            "updated_at": updated_at,
            "frontend": frontend,
        })
        if verification_records is not UNSET:
            field_dict["verification_records"] = verification_records
        if required_routing_record is not UNSET:
            field_dict["required_routing_record"] = required_routing_record

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.frontend_domain_routing_record import FrontendDomainRoutingRecord
        from ..models.frontend_domain_verification_record import FrontendDomainVerificationRecord
        from ..models.project_frontend_custom_domain_frontend import ProjectFrontendCustomDomainFrontend
        d = dict(src_dict)
        domain = d.pop("domain")

        tls_mode = check_frontend_custom_domain_response_tls_mode(d.pop("tls_mode"))




        domain_status = check_frontend_custom_domain_response_domain_status(d.pop("domain_status"))




        verification_status = check_frontend_custom_domain_response_verification_status(d.pop("verification_status"))




        effective_urls = cast(list[str], d.pop("effective_urls"))


        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        frontend = ProjectFrontendCustomDomainFrontend.from_dict(d.pop("frontend"))




        _verification_records = d.pop("verification_records", UNSET)
        verification_records: list[FrontendDomainVerificationRecord] | Unset = UNSET
        if _verification_records is not UNSET:
            verification_records = []
            for verification_records_item_data in _verification_records:
                verification_records_item = FrontendDomainVerificationRecord.from_dict(verification_records_item_data)



                verification_records.append(verification_records_item)


        _required_routing_record = d.pop("required_routing_record", UNSET)
        required_routing_record: FrontendDomainRoutingRecord | Unset
        if isinstance(_required_routing_record,  Unset):
            required_routing_record = UNSET
        else:
            required_routing_record = FrontendDomainRoutingRecord.from_dict(_required_routing_record)




        project_frontend_custom_domain = cls(
            domain=domain,
            tls_mode=tls_mode,
            domain_status=domain_status,
            verification_status=verification_status,
            effective_urls=effective_urls,
            created_at=created_at,
            updated_at=updated_at,
            frontend=frontend,
            verification_records=verification_records,
            required_routing_record=required_routing_record,
        )


        project_frontend_custom_domain.additional_properties = d
        return project_frontend_custom_domain

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
