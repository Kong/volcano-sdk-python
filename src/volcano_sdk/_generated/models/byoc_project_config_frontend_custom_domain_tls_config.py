from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.byoc_project_config_frontend_custom_domain_tls_config_mode import BYOCProjectConfigFrontendCustomDomainTLSConfigMode
from ..models.byoc_project_config_frontend_custom_domain_tls_config_mode import check_byoc_project_config_frontend_custom_domain_tls_config_mode
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="BYOCProjectConfigFrontendCustomDomainTLSConfig")



@_attrs_define
class BYOCProjectConfigFrontendCustomDomainTLSConfig:
    """ 
        Attributes:
            mode (BYOCProjectConfigFrontendCustomDomainTLSConfigMode):
            certificate_pem (str | Unset): PEM-encoded certificate for BYOC create or rotation. Omitted from exports.
            private_key_pem (str | Unset): PEM-encoded private key for BYOC create or rotation. Omitted from exports.
            certificate_chain_pem (str | Unset): Optional PEM-encoded certificate chain for BYOC. Omitted from exports.
     """

    mode: BYOCProjectConfigFrontendCustomDomainTLSConfigMode
    certificate_pem: str | Unset = UNSET
    private_key_pem: str | Unset = UNSET
    certificate_chain_pem: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        mode: str = self.mode

        certificate_pem = self.certificate_pem

        private_key_pem = self.private_key_pem

        certificate_chain_pem = self.certificate_chain_pem


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "mode": mode,
        })
        if certificate_pem is not UNSET:
            field_dict["certificate_pem"] = certificate_pem
        if private_key_pem is not UNSET:
            field_dict["private_key_pem"] = private_key_pem
        if certificate_chain_pem is not UNSET:
            field_dict["certificate_chain_pem"] = certificate_chain_pem

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = check_byoc_project_config_frontend_custom_domain_tls_config_mode(d.pop("mode"))




        certificate_pem = d.pop("certificate_pem", UNSET)

        private_key_pem = d.pop("private_key_pem", UNSET)

        certificate_chain_pem = d.pop("certificate_chain_pem", UNSET)

        byoc_project_config_frontend_custom_domain_tls_config = cls(
            mode=mode,
            certificate_pem=certificate_pem,
            private_key_pem=private_key_pem,
            certificate_chain_pem=certificate_chain_pem,
        )

        return byoc_project_config_frontend_custom_domain_tls_config

