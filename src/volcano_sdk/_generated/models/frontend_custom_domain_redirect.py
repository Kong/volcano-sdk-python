from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.frontend_custom_domain_redirect_status import check_frontend_custom_domain_redirect_status
from ..models.frontend_custom_domain_redirect_status import FrontendCustomDomainRedirectStatus
from typing import cast






T = TypeVar("T", bound="FrontendCustomDomainRedirect")



@_attrs_define
class FrontendCustomDomainRedirect:
    """ 
        Attributes:
            to (str): Hostname the domain redirects to.
            status (FrontendCustomDomainRedirectStatus):
     """

    to: str
    status: FrontendCustomDomainRedirectStatus
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        to = self.to

        status: int = self.status


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "to": to,
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        to = d.pop("to")

        status = check_frontend_custom_domain_redirect_status(d.pop("status"))




        frontend_custom_domain_redirect = cls(
            to=to,
            status=status,
        )


        frontend_custom_domain_redirect.additional_properties = d
        return frontend_custom_domain_redirect

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
