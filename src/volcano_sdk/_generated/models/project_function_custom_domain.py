from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.function_custom_domain_response_domain_status import check_function_custom_domain_response_domain_status
from ..models.function_custom_domain_response_domain_status import FunctionCustomDomainResponseDomainStatus
from ..models.function_custom_domain_response_tls_mode import check_function_custom_domain_response_tls_mode
from ..models.function_custom_domain_response_tls_mode import FunctionCustomDomainResponseTlsMode
from ..models.function_custom_domain_response_verification_status import check_function_custom_domain_response_verification_status
from ..models.function_custom_domain_response_verification_status import FunctionCustomDomainResponseVerificationStatus
from ..models.project_function_custom_domain_target_type import check_project_function_custom_domain_target_type
from ..models.project_function_custom_domain_target_type import ProjectFunctionCustomDomainTargetType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.frontend_domain_routing_record import FrontendDomainRoutingRecord
  from ..models.frontend_domain_verification_record import FrontendDomainVerificationRecord
  from ..models.project_custom_domain_target import ProjectCustomDomainTarget
  from ..models.project_function_custom_domain_function import ProjectFunctionCustomDomainFunction





T = TypeVar("T", bound="ProjectFunctionCustomDomain")



@_attrs_define
class ProjectFunctionCustomDomain:
    """ 
        Attributes:
            function_id (UUID):
            domain (str):
            tls_mode (FunctionCustomDomainResponseTlsMode):
            domain_status (FunctionCustomDomainResponseDomainStatus):
            verification_status (FunctionCustomDomainResponseVerificationStatus):
            effective_urls (list[str]):
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            target (ProjectCustomDomainTarget):
            target_type (ProjectFunctionCustomDomainTargetType):
            function (ProjectFunctionCustomDomainFunction):
            verification_records (list[FrontendDomainVerificationRecord] | Unset):
            required_routing_record (FrontendDomainRoutingRecord | Unset):
     """

    function_id: UUID
    domain: str
    tls_mode: FunctionCustomDomainResponseTlsMode
    domain_status: FunctionCustomDomainResponseDomainStatus
    verification_status: FunctionCustomDomainResponseVerificationStatus
    effective_urls: list[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    target: ProjectCustomDomainTarget
    target_type: ProjectFunctionCustomDomainTargetType
    function: ProjectFunctionCustomDomainFunction
    verification_records: list[FrontendDomainVerificationRecord] | Unset = UNSET
    required_routing_record: FrontendDomainRoutingRecord | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.frontend_domain_routing_record import FrontendDomainRoutingRecord
        from ..models.frontend_domain_verification_record import FrontendDomainVerificationRecord
        from ..models.project_custom_domain_target import ProjectCustomDomainTarget
        from ..models.project_function_custom_domain_function import ProjectFunctionCustomDomainFunction
        function_id = str(self.function_id)

        domain = self.domain

        tls_mode: str = self.tls_mode

        domain_status: str = self.domain_status

        verification_status: str = self.verification_status

        effective_urls = self.effective_urls



        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        target = self.target.to_dict()

        target_type: str = self.target_type

        function = self.function.to_dict()

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
            "function_id": function_id,
            "domain": domain,
            "tls_mode": tls_mode,
            "domain_status": domain_status,
            "verification_status": verification_status,
            "effective_urls": effective_urls,
            "created_at": created_at,
            "updated_at": updated_at,
            "target": target,
            "target_type": target_type,
            "function": function,
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
        from ..models.project_custom_domain_target import ProjectCustomDomainTarget
        from ..models.project_function_custom_domain_function import ProjectFunctionCustomDomainFunction
        d = dict(src_dict)
        function_id = UUID(d.pop("function_id"))




        domain = d.pop("domain")

        tls_mode = check_function_custom_domain_response_tls_mode(d.pop("tls_mode"))




        domain_status = check_function_custom_domain_response_domain_status(d.pop("domain_status"))




        verification_status = check_function_custom_domain_response_verification_status(d.pop("verification_status"))




        effective_urls = cast(list[str], d.pop("effective_urls"))


        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        target = ProjectCustomDomainTarget.from_dict(d.pop("target"))




        target_type = check_project_function_custom_domain_target_type(d.pop("target_type"))




        function = ProjectFunctionCustomDomainFunction.from_dict(d.pop("function"))




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




        project_function_custom_domain = cls(
            function_id=function_id,
            domain=domain,
            tls_mode=tls_mode,
            domain_status=domain_status,
            verification_status=verification_status,
            effective_urls=effective_urls,
            created_at=created_at,
            updated_at=updated_at,
            target=target,
            target_type=target_type,
            function=function,
            verification_records=verification_records,
            required_routing_record=required_routing_record,
        )


        project_function_custom_domain.additional_properties = d
        return project_function_custom_domain

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
