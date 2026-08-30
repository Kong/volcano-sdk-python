from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.function_custom_domain_tls_config import FunctionCustomDomainTLSConfig





T = TypeVar("T", bound="ConfigureFunctionCustomDomainRequest")



@_attrs_define
class ConfigureFunctionCustomDomainRequest:
    """ 
        Attributes:
            domain (str): Fully-qualified hostname only, without a scheme, port, or path. Example: api.example.com.
            tls (FunctionCustomDomainTLSConfig):
     """

    domain: str
    tls: FunctionCustomDomainTLSConfig





    def to_dict(self) -> dict[str, Any]:
        from ..models.function_custom_domain_tls_config import FunctionCustomDomainTLSConfig
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
        from ..models.function_custom_domain_tls_config import FunctionCustomDomainTLSConfig
        d = dict(src_dict)
        domain = d.pop("domain")

        tls = FunctionCustomDomainTLSConfig.from_dict(d.pop("tls"))




        configure_function_custom_domain_request = cls(
            domain=domain,
            tls=tls,
        )

        return configure_function_custom_domain_request

