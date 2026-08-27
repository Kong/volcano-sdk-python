from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.frontend_custom_domain_tls_config import FrontendCustomDomainTLSConfig





T = TypeVar("T", bound="ProjectConfigCustomDomain")



@_attrs_define
class ProjectConfigCustomDomain:
    """ Custom domain with BYOC TLS (PRO plan). `tls` is required when the
    domain is first created and optional afterwards: providing new TLS
    material for the same domain rotates the certificate in place (zero
    downtime); omitting `tls` keeps the stored certificate. TLS material is
    write-only and omitted from config export.

        Attributes:
            domain (str): Fully-qualified domain name (hostname only, no scheme/path)
            tls (FrontendCustomDomainTLSConfig | Unset):
     """

    domain: str
    tls: FrontendCustomDomainTLSConfig | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.frontend_custom_domain_tls_config import FrontendCustomDomainTLSConfig
        domain = self.domain

        tls: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tls, Unset):
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
        from ..models.frontend_custom_domain_tls_config import FrontendCustomDomainTLSConfig
        d = dict(src_dict)
        domain = d.pop("domain")

        _tls = d.pop("tls", UNSET)
        tls: FrontendCustomDomainTLSConfig | Unset
        if isinstance(_tls,  Unset):
            tls = UNSET
        else:
            tls = FrontendCustomDomainTLSConfig.from_dict(_tls)




        project_config_custom_domain = cls(
            domain=domain,
            tls=tls,
        )

        return project_config_custom_domain

