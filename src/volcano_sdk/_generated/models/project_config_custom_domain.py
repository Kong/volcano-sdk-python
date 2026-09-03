from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.byoc_project_config_frontend_custom_domain_tls_config import BYOCProjectConfigFrontendCustomDomainTLSConfig
  from ..models.managed_project_config_frontend_custom_domain_tls_config import ManagedProjectConfigFrontendCustomDomainTLSConfig





T = TypeVar("T", bound="ProjectConfigCustomDomain")



@_attrs_define
class ProjectConfigCustomDomain:
    """ Custom domain with managed or BYOC TLS (PRO plan). `tls` is required
    when the domain is first created and optional afterwards. BYOC TLS
    material is write-only and omitted from config export.

        Attributes:
            domain (str): Fully-qualified domain name (hostname only, no scheme/path)
            tls (BYOCProjectConfigFrontendCustomDomainTLSConfig | ManagedProjectConfigFrontendCustomDomainTLSConfig |
                Unset):
     """

    domain: str
    tls: BYOCProjectConfigFrontendCustomDomainTLSConfig | ManagedProjectConfigFrontendCustomDomainTLSConfig | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.byoc_project_config_frontend_custom_domain_tls_config import BYOCProjectConfigFrontendCustomDomainTLSConfig
        from ..models.managed_project_config_frontend_custom_domain_tls_config import ManagedProjectConfigFrontendCustomDomainTLSConfig
        domain = self.domain

        tls: dict[str, Any] | Unset
        if isinstance(self.tls, Unset):
            tls = UNSET
        elif isinstance(self.tls, ManagedProjectConfigFrontendCustomDomainTLSConfig):
            tls = self.tls.to_dict()
        else:
            tls = self.tls.to_dict()



        field_dict: dict[str, Any] = {}

        field_dict.update({
            "domain": domain,
        })
        if tls is not UNSET:
            field_dict["tls"] = tls

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.byoc_project_config_frontend_custom_domain_tls_config import BYOCProjectConfigFrontendCustomDomainTLSConfig
        from ..models.managed_project_config_frontend_custom_domain_tls_config import ManagedProjectConfigFrontendCustomDomainTLSConfig
        d = dict(src_dict)
        domain = d.pop("domain")

        def _parse_tls(data: object) -> BYOCProjectConfigFrontendCustomDomainTLSConfig | ManagedProjectConfigFrontendCustomDomainTLSConfig | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_project_config_frontend_custom_domain_tls_config_type_0 = ManagedProjectConfigFrontendCustomDomainTLSConfig.from_dict(data)



                return componentsschemas_project_config_frontend_custom_domain_tls_config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_project_config_frontend_custom_domain_tls_config_type_1 = BYOCProjectConfigFrontendCustomDomainTLSConfig.from_dict(data)



            return componentsschemas_project_config_frontend_custom_domain_tls_config_type_1

        tls = _parse_tls(d.pop("tls", UNSET))


        project_config_custom_domain = cls(
            domain=domain,
            tls=tls,
        )

        return project_config_custom_domain

