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
  from ..models.project_config_custom_domain_redirect import ProjectConfigCustomDomainRedirect





T = TypeVar("T", bound="ProjectConfigFrontendCustomDomain")



@_attrs_define
class ProjectConfigFrontendCustomDomain:
    """ One of the frontend's custom domains. `domain` and `tls` behave as in
    `custom_domain`. With `redirect`, the domain redirects every request to
    another listed domain that serves the frontend. While the list holds one
    domain, `redirect` has no domain to point at.

        Attributes:
            domain (str): Fully-qualified domain name (hostname only, no scheme/path). Managed TLS (`tls.mode: managed`)
                accepts at most 219 characters; BYOC accepts 253.
            tls (BYOCProjectConfigFrontendCustomDomainTLSConfig | ManagedProjectConfigFrontendCustomDomainTLSConfig |
                Unset): TLS for the custom domain. `mode` defaults to `byoc` when omitted.
            redirect (ProjectConfigCustomDomainRedirect | Unset):
     """

    domain: str
    tls: BYOCProjectConfigFrontendCustomDomainTLSConfig | ManagedProjectConfigFrontendCustomDomainTLSConfig | Unset = UNSET
    redirect: ProjectConfigCustomDomainRedirect | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.byoc_project_config_frontend_custom_domain_tls_config import BYOCProjectConfigFrontendCustomDomainTLSConfig # noqa: PLC0415
        from ..models.managed_project_config_frontend_custom_domain_tls_config import ManagedProjectConfigFrontendCustomDomainTLSConfig # noqa: PLC0415
        from ..models.project_config_custom_domain_redirect import ProjectConfigCustomDomainRedirect # noqa: PLC0415
        domain = self.domain

        tls: dict[str, Any] | Unset
        if isinstance(self.tls, Unset):
            tls = UNSET
        elif isinstance(self.tls, ManagedProjectConfigFrontendCustomDomainTLSConfig):
            tls = self.tls.to_dict()
        else:
            tls = self.tls.to_dict()


        redirect: dict[str, Any] | Unset = UNSET
        if not isinstance(self.redirect, Unset):
            redirect = self.redirect.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "domain": domain,
        })
        if tls is not UNSET:
            field_dict["tls"] = tls
        if redirect is not UNSET:
            field_dict["redirect"] = redirect

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.byoc_project_config_frontend_custom_domain_tls_config import BYOCProjectConfigFrontendCustomDomainTLSConfig # noqa: PLC0415
        from ..models.managed_project_config_frontend_custom_domain_tls_config import ManagedProjectConfigFrontendCustomDomainTLSConfig # noqa: PLC0415
        from ..models.project_config_custom_domain_redirect import ProjectConfigCustomDomainRedirect # noqa: PLC0415
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


        _redirect = d.pop("redirect", UNSET)
        redirect: ProjectConfigCustomDomainRedirect | Unset
        if isinstance(_redirect,  Unset):
            redirect = UNSET
        else:
            redirect = ProjectConfigCustomDomainRedirect.from_dict(_redirect)




        project_config_frontend_custom_domain = cls(
            domain=domain,
            tls=tls,
            redirect=redirect,
        )

        return project_config_frontend_custom_domain

