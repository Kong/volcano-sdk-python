from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.frontend_custom_domain_tls_config import FrontendCustomDomainTLSConfig





T = TypeVar("T", bound="CreateFrontendCustomDomainRequest")



@_attrs_define
class CreateFrontendCustomDomainRequest:
    """ 
        Attributes:
            domain (str): Fully-qualified domain name (hostname only, no scheme/path) Example: app.example.com.
            tls (FrontendCustomDomainTLSConfig):
     """

    domain: str
    tls: FrontendCustomDomainTLSConfig
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.frontend_custom_domain_tls_config import FrontendCustomDomainTLSConfig
        domain = self.domain

        tls = self.tls.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "domain": domain,
            "tls": tls,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.frontend_custom_domain_tls_config import FrontendCustomDomainTLSConfig
        d = dict(src_dict)
        domain = d.pop("domain")

        tls = FrontendCustomDomainTLSConfig.from_dict(d.pop("tls"))




        create_frontend_custom_domain_request = cls(
            domain=domain,
            tls=tls,
        )


        create_frontend_custom_domain_request.additional_properties = d
        return create_frontend_custom_domain_request

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
