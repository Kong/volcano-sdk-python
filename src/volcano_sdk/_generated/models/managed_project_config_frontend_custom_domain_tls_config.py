from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_project_config_frontend_custom_domain_tls_config_mode import check_managed_project_config_frontend_custom_domain_tls_config_mode
from ..models.managed_project_config_frontend_custom_domain_tls_config_mode import ManagedProjectConfigFrontendCustomDomainTLSConfigMode
from typing import cast






T = TypeVar("T", bound="ManagedProjectConfigFrontendCustomDomainTLSConfig")



@_attrs_define
class ManagedProjectConfigFrontendCustomDomainTLSConfig:
    """ 
        Attributes:
            mode (ManagedProjectConfigFrontendCustomDomainTLSConfigMode):
     """

    mode: ManagedProjectConfigFrontendCustomDomainTLSConfigMode





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
        mode = check_managed_project_config_frontend_custom_domain_tls_config_mode(d.pop("mode"))




        managed_project_config_frontend_custom_domain_tls_config = cls(
            mode=mode,
        )

        return managed_project_config_frontend_custom_domain_tls_config

