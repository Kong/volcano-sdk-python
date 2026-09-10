from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_config_custom_domain import ProjectConfigCustomDomain





T = TypeVar("T", bound="ProjectConfigFrontend")



@_attrs_define
class ProjectConfigFrontend:
    """ Configuration for an existing (deployed) frontend. Frontends are never
    created or deleted through the manifest. A declared frontend entry
    without `custom_domain` deletes an existing custom domain.

        Attributes:
            name (str):
            custom_domain (ProjectConfigCustomDomain | Unset): Custom domain with managed or BYOC TLS (PRO plan). `tls` is
                required
                when the domain is first created and optional afterwards. BYOC TLS
                material is write-only and omitted from config export.
     """

    name: str
    custom_domain: ProjectConfigCustomDomain | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_custom_domain import ProjectConfigCustomDomain
        name = self.name

        custom_domain: dict[str, Any] | Unset = UNSET
        if not isinstance(self.custom_domain, Unset):
            custom_domain = self.custom_domain.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
        })
        if custom_domain is not UNSET:
            field_dict["custom_domain"] = custom_domain

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_custom_domain import ProjectConfigCustomDomain
        d = dict(src_dict)
        name = d.pop("name")

        _custom_domain = d.pop("custom_domain", UNSET)
        custom_domain: ProjectConfigCustomDomain | Unset
        if isinstance(_custom_domain,  Unset):
            custom_domain = UNSET
        else:
            custom_domain = ProjectConfigCustomDomain.from_dict(_custom_domain)




        project_config_frontend = cls(
            name=name,
            custom_domain=custom_domain,
        )

        return project_config_frontend

