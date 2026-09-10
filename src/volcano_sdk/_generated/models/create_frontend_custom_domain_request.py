from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.byoc_frontend_custom_domain_tls_config import BYOCFrontendCustomDomainTLSConfig
  from ..models.managed_frontend_custom_domain_tls_config import ManagedFrontendCustomDomainTLSConfig





T = TypeVar("T", bound="CreateFrontendCustomDomainRequest")



@_attrs_define
class CreateFrontendCustomDomainRequest:
    """ 
        Attributes:
            domain (str): Fully-qualified domain name (hostname only, no scheme/path) Example: app.example.com.
            tls (BYOCFrontendCustomDomainTLSConfig | ManagedFrontendCustomDomainTLSConfig):
     """

    domain: str
    tls: BYOCFrontendCustomDomainTLSConfig | ManagedFrontendCustomDomainTLSConfig





    def to_dict(self) -> dict[str, Any]:
        from ..models.byoc_frontend_custom_domain_tls_config import BYOCFrontendCustomDomainTLSConfig
        from ..models.managed_frontend_custom_domain_tls_config import ManagedFrontendCustomDomainTLSConfig
        domain = self.domain

        tls: dict[str, Any]
        if isinstance(self.tls, ManagedFrontendCustomDomainTLSConfig):
            tls = self.tls.to_dict()
        else:
            tls = self.tls.to_dict()



        field_dict: dict[str, Any] = {}

        field_dict.update({
            "domain": domain,
            "tls": tls,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.byoc_frontend_custom_domain_tls_config import BYOCFrontendCustomDomainTLSConfig
        from ..models.managed_frontend_custom_domain_tls_config import ManagedFrontendCustomDomainTLSConfig
        d = dict(src_dict)
        domain = d.pop("domain")

        def _parse_tls(data: object) -> BYOCFrontendCustomDomainTLSConfig | ManagedFrontendCustomDomainTLSConfig:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_frontend_custom_domain_tls_config_type_0 = ManagedFrontendCustomDomainTLSConfig.from_dict(data)



                return componentsschemas_create_frontend_custom_domain_tls_config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_create_frontend_custom_domain_tls_config_type_1 = BYOCFrontendCustomDomainTLSConfig.from_dict(data)



            return componentsschemas_create_frontend_custom_domain_tls_config_type_1

        tls = _parse_tls(d.pop("tls"))


        create_frontend_custom_domain_request = cls(
            domain=domain,
            tls=tls,
        )

        return create_frontend_custom_domain_request

