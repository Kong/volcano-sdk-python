from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.frontend_custom_domain_response_domain_status import check_frontend_custom_domain_response_domain_status
from ..models.frontend_custom_domain_response_domain_status import FrontendCustomDomainResponseDomainStatus
from ..models.frontend_custom_domain_response_serving_certificate import check_frontend_custom_domain_response_serving_certificate
from ..models.frontend_custom_domain_response_serving_certificate import FrontendCustomDomainResponseServingCertificate
from ..models.frontend_custom_domain_response_tls_mode import check_frontend_custom_domain_response_tls_mode
from ..models.frontend_custom_domain_response_tls_mode import FrontendCustomDomainResponseTlsMode
from ..models.frontend_custom_domain_response_verification_status import check_frontend_custom_domain_response_verification_status
from ..models.frontend_custom_domain_response_verification_status import FrontendCustomDomainResponseVerificationStatus
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.frontend_custom_domain_redirect import FrontendCustomDomainRedirect
  from ..models.frontend_domain_routing_record import FrontendDomainRoutingRecord
  from ..models.frontend_domain_verification_record import FrontendDomainVerificationRecord





T = TypeVar("T", bound="FrontendCustomDomainResponse")



@_attrs_define
class FrontendCustomDomainResponse:
    """ 
        Attributes:
            domain (str):
            tls_mode (FrontendCustomDomainResponseTlsMode):
            domain_status (FrontendCustomDomainResponseDomainStatus):
            verification_status (FrontendCustomDomainResponseVerificationStatus): `verified`: the domain is served by a
                validated certificate. `pending`: it is not served yet, is being re-validated after its certificate material was
                withdrawn, or Volcano is retrying after a failure. `failed`: a failure left the domain unserved, alongside
                `domain_status: failed`; managed domains report the cause in `failure_reason`.
            effective_urls (list[str]):
            redirect (FrontendCustomDomainRedirect | None): Where the domain redirects every request, or null when it serves
                the frontend.
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            serving_certificate (FrontendCustomDomainResponseServingCertificate | Unset): Certificate the domain serves,
                present only while it is active. `uploaded`: the BYOC certificate, including after the domain switched to
                managed TLS and until Volcano issues the managed one; `failure_reason` then reports an issuance failure.
                `managed`: a certificate Volcano issued.
            failure_reason (str | Unset): Failure category, present when managed TLS setup has failed, or when issuance is
                failing for a domain that switched to managed TLS and still serves its uploaded certificate. Current values are
                provider, certificate, ownership, and internal; ownership means another account has already claimed the hostname
                through ownership verification. Treat unrecognized values as internal.
            verification_records (list[FrontendDomainVerificationRecord] | Unset): DNS records to publish now. For a managed
                domain whose hostname the account already owns, the create response names the `_acme-challenge` CNAME that
                authorizes certificate issuance and renewal. Otherwise it names the `_volcano` TXT record that proves ownership
                of the hostname's registrable domain, and reads return the CNAME once Volcano sees that record. Usually empty
                for BYOC.
            required_routing_record (FrontendDomainRoutingRecord | Unset):
            routing_target_hostname (str | Unset): DNS routing target hostname for this frontend. The DNS record type
                depends on whether the custom domain is a zone apex.
     """

    domain: str
    tls_mode: FrontendCustomDomainResponseTlsMode
    domain_status: FrontendCustomDomainResponseDomainStatus
    verification_status: FrontendCustomDomainResponseVerificationStatus
    effective_urls: list[str]
    redirect: FrontendCustomDomainRedirect | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    serving_certificate: FrontendCustomDomainResponseServingCertificate | Unset = UNSET
    failure_reason: str | Unset = UNSET
    verification_records: list[FrontendDomainVerificationRecord] | Unset = UNSET
    required_routing_record: FrontendDomainRoutingRecord | Unset = UNSET
    routing_target_hostname: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.frontend_custom_domain_redirect import FrontendCustomDomainRedirect # noqa: PLC0415
        from ..models.frontend_domain_routing_record import FrontendDomainRoutingRecord # noqa: PLC0415
        from ..models.frontend_domain_verification_record import FrontendDomainVerificationRecord # noqa: PLC0415
        domain = self.domain

        tls_mode: str = self.tls_mode

        domain_status: str = self.domain_status

        verification_status: str = self.verification_status

        effective_urls = self.effective_urls



        redirect: dict[str, Any] | None
        if isinstance(self.redirect, FrontendCustomDomainRedirect):
            redirect = self.redirect.to_dict()
        else:
            redirect = self.redirect

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        serving_certificate: str | Unset = UNSET
        if not isinstance(self.serving_certificate, Unset):
            serving_certificate = self.serving_certificate


        failure_reason = self.failure_reason

        verification_records: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.verification_records, Unset):
            verification_records = []
            for verification_records_item_data in self.verification_records:
                verification_records_item = verification_records_item_data.to_dict()
                verification_records.append(verification_records_item)



        required_routing_record: dict[str, Any] | Unset = UNSET
        if not isinstance(self.required_routing_record, Unset):
            required_routing_record = self.required_routing_record.to_dict()

        routing_target_hostname = self.routing_target_hostname


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "domain": domain,
            "tls_mode": tls_mode,
            "domain_status": domain_status,
            "verification_status": verification_status,
            "effective_urls": effective_urls,
            "redirect": redirect,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if serving_certificate is not UNSET:
            field_dict["serving_certificate"] = serving_certificate
        if failure_reason is not UNSET:
            field_dict["failure_reason"] = failure_reason
        if verification_records is not UNSET:
            field_dict["verification_records"] = verification_records
        if required_routing_record is not UNSET:
            field_dict["required_routing_record"] = required_routing_record
        if routing_target_hostname is not UNSET:
            field_dict["routing_target_hostname"] = routing_target_hostname

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.frontend_custom_domain_redirect import FrontendCustomDomainRedirect # noqa: PLC0415
        from ..models.frontend_domain_routing_record import FrontendDomainRoutingRecord # noqa: PLC0415
        from ..models.frontend_domain_verification_record import FrontendDomainVerificationRecord # noqa: PLC0415
        d = dict(src_dict)
        domain = d.pop("domain")

        tls_mode = check_frontend_custom_domain_response_tls_mode(d.pop("tls_mode"))




        domain_status = check_frontend_custom_domain_response_domain_status(d.pop("domain_status"))




        verification_status = check_frontend_custom_domain_response_verification_status(d.pop("verification_status"))




        effective_urls = cast(list[str], d.pop("effective_urls"))


        def _parse_redirect(data: object) -> FrontendCustomDomainRedirect | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                redirect_type_1 = FrontendCustomDomainRedirect.from_dict(data)



                return redirect_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FrontendCustomDomainRedirect | None, data)

        redirect = _parse_redirect(d.pop("redirect"))


        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        _serving_certificate = d.pop("serving_certificate", UNSET)
        serving_certificate: FrontendCustomDomainResponseServingCertificate | Unset
        if isinstance(_serving_certificate,  Unset):
            serving_certificate = UNSET
        else:
            serving_certificate = check_frontend_custom_domain_response_serving_certificate(_serving_certificate)




        failure_reason = d.pop("failure_reason", UNSET)

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




        routing_target_hostname = d.pop("routing_target_hostname", UNSET)

        frontend_custom_domain_response = cls(
            domain=domain,
            tls_mode=tls_mode,
            domain_status=domain_status,
            verification_status=verification_status,
            effective_urls=effective_urls,
            redirect=redirect,
            created_at=created_at,
            updated_at=updated_at,
            serving_certificate=serving_certificate,
            failure_reason=failure_reason,
            verification_records=verification_records,
            required_routing_record=required_routing_record,
            routing_target_hostname=routing_target_hostname,
        )


        frontend_custom_domain_response.additional_properties = d
        return frontend_custom_domain_response

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
