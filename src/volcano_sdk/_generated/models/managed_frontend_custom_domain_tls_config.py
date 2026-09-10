from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_frontend_custom_domain_tls_config_mode import check_managed_frontend_custom_domain_tls_config_mode
from ..models.managed_frontend_custom_domain_tls_config_mode import ManagedFrontendCustomDomainTLSConfigMode
from typing import cast






T = TypeVar("T", bound="ManagedFrontendCustomDomainTLSConfig")



@_attrs_define
class ManagedFrontendCustomDomainTLSConfig:
    """ Volcano issues and renews the certificate. Do not send certificate material.

        Attributes:
            mode (ManagedFrontendCustomDomainTLSConfigMode):
     """

    mode: ManagedFrontendCustomDomainTLSConfigMode





    def to_dict(self) -> dict[str, Any]:
        mode: str = self.mode


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "mode": mode,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = check_managed_frontend_custom_domain_tls_config_mode(d.pop("mode"))




        managed_frontend_custom_domain_tls_config = cls(
            mode=mode,
        )

        return managed_frontend_custom_domain_tls_config

