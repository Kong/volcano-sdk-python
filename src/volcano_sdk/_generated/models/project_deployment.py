from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_deployment_deploy_source import check_project_deployment_deploy_source
from ..models.project_deployment_deploy_source import ProjectDeploymentDeploySource
from ..models.project_deployment_operation import check_project_deployment_operation
from ..models.project_deployment_operation import ProjectDeploymentOperation
from ..models.project_deployment_status import check_project_deployment_status
from ..models.project_deployment_status import ProjectDeploymentStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.deployment_progress import DeploymentProgress
  from ..models.project_deployment_resource import ProjectDeploymentResource





T = TypeVar("T", bound="ProjectDeployment")



@_attrs_define
class ProjectDeployment:
    """ A Function or Frontend deployment attempt in a project-scoped feed.

        Attributes:
            id (UUID):
            project_id (UUID):
            resource (ProjectDeploymentResource): The resource this deployment belongs to.
            operation (ProjectDeploymentOperation):
            status (ProjectDeploymentStatus):
            deploy_source (ProjectDeploymentDeploySource): What initiated this deployment.
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            artifact_version (str | Unset):
            error_message (str | Unset):
            completed_at (datetime.datetime | Unset):
            progress (DeploymentProgress | Unset): Normalized live progress derived from the deployment workflow and build
                phases.
     """

    id: UUID
    project_id: UUID
    resource: ProjectDeploymentResource
    operation: ProjectDeploymentOperation
    status: ProjectDeploymentStatus
    deploy_source: ProjectDeploymentDeploySource
    created_at: datetime.datetime
    updated_at: datetime.datetime
    artifact_version: str | Unset = UNSET
    error_message: str | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET
    progress: DeploymentProgress | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.deployment_progress import DeploymentProgress
        from ..models.project_deployment_resource import ProjectDeploymentResource
        id = str(self.id)

        project_id = str(self.project_id)

        resource = self.resource.to_dict()

        operation: str = self.operation

        status: str = self.status

        deploy_source: str = self.deploy_source

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        artifact_version = self.artifact_version

        error_message = self.error_message

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        progress: dict[str, Any] | Unset = UNSET
        if not isinstance(self.progress, Unset):
            progress = self.progress.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "project_id": project_id,
            "resource": resource,
            "operation": operation,
            "status": status,
            "deploy_source": deploy_source,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if artifact_version is not UNSET:
            field_dict["artifact_version"] = artifact_version
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if progress is not UNSET:
            field_dict["progress"] = progress

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.deployment_progress import DeploymentProgress
        from ..models.project_deployment_resource import ProjectDeploymentResource
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        resource = ProjectDeploymentResource.from_dict(d.pop("resource"))




        operation = check_project_deployment_operation(d.pop("operation"))




        status = check_project_deployment_status(d.pop("status"))




        deploy_source = check_project_deployment_deploy_source(d.pop("deploy_source"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        artifact_version = d.pop("artifact_version", UNSET)

        error_message = d.pop("error_message", UNSET)

        _completed_at = d.pop("completed_at", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at,  Unset):
            completed_at = UNSET
        else:
            completed_at = datetime.datetime.fromisoformat(_completed_at)




        _progress = d.pop("progress", UNSET)
        progress: DeploymentProgress | Unset
        if isinstance(_progress,  Unset):
            progress = UNSET
        else:
            progress = DeploymentProgress.from_dict(_progress)




        project_deployment = cls(
            id=id,
            project_id=project_id,
            resource=resource,
            operation=operation,
            status=status,
            deploy_source=deploy_source,
            created_at=created_at,
            updated_at=updated_at,
            artifact_version=artifact_version,
            error_message=error_message,
            completed_at=completed_at,
            progress=progress,
        )


        project_deployment.additional_properties = d
        return project_deployment

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
