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
            tls (FrontendCustomDomainTLSConfig): Set mode to managed for Volcano-issued TLS, or byoc with certificate_pem
                and private_key_pem.
     """

    domain: str
    tls: FrontendCustomDomainTLSConfig





    def to_dict(self) -> dict[str, Any]:
        from ..models.frontend_custom_domain_tls_config import FrontendCustomDomainTLSConfig
        domain = self.domain

        tls = self.tls.to_dict()


        field_dict: dict[str, Any] = {}

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

        return create_frontend_custom_domain_request

