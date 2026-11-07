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
  from ..models.project_config_frontend_custom_domain import ProjectConfigFrontendCustomDomain
  from ..models.project_config_frontend_function_route import ProjectConfigFrontendFunctionRoute
  from ..models.project_config_frontend_route import ProjectConfigFrontendRoute





T = TypeVar("T", bound="ProjectConfigFrontend")



@_attrs_define
class ProjectConfigFrontend:
    """ Configuration for an existing (deployed) frontend. Frontends are never
    created or deleted through the manifest.

        Attributes:
            name (str):
            variable_scope (ProjectConfigFrontendVariableScope | Unset): All preserves access to all project variables.
                Shared includes the project frontend_shared_variables list. Scoped includes only explicitly declared variables
                in builds and runtime. Omission preserves the stored selection.
            variables (list[str] | Unset): Names selected when variable_scope is scoped. Missing declared values reject
                deployment. Omission preserves the stored list; an empty list clears it.
            custom_domain (None | ProjectConfigCustomDomain | Unset): The frontend's custom domain. Omission leaves an
                existing domain
                untouched; null deletes it. For a frontend with more than one
                domain, or a redirect, use `custom_domains`; an entry may not set
                both.
            custom_domains (list[ProjectConfigFrontendCustomDomain] | Unset): Complete set of the frontend's custom domains
                when declared.
                Domains not listed are deleted; an empty list deletes all of them.
                Omission leaves existing domains untouched. More than one domain
                needs a plan that allows it.
            function_routes (list[ProjectConfigFrontendFunctionRoute] | Unset): Complete set of same-origin Function path
                mappings when declared. Omission preserves existing mappings; an empty list deletes all mappings.
            frontend_routes (list[ProjectConfigFrontendRoute] | Unset): Complete set of paths this frontend serves from
                another frontend in the project when
                declared. Omission preserves existing routes; an empty list deletes all of them.
                Function and Frontend routes share one path namespace and the 64-route limit.
     """

    name: str
    variable_scope: ProjectConfigFrontendVariableScope | Unset = UNSET
    variables: list[str] | Unset = UNSET
    custom_domain: None | ProjectConfigCustomDomain | Unset = UNSET
    custom_domains: list[ProjectConfigFrontendCustomDomain] | Unset = UNSET
    function_routes: list[ProjectConfigFrontendFunctionRoute] | Unset = UNSET
    frontend_routes: list[ProjectConfigFrontendRoute] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_custom_domain import ProjectConfigCustomDomain # noqa: PLC0415
        from ..models.project_config_frontend_custom_domain import ProjectConfigFrontendCustomDomain # noqa: PLC0415
        from ..models.project_config_frontend_function_route import ProjectConfigFrontendFunctionRoute # noqa: PLC0415
        from ..models.project_config_frontend_route import ProjectConfigFrontendRoute # noqa: PLC0415
        name = self.name

        variable_scope: str | Unset = UNSET
        if not isinstance(self.variable_scope, Unset):
            variable_scope = self.variable_scope


        variables: list[str] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables



        custom_domain: dict[str, Any] | None | Unset
        if isinstance(self.custom_domain, Unset):
            custom_domain = UNSET
        elif isinstance(self.custom_domain, ProjectConfigCustomDomain):
            custom_domain = self.custom_domain.to_dict()
        else:
            custom_domain = self.custom_domain

        custom_domains: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.custom_domains, Unset):
            custom_domains = []
            for custom_domains_item_data in self.custom_domains:
                custom_domains_item = custom_domains_item_data.to_dict()
                custom_domains.append(custom_domains_item)



        function_routes: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.function_routes, Unset):
            function_routes = []
            for function_routes_item_data in self.function_routes:
                function_routes_item = function_routes_item_data.to_dict()
                function_routes.append(function_routes_item)



        frontend_routes: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.frontend_routes, Unset):
            frontend_routes = []
            for frontend_routes_item_data in self.frontend_routes:
                frontend_routes_item = frontend_routes_item_data.to_dict()
                frontend_routes.append(frontend_routes_item)




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
        if custom_domains is not UNSET:
            field_dict["custom_domains"] = custom_domains
        if function_routes is not UNSET:
            field_dict["function_routes"] = function_routes
        if frontend_routes is not UNSET:
            field_dict["frontend_routes"] = frontend_routes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_custom_domain import ProjectConfigCustomDomain # noqa: PLC0415
        from ..models.project_config_frontend_custom_domain import ProjectConfigFrontendCustomDomain # noqa: PLC0415
        from ..models.project_config_frontend_function_route import ProjectConfigFrontendFunctionRoute # noqa: PLC0415
        from ..models.project_config_frontend_route import ProjectConfigFrontendRoute # noqa: PLC0415
        d = dict(src_dict)
        name = d.pop("name")

        _variable_scope = d.pop("variable_scope", UNSET)
        variable_scope: ProjectConfigFrontendVariableScope | Unset
        if isinstance(_variable_scope,  Unset):
            variable_scope = UNSET
        else:
            variable_scope = check_project_config_frontend_variable_scope(_variable_scope)




        variables = cast(list[str], d.pop("variables", UNSET))


        def _parse_custom_domain(data: object) -> None | ProjectConfigCustomDomain | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                custom_domain_type_1 = ProjectConfigCustomDomain.from_dict(data)



                return custom_domain_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProjectConfigCustomDomain | Unset, data)

        custom_domain = _parse_custom_domain(d.pop("custom_domain", UNSET))


        _custom_domains = d.pop("custom_domains", UNSET)
        custom_domains: list[ProjectConfigFrontendCustomDomain] | Unset = UNSET
        if _custom_domains is not UNSET:
            custom_domains = []
            for custom_domains_item_data in _custom_domains:
                custom_domains_item = ProjectConfigFrontendCustomDomain.from_dict(custom_domains_item_data)



                custom_domains.append(custom_domains_item)


        _function_routes = d.pop("function_routes", UNSET)
        function_routes: list[ProjectConfigFrontendFunctionRoute] | Unset = UNSET
        if _function_routes is not UNSET:
            function_routes = []
            for function_routes_item_data in _function_routes:
                function_routes_item = ProjectConfigFrontendFunctionRoute.from_dict(function_routes_item_data)



                function_routes.append(function_routes_item)


        _frontend_routes = d.pop("frontend_routes", UNSET)
        frontend_routes: list[ProjectConfigFrontendRoute] | Unset = UNSET
        if _frontend_routes is not UNSET:
            frontend_routes = []
            for frontend_routes_item_data in _frontend_routes:
                frontend_routes_item = ProjectConfigFrontendRoute.from_dict(frontend_routes_item_data)



                frontend_routes.append(frontend_routes_item)


        project_config_frontend = cls(
            name=name,
            variable_scope=variable_scope,
            variables=variables,
            custom_domain=custom_domain,
            custom_domains=custom_domains,
            function_routes=function_routes,
            frontend_routes=frontend_routes,
        )

        return project_config_frontend

