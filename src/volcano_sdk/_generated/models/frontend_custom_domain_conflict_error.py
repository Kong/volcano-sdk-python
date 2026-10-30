from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.frontend_domain_verification_record import FrontendDomainVerificationRecord





T = TypeVar("T", bound="FrontendCustomDomainConflictError")



@_attrs_define
class FrontendCustomDomainConflictError:
    """ Domain ownership conflict. With `code: ownership_verification_required`, the account has not proven it owns the
    domain: publish `required_record` in DNS and send the same request again. The retry succeeds once Volcano can see
    the record. With `code: custom_domain_releasing`, a removed domain still holds the hostname or the frontend while
    Volcano releases it: send the same request again after the response's `Retry-After` seconds. A release that will not
    finish within a few minutes is a plain conflict. Other conflicts omit both fields.

        Attributes:
            error (str):
            code (str | Unset): Stable machine-readable error code when a specific recovery path is available.
                `plan_required` (403) means the project owner's plan does not include the requested feature or option; upgrading
                the plan unlocks it. A 403 without a code leaves the reason unspecified: it can be an access refusal, a reached
                limit, or a plan check that could not read the owner's plan. Match on the code, not the message text.
            required_record (FrontendDomainVerificationRecord | Unset): The DNS records currently required. Volcano may
                require an account-specific TXT ownership record for the hostname's domain before returning a CNAME that
                authorizes managed certificate issuance and renewal. Clients must follow the records returned for the current
                lifecycle state instead of assuming a fixed sequence.
     """

    error: str
    code: str | Unset = UNSET
    required_record: FrontendDomainVerificationRecord | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.frontend_domain_verification_record import FrontendDomainVerificationRecord # noqa: PLC0415
        error = self.error

        code = self.code

        required_record: dict[str, Any] | Unset = UNSET
        if not isinstance(self.required_record, Unset):
            required_record = self.required_record.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "error": error,
        })
        if code is not UNSET:
            field_dict["code"] = code
        if required_record is not UNSET:
            field_dict["required_record"] = required_record

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.frontend_domain_verification_record import FrontendDomainVerificationRecord # noqa: PLC0415
        d = dict(src_dict)
        error = d.pop("error")

        code = d.pop("code", UNSET)

        _required_record = d.pop("required_record", UNSET)
        required_record: FrontendDomainVerificationRecord | Unset
        if isinstance(_required_record,  Unset):
            required_record = UNSET
        else:
            required_record = FrontendDomainVerificationRecord.from_dict(_required_record)




        frontend_custom_domain_conflict_error = cls(
            error=error,
            code=code,
            required_record=required_record,
        )


        frontend_custom_domain_conflict_error.additional_properties = d
        return frontend_custom_domain_conflict_error

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
