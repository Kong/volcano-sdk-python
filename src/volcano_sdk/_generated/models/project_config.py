from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_config_version import check_project_config_version
from ..models.project_config_version import ProjectConfigVersion
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_config_auth import ProjectConfigAuth
  from ..models.project_config_bucket import ProjectConfigBucket
  from ..models.project_config_database import ProjectConfigDatabase
  from ..models.project_config_frontend import ProjectConfigFrontend
  from ..models.project_config_function import ProjectConfigFunction
  from ..models.project_config_project import ProjectConfigProject
  from ..models.project_config_realtime import ProjectConfigRealtime
  from ..models.project_config_variable import ProjectConfigVariable





T = TypeVar("T", bound="ProjectConfig")



@_attrs_define
class ProjectConfig:
    """ Declarative project configuration manifest (the JSON form of
    volcano-config.yaml). Omitted sections are left untouched. Within
    declared entries, omitted optional fields keep their current server
    values (patch semantics). Declared collection keys are fully synced to
    the manifest: `variables`, `buckets[].policies`, `auth.providers.oauth`,
    `auth.email.templates`, and `functions[].schedulers` are reconciled to
    exactly match, deleting resources absent from the manifest. Functions,
    frontends, databases, and buckets are never created or deleted through
    this manifest; entries referencing resources that do not exist are
    skipped and reported.

        Attributes:
            version (ProjectConfigVersion): Manifest schema version. Must be 1.
            project (ProjectConfigProject | Unset): Project-level settings. `name` renames the project.
            databases (list[ProjectConfigDatabase] | Unset):
            shared_variables (list[str] | Unset): Replace the complete shared function-variable list with existing names,
                without changing variable values. Omission keeps membership unchanged; an empty list clears it.
            variables (list[ProjectConfigVariable] | Unset): Fully synced when declared - variables absent from this list
                are deleted.
            buckets (list[ProjectConfigBucket] | Unset):
            realtime (ProjectConfigRealtime | Unset):
            auth (ProjectConfigAuth | Unset): Authentication settings, grouped like the dashboard auth-settings tabs.
            functions (list[ProjectConfigFunction] | Unset):
            frontends (list[ProjectConfigFrontend] | Unset):
     """

    version: ProjectConfigVersion
    project: ProjectConfigProject | Unset = UNSET
    databases: list[ProjectConfigDatabase] | Unset = UNSET
    shared_variables: list[str] | Unset = UNSET
    variables: list[ProjectConfigVariable] | Unset = UNSET
    buckets: list[ProjectConfigBucket] | Unset = UNSET
    realtime: ProjectConfigRealtime | Unset = UNSET
    auth: ProjectConfigAuth | Unset = UNSET
    functions: list[ProjectConfigFunction] | Unset = UNSET
    frontends: list[ProjectConfigFrontend] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_auth import ProjectConfigAuth
        from ..models.project_config_bucket import ProjectConfigBucket
        from ..models.project_config_database import ProjectConfigDatabase
        from ..models.project_config_frontend import ProjectConfigFrontend
        from ..models.project_config_function import ProjectConfigFunction
        from ..models.project_config_project import ProjectConfigProject
        from ..models.project_config_realtime import ProjectConfigRealtime
        from ..models.project_config_variable import ProjectConfigVariable
        version: int = self.version

        project: dict[str, Any] | Unset = UNSET
        if not isinstance(self.project, Unset):
            project = self.project.to_dict()

        databases: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.databases, Unset):
            databases = []
            for databases_item_data in self.databases:
                databases_item = databases_item_data.to_dict()
                databases.append(databases_item)



        shared_variables: list[str] | Unset = UNSET
        if not isinstance(self.shared_variables, Unset):
            shared_variables = self.shared_variables



        variables: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = []
            for variables_item_data in self.variables:
                variables_item = variables_item_data.to_dict()
                variables.append(variables_item)



        buckets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.buckets, Unset):
            buckets = []
            for buckets_item_data in self.buckets:
                buckets_item = buckets_item_data.to_dict()
                buckets.append(buckets_item)



        realtime: dict[str, Any] | Unset = UNSET
        if not isinstance(self.realtime, Unset):
            realtime = self.realtime.to_dict()

        auth: dict[str, Any] | Unset = UNSET
        if not isinstance(self.auth, Unset):
            auth = self.auth.to_dict()

        functions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.functions, Unset):
            functions = []
            for functions_item_data in self.functions:
                functions_item = functions_item_data.to_dict()
                functions.append(functions_item)



        frontends: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.frontends, Unset):
            frontends = []
            for frontends_item_data in self.frontends:
                frontends_item = frontends_item_data.to_dict()
                frontends.append(frontends_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "version": version,
        })
        if project is not UNSET:
            field_dict["project"] = project
        if databases is not UNSET:
            field_dict["databases"] = databases
        if shared_variables is not UNSET:
            field_dict["shared_variables"] = shared_variables
        if variables is not UNSET:
            field_dict["variables"] = variables
        if buckets is not UNSET:
            field_dict["buckets"] = buckets
        if realtime is not UNSET:
            field_dict["realtime"] = realtime
        if auth is not UNSET:
            field_dict["auth"] = auth
        if functions is not UNSET:
            field_dict["functions"] = functions
        if frontends is not UNSET:
            field_dict["frontends"] = frontends

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_auth import ProjectConfigAuth
        from ..models.project_config_bucket import ProjectConfigBucket
        from ..models.project_config_database import ProjectConfigDatabase
        from ..models.project_config_frontend import ProjectConfigFrontend
        from ..models.project_config_function import ProjectConfigFunction
        from ..models.project_config_project import ProjectConfigProject
        from ..models.project_config_realtime import ProjectConfigRealtime
        from ..models.project_config_variable import ProjectConfigVariable
        d = dict(src_dict)
        version = check_project_config_version(d.pop("version"))




        _project = d.pop("project", UNSET)
        project: ProjectConfigProject | Unset
        if isinstance(_project,  Unset):
            project = UNSET
        else:
            project = ProjectConfigProject.from_dict(_project)




        _databases = d.pop("databases", UNSET)
        databases: list[ProjectConfigDatabase] | Unset = UNSET
        if _databases is not UNSET:
            databases = []
            for databases_item_data in _databases:
                databases_item = ProjectConfigDatabase.from_dict(databases_item_data)



                databases.append(databases_item)


        shared_variables = cast(list[str], d.pop("shared_variables", UNSET))


        _variables = d.pop("variables", UNSET)
        variables: list[ProjectConfigVariable] | Unset = UNSET
        if _variables is not UNSET:
            variables = []
            for variables_item_data in _variables:
                variables_item = ProjectConfigVariable.from_dict(variables_item_data)



                variables.append(variables_item)


        _buckets = d.pop("buckets", UNSET)
        buckets: list[ProjectConfigBucket] | Unset = UNSET
        if _buckets is not UNSET:
            buckets = []
            for buckets_item_data in _buckets:
                buckets_item = ProjectConfigBucket.from_dict(buckets_item_data)



                buckets.append(buckets_item)


        _realtime = d.pop("realtime", UNSET)
        realtime: ProjectConfigRealtime | Unset
        if isinstance(_realtime,  Unset):
            realtime = UNSET
        else:
            realtime = ProjectConfigRealtime.from_dict(_realtime)




        _auth = d.pop("auth", UNSET)
        auth: ProjectConfigAuth | Unset
        if isinstance(_auth,  Unset):
            auth = UNSET
        else:
            auth = ProjectConfigAuth.from_dict(_auth)




        _functions = d.pop("functions", UNSET)
        functions: list[ProjectConfigFunction] | Unset = UNSET
        if _functions is not UNSET:
            functions = []
            for functions_item_data in _functions:
                functions_item = ProjectConfigFunction.from_dict(functions_item_data)



                functions.append(functions_item)


        _frontends = d.pop("frontends", UNSET)
        frontends: list[ProjectConfigFrontend] | Unset = UNSET
        if _frontends is not UNSET:
            frontends = []
            for frontends_item_data in _frontends:
                frontends_item = ProjectConfigFrontend.from_dict(frontends_item_data)



                frontends.append(frontends_item)


        project_config = cls(
            version=version,
            project=project,
            databases=databases,
            shared_variables=shared_variables,
            variables=variables,
            buckets=buckets,
            realtime=realtime,
            auth=auth,
            functions=functions,
            frontends=frontends,
        )

        return project_config

