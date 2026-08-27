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
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






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
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            app_root (str | Unset): Optional relative POSIX path from the uploaded archive root to the Next.js app that is
                deployed.
            provisioning_started_at (datetime.datetime | Unset): Timestamp when the current provisioning phase started
            current_deployment_id (UUID | Unset): Identifier of the latest frontend deployment operation
            pending_deployment_id (UUID | Unset): Newest queued deployment that will run after the current operation
            site_url (str | Unset):
            custom_domain (str | Unset): Active custom domain hostname when configured
            custom_domain_status (FrontendCustomDomainStatus | Unset): Current custom domain lifecycle status
            last_invoked_at (datetime.datetime | Unset):
     """

    id: UUID
    project_id: UUID
    name: str
    framework: FrontendFramework
    status: FrontendStatus
    deployed_regions: list[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    app_root: str | Unset = UNSET
    provisioning_started_at: datetime.datetime | Unset = UNSET
    current_deployment_id: UUID | Unset = UNSET
    pending_deployment_id: UUID | Unset = UNSET
    site_url: str | Unset = UNSET
    custom_domain: str | Unset = UNSET
    custom_domain_status: FrontendCustomDomainStatus | Unset = UNSET
    last_invoked_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id = str(self.project_id)

        name = self.name

        framework: str = self.framework

        status: str = self.status

        deployed_regions = self.deployed_regions



        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

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
            "created_at": created_at,
            "updated_at": updated_at,
        })
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
        if last_invoked_at is not UNSET:
            field_dict["last_invoked_at"] = last_invoked_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        name = d.pop("name")

        framework = check_frontend_framework(d.pop("framework"))




        status = check_frontend_status(d.pop("status"))




        deployed_regions = cast(list[str], d.pop("deployed_regions"))


        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




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
            created_at=created_at,
            updated_at=updated_at,
            app_root=app_root,
            provisioning_started_at=provisioning_started_at,
            current_deployment_id=current_deployment_id,
            pending_deployment_id=pending_deployment_id,
            site_url=site_url,
            custom_domain=custom_domain,
            custom_domain_status=custom_domain_status,
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
