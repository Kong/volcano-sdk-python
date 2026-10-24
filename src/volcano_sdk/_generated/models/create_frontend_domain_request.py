from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.frontend_custom_domain_redirect_request import FrontendCustomDomainRedirectRequest
  from ..models.frontend_custom_domain_tls_config import FrontendCustomDomainTLSConfig





T = TypeVar("T", bound="CreateFrontendDomainRequest")



@_attrs_define
class CreateFrontendDomainRequest:
    """ 
        Attributes:
            domain (str): Fully-qualified domain name (hostname only, no scheme/path). Managed TLS (`tls.mode: managed`)
                accepts at most 219 characters; BYOC accepts 253. Example: www.example.com.
            tls (FrontendCustomDomainTLSConfig): TLS for a new custom domain. With `mode: managed`, Volcano issues and
                renews the certificate; omit every PEM field. With `mode: byoc`, send both `certificate_pem` and
                `private_key_pem`, plus an optional `certificate_chain_pem`.
            redirect (FrontendCustomDomainRedirectRequest | Unset): Redirects every request for the domain to `to`, another
                active domain of the same frontend that serves it, keeping the path and query string.
     """

    domain: str
    tls: FrontendCustomDomainTLSConfig
    redirect: FrontendCustomDomainRedirectRequest | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.frontend_custom_domain_redirect_request import FrontendCustomDomainRedirectRequest # noqa: PLC0415
        from ..models.frontend_custom_domain_tls_config import FrontendCustomDomainTLSConfig # noqa: PLC0415
        domain = self.domain

        tls = self.tls.to_dict()

        redirect: dict[str, Any] | Unset = UNSET
        if not isinstance(self.redirect, Unset):
            redirect = self.redirect.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "domain": domain,
            "tls": tls,
        })
        if redirect is not UNSET:
            field_dict["redirect"] = redirect

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.frontend_custom_domain_redirect_request import FrontendCustomDomainRedirectRequest # noqa: PLC0415
        from ..models.frontend_custom_domain_tls_config import FrontendCustomDomainTLSConfig # noqa: PLC0415
        d = dict(src_dict)
        domain = d.pop("domain")

        tls = FrontendCustomDomainTLSConfig.from_dict(d.pop("tls"))




        _redirect = d.pop("redirect", UNSET)
        redirect: FrontendCustomDomainRedirectRequest | Unset
        if isinstance(_redirect,  Unset):
            redirect = UNSET
        else:
            redirect = FrontendCustomDomainRedirectRequest.from_dict(_redirect)




        create_frontend_domain_request = cls(
            domain=domain,
            tls=tls,
            redirect=redirect,
        )

        return create_frontend_domain_request

