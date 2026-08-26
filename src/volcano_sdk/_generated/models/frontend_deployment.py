from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.frontend_deployment_deploy_source import check_frontend_deployment_deploy_source
from ..models.frontend_deployment_deploy_source import FrontendDeploymentDeploySource
from ..models.frontend_deployment_operation import check_frontend_deployment_operation
from ..models.frontend_deployment_operation import FrontendDeploymentOperation
from ..models.frontend_deployment_status import check_frontend_deployment_status
from ..models.frontend_deployment_status import FrontendDeploymentStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.deployment_progress import DeploymentProgress





T = TypeVar("T", bound="FrontendDeployment")



@_attrs_define
class FrontendDeployment:
    """ 
        Attributes:
            id (UUID):
            frontend_id (UUID):
            project_id (UUID):
            operation (FrontendDeploymentOperation):
            status (FrontendDeploymentStatus): Deployment lifecycle status. A `degraded` redeploy remains available while
                edge-only recovery is retried. A `failed` redeploy is recorded here while the
                frontend keeps serving its previous deployment.
            deploy_source (FrontendDeploymentDeploySource): What initiated this deployment.
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            initiated_by (str | Unset): Platform user that triggered a request-initiated deployment; absent for git and
                system deployments.
            artifact_bucket (str | Unset):
            artifact_key (str | Unset):
            artifact_version (str | Unset):
            site_url (str | Unset):
            cloudformation_stack_id (str | Unset):
            cloudformation_stack_url (str | Unset):
            codebuild_duration_seconds (int | Unset): Total CodeBuild build duration recorded for this deployment, in
                seconds.
            codebuild_build_count (int | Unset): Number of completed CodeBuild builds included in
                codebuild_duration_seconds.
            codebuild_duration_recorded_at (datetime.datetime | Unset):
            progress (DeploymentProgress | Unset): Normalized live progress derived from the deployment workflow and build
                phases.
            error_message (str | Unset):
     """

    id: UUID
    frontend_id: UUID
    project_id: UUID
    operation: FrontendDeploymentOperation
    status: FrontendDeploymentStatus
    deploy_source: FrontendDeploymentDeploySource
    created_at: datetime.datetime
    updated_at: datetime.datetime
    initiated_by: str | Unset = UNSET
    artifact_bucket: str | Unset = UNSET
    artifact_key: str | Unset = UNSET
    artifact_version: str | Unset = UNSET
    site_url: str | Unset = UNSET
    cloudformation_stack_id: str | Unset = UNSET
    cloudformation_stack_url: str | Unset = UNSET
    codebuild_duration_seconds: int | Unset = UNSET
    codebuild_build_count: int | Unset = UNSET
    codebuild_duration_recorded_at: datetime.datetime | Unset = UNSET
    progress: DeploymentProgress | Unset = UNSET
    error_message: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.deployment_progress import DeploymentProgress
        id = str(self.id)

        frontend_id = str(self.frontend_id)

        project_id = str(self.project_id)

        operation: str = self.operation

        status: str = self.status

        deploy_source: str = self.deploy_source

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        initiated_by = self.initiated_by

        artifact_bucket = self.artifact_bucket

        artifact_key = self.artifact_key

        artifact_version = self.artifact_version

        site_url = self.site_url

        cloudformation_stack_id = self.cloudformation_stack_id

        cloudformation_stack_url = self.cloudformation_stack_url

        codebuild_duration_seconds = self.codebuild_duration_seconds

        codebuild_build_count = self.codebuild_build_count

        codebuild_duration_recorded_at: str | Unset = UNSET
        if not isinstance(self.codebuild_duration_recorded_at, Unset):
            codebuild_duration_recorded_at = self.codebuild_duration_recorded_at.isoformat()

        progress: dict[str, Any] | Unset = UNSET
        if not isinstance(self.progress, Unset):
            progress = self.progress.to_dict()

        error_message = self.error_message


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "frontend_id": frontend_id,
            "project_id": project_id,
            "operation": operation,
            "status": status,
            "deploy_source": deploy_source,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if initiated_by is not UNSET:
            field_dict["initiated_by"] = initiated_by
        if artifact_bucket is not UNSET:
            field_dict["artifact_bucket"] = artifact_bucket
        if artifact_key is not UNSET:
            field_dict["artifact_key"] = artifact_key
        if artifact_version is not UNSET:
            field_dict["artifact_version"] = artifact_version
        if site_url is not UNSET:
            field_dict["site_url"] = site_url
        if cloudformation_stack_id is not UNSET:
            field_dict["cloudformation_stack_id"] = cloudformation_stack_id
        if cloudformation_stack_url is not UNSET:
            field_dict["cloudformation_stack_url"] = cloudformation_stack_url
        if codebuild_duration_seconds is not UNSET:
            field_dict["codebuild_duration_seconds"] = codebuild_duration_seconds
        if codebuild_build_count is not UNSET:
            field_dict["codebuild_build_count"] = codebuild_build_count
        if codebuild_duration_recorded_at is not UNSET:
            field_dict["codebuild_duration_recorded_at"] = codebuild_duration_recorded_at
        if progress is not UNSET:
            field_dict["progress"] = progress
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.deployment_progress import DeploymentProgress
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        frontend_id = UUID(d.pop("frontend_id"))




        project_id = UUID(d.pop("project_id"))




        operation = check_frontend_deployment_operation(d.pop("operation"))




        status = check_frontend_deployment_status(d.pop("status"))




        deploy_source = check_frontend_deployment_deploy_source(d.pop("deploy_source"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        initiated_by = d.pop("initiated_by", UNSET)

        artifact_bucket = d.pop("artifact_bucket", UNSET)

        artifact_key = d.pop("artifact_key", UNSET)

        artifact_version = d.pop("artifact_version", UNSET)

        site_url = d.pop("site_url", UNSET)

        cloudformation_stack_id = d.pop("cloudformation_stack_id", UNSET)

        cloudformation_stack_url = d.pop("cloudformation_stack_url", UNSET)

        codebuild_duration_seconds = d.pop("codebuild_duration_seconds", UNSET)

        codebuild_build_count = d.pop("codebuild_build_count", UNSET)

        _codebuild_duration_recorded_at = d.pop("codebuild_duration_recorded_at", UNSET)
        codebuild_duration_recorded_at: datetime.datetime | Unset
        if isinstance(_codebuild_duration_recorded_at,  Unset):
            codebuild_duration_recorded_at = UNSET
        else:
            codebuild_duration_recorded_at = datetime.datetime.fromisoformat(_codebuild_duration_recorded_at)




        _progress = d.pop("progress", UNSET)
        progress: DeploymentProgress | Unset
        if isinstance(_progress,  Unset):
            progress = UNSET
        else:
            progress = DeploymentProgress.from_dict(_progress)




        error_message = d.pop("error_message", UNSET)

        frontend_deployment = cls(
            id=id,
            frontend_id=frontend_id,
            project_id=project_id,
            operation=operation,
            status=status,
            deploy_source=deploy_source,
            created_at=created_at,
            updated_at=updated_at,
            initiated_by=initiated_by,
            artifact_bucket=artifact_bucket,
            artifact_key=artifact_key,
            artifact_version=artifact_version,
            site_url=site_url,
            cloudformation_stack_id=cloudformation_stack_id,
            cloudformation_stack_url=cloudformation_stack_url,
            codebuild_duration_seconds=codebuild_duration_seconds,
            codebuild_build_count=codebuild_build_count,
            codebuild_duration_recorded_at=codebuild_duration_recorded_at,
            progress=progress,
            error_message=error_message,
        )


        frontend_deployment.additional_properties = d
        return frontend_deployment

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
