from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_config_frontend_variable_scope import check_project_config_frontend_variable_scope
from ..models.project_config_frontend_variable_scope import ProjectConfigFrontendVariableScope
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
            variable_scope (ProjectConfigFrontendVariableScope | Unset): All preserves access to all project variables.
                Shared includes the project frontend_shared_variables list. Scoped includes only explicitly declared variables
                in builds and runtime. Omission preserves the stored selection.
            variables (list[str] | Unset): Names selected when variable_scope is scoped. Missing declared values reject
                deployment. Omission preserves the stored list; an empty list clears it.
            custom_domain (ProjectConfigCustomDomain | Unset): Custom domain with BYOC TLS (PRO plan). `tls` is required
                when the
                domain is first created and optional afterwards: providing new TLS
                material for the same domain rotates the certificate in place (zero
                downtime); omitting `tls` keeps the stored certificate. TLS material is
                write-only and omitted from config export.
     """

    name: str
    variable_scope: ProjectConfigFrontendVariableScope | Unset = UNSET
    variables: list[str] | Unset = UNSET
    custom_domain: ProjectConfigCustomDomain | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_custom_domain import ProjectConfigCustomDomain
        name = self.name

        variable_scope: str | Unset = UNSET
        if not isinstance(self.variable_scope, Unset):
            variable_scope = self.variable_scope


        variables: list[str] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables



        custom_domain: dict[str, Any] | Unset = UNSET
        if not isinstance(self.custom_domain, Unset):
            custom_domain = self.custom_domain.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
        })
        if variable_scope is not UNSET:
            field_dict["variable_scope"] = variable_scope
        if variables is not UNSET:
            field_dict["variables"] = variables
        if custom_domain is not UNSET:
            field_dict["custom_domain"] = custom_domain

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_custom_domain import ProjectConfigCustomDomain
        d = dict(src_dict)
        name = d.pop("name")

        _variable_scope = d.pop("variable_scope", UNSET)
        variable_scope: ProjectConfigFrontendVariableScope | Unset
        if isinstance(_variable_scope,  Unset):
            variable_scope = UNSET
        else:
            variable_scope = check_project_config_frontend_variable_scope(_variable_scope)




        variables = cast(list[str], d.pop("variables", UNSET))


        _custom_domain = d.pop("custom_domain", UNSET)
        custom_domain: ProjectConfigCustomDomain | Unset
        if isinstance(_custom_domain,  Unset):
            custom_domain = UNSET
        else:
            custom_domain = ProjectConfigCustomDomain.from_dict(_custom_domain)




        project_config_frontend = cls(
            name=name,
            variable_scope=variable_scope,
            variables=variables,
            custom_domain=custom_domain,
        )

        return project_config_frontend

