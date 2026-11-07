from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.frontend_custom_domain_status import check_frontend_custom_domain_status
from ..models.frontend_custom_domain_status import FrontendCustomDomainStatus
from ..models.frontend_framework import check_frontend_framework
from ..models.frontend_framework import FrontendFramework
from ..models.frontend_status import check_frontend_status
from ..models.frontend_status import FrontendStatus
from ..models.frontend_variable_scope import check_frontend_variable_scope
from ..models.frontend_variable_scope import FrontendVariableScope
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.frontend_function_route import FrontendFunctionRoute
  from ..models.frontend_route import FrontendRoute





T = TypeVar("T", bound="Frontend")



@_attrs_define
class Frontend:
    """ 
        Attributes:
            id (UUID):
            project_id (UUID):
            name (str):
            framework (FrontendFramework):
            status (FrontendStatus): Frontend lifecycle status. `degraded` means the regional runtime remains
                available but edge synchronization exhausted its immediate retries; Volcano
                retries edge recovery without rebuilding the frontend, and stops once a new
                deployment is queued or the retry budget runs out, leaving the frontend
                `degraded` until the next redeploy. A redeploy that fails over a serving
                frontend stays `active` on the previous deployment, so `failed` means no
                deployment is serving.
            deployed_regions (list[str]):
            serving_candidate_id (None | UUID): The promoted Candidate whose runtime receives this frontend's traffic, the
                same as
                `candidate_id` in `serving`. Null when the frontend serves its own runtime. While it is
                set, `current_deployment_id` and `status` describe a deployment that receives no traffic,
                and deploying the frontend is refused until it is rolled back.
            function_routes (list[FrontendFunctionRoute]): Paths on this frontend that forward to a public function, ordered
                from most to least specific. Anyone who can load the frontend can
                reach the target function at these paths without a credential.
            frontend_routes (list[FrontendRoute]): Paths on this frontend served by another frontend in the project,
                ordered from most to least specific. Function and Frontend routes
                share one path namespace and the 64-route limit.
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            variable_scope (FrontendVariableScope | Unset): All preserves access to all project variables. Shared includes
                the project frontend shared-variable list. Scoped includes only explicitly declared variables in builds and
                runtime. Omission preserves the stored selection.
            declared_variables (list[str] | Unset): Names selected when variable_scope is scoped. Missing declared values
                reject deployment. Omission preserves the stored list; an empty list clears it.
            app_root (str | Unset): Optional relative POSIX path from the uploaded archive root to the Next.js app that is
                deployed.
            provisioning_started_at (datetime.datetime | Unset): Timestamp when the current provisioning phase started
            current_deployment_id (UUID | Unset): Identifier of the latest frontend deployment operation
            pending_deployment_id (UUID | Unset): Newest queued deployment that will run after the current operation
            site_url (str | Unset):
            custom_domain (str | Unset): Active custom domain hostname when configured
            custom_domain_status (FrontendCustomDomainStatus | Unset): Current custom domain lifecycle status
            last_deployed_at (datetime.datetime | Unset): Recorded completion time of the most recent deploy or redeploy
                with status active. Omitted when no such deployment has a recorded completion time. Site traffic, pending
                deployments, degraded deployments, failed deployments, and deletion do not change this value.
            last_invoked_at (datetime.datetime | Unset):
     """

    id: UUID
    project_id: UUID
    name: str
    framework: FrontendFramework
    status: FrontendStatus
    deployed_regions: list[str]
    serving_candidate_id: None | UUID
    function_routes: list[FrontendFunctionRoute]
    frontend_routes: list[FrontendRoute]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    variable_scope: FrontendVariableScope | Unset = UNSET
    declared_variables: list[str] | Unset = UNSET
    app_root: str | Unset = UNSET
    provisioning_started_at: datetime.datetime | Unset = UNSET
    current_deployment_id: UUID | Unset = UNSET
    pending_deployment_id: UUID | Unset = UNSET
    site_url: str | Unset = UNSET
    custom_domain: str | Unset = UNSET
    custom_domain_status: FrontendCustomDomainStatus | Unset = UNSET
    last_deployed_at: datetime.datetime | Unset = UNSET
    last_invoked_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.frontend_function_route import FrontendFunctionRoute # noqa: PLC0415
        from ..models.frontend_route import FrontendRoute # noqa: PLC0415
        id = str(self.id)

        project_id = str(self.project_id)

        name = self.name

        framework: str = self.framework

        status: str = self.status

        deployed_regions = self.deployed_regions



        serving_candidate_id: None | str
        if isinstance(self.serving_candidate_id, UUID):
            serving_candidate_id = str(self.serving_candidate_id)
        else:
            serving_candidate_id = self.serving_candidate_id

        function_routes = []
        for function_routes_item_data in self.function_routes:
            function_routes_item = function_routes_item_data.to_dict()
            function_routes.append(function_routes_item)



        frontend_routes = []
        for frontend_routes_item_data in self.frontend_routes:
            frontend_routes_item = frontend_routes_item_data.to_dict()
            frontend_routes.append(frontend_routes_item)



        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        variable_scope: str | Unset = UNSET
        if not isinstance(self.variable_scope, Unset):
            variable_scope = self.variable_scope


        declared_variables: list[str] | Unset = UNSET
        if not isinstance(self.declared_variables, Unset):
            declared_variables = self.declared_variables



        app_root = self.app_root

        provisioning_started_at: str | Unset = UNSET
        if not isinstance(self.provisioning_started_at, Unset):
            provisioning_started_at = self.provisioning_started_at.isoformat()

        current_deployment_id: str | Unset = UNSET
        if not isinstance(self.current_deployment_id, Unset):
            current_deployment_id = str(self.current_deployment_id)

        pending_deployment_id: str | Unset = UNSET
        if not isinstance(self.pending_deployment_id, Unset):
            pending_deployment_id = str(self.pending_deployment_id)

        site_url = self.site_url

        custom_domain = self.custom_domain

        custom_domain_status: str | Unset = UNSET
        if not isinstance(self.custom_domain_status, Unset):
            custom_domain_status = self.custom_domain_status


        last_deployed_at: str | Unset = UNSET
        if not isinstance(self.last_deployed_at, Unset):
            last_deployed_at = self.last_deployed_at.isoformat()

        last_invoked_at: str | Unset = UNSET
        if not isinstance(self.last_invoked_at, Unset):
            last_invoked_at = self.last_invoked_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "project_id": project_id,
            "name": name,
            "framework": framework,
            "status": status,
            "deployed_regions": deployed_regions,
            "serving_candidate_id": serving_candidate_id,
            "function_routes": function_routes,
            "frontend_routes": frontend_routes,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if variable_scope is not UNSET:
            field_dict["variable_scope"] = variable_scope
        if declared_variables is not UNSET:
            field_dict["declared_variables"] = declared_variables
        if app_root is not UNSET:
            field_dict["app_root"] = app_root
        if provisioning_started_at is not UNSET:
            field_dict["provisioning_started_at"] = provisioning_started_at
        if current_deployment_id is not UNSET:
            field_dict["current_deployment_id"] = current_deployment_id
        if pending_deployment_id is not UNSET:
            field_dict["pending_deployment_id"] = pending_deployment_id
        if site_url is not UNSET:
            field_dict["site_url"] = site_url
        if custom_domain is not UNSET:
            field_dict["custom_domain"] = custom_domain
        if custom_domain_status is not UNSET:
            field_dict["custom_domain_status"] = custom_domain_status
        if last_deployed_at is not UNSET:
            field_dict["last_deployed_at"] = last_deployed_at
        if last_invoked_at is not UNSET:
            field_dict["last_invoked_at"] = last_invoked_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.frontend_function_route import FrontendFunctionRoute # noqa: PLC0415
        from ..models.frontend_route import FrontendRoute # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        name = d.pop("name")

        framework = check_frontend_framework(d.pop("framework"))




        status = check_frontend_status(d.pop("status"))




        deployed_regions = cast(list[str], d.pop("deployed_regions"))


        def _parse_serving_candidate_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                serving_candidate_id_type_0 = UUID(data)



                return serving_candidate_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        serving_candidate_id = _parse_serving_candidate_id(d.pop("serving_candidate_id"))


        function_routes = []
        _function_routes = d.pop("function_routes")
        for function_routes_item_data in (_function_routes):
            function_routes_item = FrontendFunctionRoute.from_dict(function_routes_item_data)



            function_routes.append(function_routes_item)


        frontend_routes = []
        _frontend_routes = d.pop("frontend_routes")
        for frontend_routes_item_data in (_frontend_routes):
            frontend_routes_item = FrontendRoute.from_dict(frontend_routes_item_data)



            frontend_routes.append(frontend_routes_item)


        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        _variable_scope = d.pop("variable_scope", UNSET)
        variable_scope: FrontendVariableScope | Unset
        if isinstance(_variable_scope,  Unset):
            variable_scope = UNSET
        else:
            variable_scope = check_frontend_variable_scope(_variable_scope)




        declared_variables = cast(list[str], d.pop("declared_variables", UNSET))


        app_root = d.pop("app_root", UNSET)

        _provisioning_started_at = d.pop("provisioning_started_at", UNSET)
        provisioning_started_at: datetime.datetime | Unset
        if isinstance(_provisioning_started_at,  Unset):
            provisioning_started_at = UNSET
        else:
            provisioning_started_at = datetime.datetime.fromisoformat(_provisioning_started_at)




        _current_deployment_id = d.pop("current_deployment_id", UNSET)
        current_deployment_id: UUID | Unset
        if isinstance(_current_deployment_id,  Unset):
            current_deployment_id = UNSET
        else:
            current_deployment_id = UUID(_current_deployment_id)




        _pending_deployment_id = d.pop("pending_deployment_id", UNSET)
        pending_deployment_id: UUID | Unset
        if isinstance(_pending_deployment_id,  Unset):
            pending_deployment_id = UNSET
        else:
            pending_deployment_id = UUID(_pending_deployment_id)




        site_url = d.pop("site_url", UNSET)

        custom_domain = d.pop("custom_domain", UNSET)

        _custom_domain_status = d.pop("custom_domain_status", UNSET)
        custom_domain_status: FrontendCustomDomainStatus | Unset
        if isinstance(_custom_domain_status,  Unset):
            custom_domain_status = UNSET
        else:
            custom_domain_status = check_frontend_custom_domain_status(_custom_domain_status)




        _last_deployed_at = d.pop("last_deployed_at", UNSET)
        last_deployed_at: datetime.datetime | Unset
        if isinstance(_last_deployed_at,  Unset):
            last_deployed_at = UNSET
        else:
            last_deployed_at = datetime.datetime.fromisoformat(_last_deployed_at)




        _last_invoked_at = d.pop("last_invoked_at", UNSET)
        last_invoked_at: datetime.datetime | Unset
        if isinstance(_last_invoked_at,  Unset):
            last_invoked_at = UNSET
        else:
            last_invoked_at = datetime.datetime.fromisoformat(_last_invoked_at)




        frontend = cls(
            id=id,
            project_id=project_id,
            name=name,
            framework=framework,
            status=status,
            deployed_regions=deployed_regions,
            serving_candidate_id=serving_candidate_id,
            function_routes=function_routes,
            frontend_routes=frontend_routes,
            created_at=created_at,
            updated_at=updated_at,
            variable_scope=variable_scope,
            declared_variables=declared_variables,
            app_root=app_root,
            provisioning_started_at=provisioning_started_at,
            current_deployment_id=current_deployment_id,
            pending_deployment_id=pending_deployment_id,
            site_url=site_url,
            custom_domain=custom_domain,
            custom_domain_status=custom_domain_status,
            last_deployed_at=last_deployed_at,
            last_invoked_at=last_invoked_at,
        )


        frontend.additional_properties = d
        return frontend

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
