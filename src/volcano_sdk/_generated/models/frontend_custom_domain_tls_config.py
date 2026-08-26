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
    """ 
        Attributes:
            mode (FrontendCustomDomainTLSConfigMode): BYOC is mandatory for custom domain creation. Default: 'byoc'.
            certificate_pem (str): Required. PEM-encoded certificate.
            private_key_pem (str): Required. PEM-encoded private key.
            certificate_chain_pem (str | Unset): Optional PEM-encoded certificate chain.
     """

    certificate_pem: str
    private_key_pem: str
    mode: FrontendCustomDomainTLSConfigMode = 'byoc'
    certificate_chain_pem: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        mode: str = self.mode

        certificate_pem = self.certificate_pem

        private_key_pem = self.private_key_pem

        certificate_chain_pem = self.certificate_chain_pem


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "mode": mode,
            "certificate_pem": certificate_pem,
            "private_key_pem": private_key_pem,
        })
        if certificate_chain_pem is not UNSET:
            field_dict["certificate_chain_pem"] = certificate_chain_pem

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = check_frontend_custom_domain_tls_config_mode(d.pop("mode"))




        certificate_pem = d.pop("certificate_pem")

        private_key_pem = d.pop("private_key_pem")

        certificate_chain_pem = d.pop("certificate_chain_pem", UNSET)

        frontend_custom_domain_tls_config = cls(
            mode=mode,
            certificate_pem=certificate_pem,
            private_key_pem=private_key_pem,
            certificate_chain_pem=certificate_chain_pem,
        )


        frontend_custom_domain_tls_config.additional_properties = d
        return frontend_custom_domain_tls_config

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
