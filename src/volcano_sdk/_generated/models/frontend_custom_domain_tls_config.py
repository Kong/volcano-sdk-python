from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.frontend_custom_domain_tls_config_mode import check_frontend_custom_domain_tls_config_mode
from ..models.frontend_custom_domain_tls_config_mode import FrontendCustomDomainTLSConfigMode
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="FrontendCustomDomainTLSConfig")



@_attrs_define
class FrontendCustomDomainTLSConfig:
    """ TLS for a new custom domain. With `mode: managed`, Volcano issues and renews the certificate; omit every PEM field.
    With `mode: byoc`, send both `certificate_pem` and `private_key_pem`, plus an optional `certificate_chain_pem`.

        Attributes:
            mode (FrontendCustomDomainTLSConfigMode): managed for a Volcano-issued certificate; byoc to supply your own.
            certificate_pem (str | Unset): PEM-encoded certificate. Required when mode is byoc; not allowed when mode is
                managed.
            private_key_pem (str | Unset): PEM-encoded private key. Required when mode is byoc; not allowed when mode is
                managed.
            certificate_chain_pem (str | Unset): Optional PEM-encoded certificate chain when mode is byoc; not allowed when
                mode is managed.
     """

    mode: FrontendCustomDomainTLSConfigMode
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
        mode = check_frontend_custom_domain_tls_config_mode(d.pop("mode"))




        certificate_pem = d.pop("certificate_pem", UNSET)

        private_key_pem = d.pop("private_key_pem", UNSET)

        certificate_chain_pem = d.pop("certificate_chain_pem", UNSET)

        frontend_custom_domain_tls_config = cls(
            mode=mode,
            certificate_pem=certificate_pem,
            private_key_pem=private_key_pem,
            certificate_chain_pem=certificate_chain_pem,
        )

        return frontend_custom_domain_tls_config

