from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.function_custom_domain_tls_config_mode import check_function_custom_domain_tls_config_mode
from ..models.function_custom_domain_tls_config_mode import FunctionCustomDomainTLSConfigMode
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="FunctionCustomDomainTLSConfig")



@_attrs_define
class FunctionCustomDomainTLSConfig:
    """ 
        Attributes:
            mode (FunctionCustomDomainTLSConfigMode):  Default: 'byoc'.
            certificate_pem (str):
            private_key_pem (str):
            certificate_chain_pem (str | Unset):
     """

    certificate_pem: str
    private_key_pem: str
    mode: FunctionCustomDomainTLSConfigMode = 'byoc'
    certificate_chain_pem: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        mode: str = self.mode

        certificate_pem = self.certificate_pem

        private_key_pem = self.private_key_pem

        certificate_chain_pem = self.certificate_chain_pem


        field_dict: dict[str, Any] = {}

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
        mode = check_function_custom_domain_tls_config_mode(d.pop("mode"))




        certificate_pem = d.pop("certificate_pem")

        private_key_pem = d.pop("private_key_pem")

        certificate_chain_pem = d.pop("certificate_chain_pem", UNSET)

        function_custom_domain_tls_config = cls(
            mode=mode,
            certificate_pem=certificate_pem,
            private_key_pem=private_key_pem,
            certificate_chain_pem=certificate_chain_pem,
        )

        return function_custom_domain_tls_config

