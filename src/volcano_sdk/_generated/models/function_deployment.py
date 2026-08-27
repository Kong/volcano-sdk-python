from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.function_deployment_deploy_source import check_function_deployment_deploy_source
from ..models.function_deployment_deploy_source import FunctionDeploymentDeploySource
from ..models.function_deployment_operation import check_function_deployment_operation
from ..models.function_deployment_operation import FunctionDeploymentOperation
from ..models.function_deployment_status import check_function_deployment_status
from ..models.function_deployment_status import FunctionDeploymentStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.deployment_progress import DeploymentProgress





T = TypeVar("T", bound="FunctionDeployment")



@_attrs_define
class FunctionDeployment:
    """ 
        Attributes:
            id (UUID):
            function_id (UUID):
            project_id (UUID):
            operation (FunctionDeploymentOperation):
            status (FunctionDeploymentStatus):
            deploy_source (FunctionDeploymentDeploySource): What initiated this deployment.
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            batch_id (UUID | Unset):
            initiated_by (str | Unset): Platform user that triggered a request-initiated deployment; absent for git and
                system deployments.
            artifact_bucket (str | Unset):
            artifact_key (str | Unset):
            artifact_version (str | Unset):
            codebuild_duration_seconds (int | Unset): Total CodeBuild build duration recorded for this deployment, in
                seconds.
            codebuild_build_count (int | Unset): Number of completed CodeBuild builds included in
                codebuild_duration_seconds.
            codebuild_duration_recorded_at (datetime.datetime | Unset):
            progress (DeploymentProgress | Unset): Normalized live progress derived from the deployment workflow and build
                phases.
            error_message (str | Unset):
            completed_at (datetime.datetime | Unset):
     """

    id: UUID
    function_id: UUID
    project_id: UUID
    operation: FunctionDeploymentOperation
    status: FunctionDeploymentStatus
    deploy_source: FunctionDeploymentDeploySource
    created_at: datetime.datetime
    updated_at: datetime.datetime
    batch_id: UUID | Unset = UNSET
    initiated_by: str | Unset = UNSET
    artifact_bucket: str | Unset = UNSET
    artifact_key: str | Unset = UNSET
    artifact_version: str | Unset = UNSET
    codebuild_duration_seconds: int | Unset = UNSET
    codebuild_build_count: int | Unset = UNSET
    codebuild_duration_recorded_at: datetime.datetime | Unset = UNSET
    progress: DeploymentProgress | Unset = UNSET
    error_message: str | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.deployment_progress import DeploymentProgress
        id = str(self.id)

        function_id = str(self.function_id)

        project_id = str(self.project_id)

        operation: str = self.operation

        status: str = self.status

        deploy_source: str = self.deploy_source

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        batch_id: str | Unset = UNSET
        if not isinstance(self.batch_id, Unset):
            batch_id = str(self.batch_id)

        initiated_by = self.initiated_by

        artifact_bucket = self.artifact_bucket

        artifact_key = self.artifact_key

        artifact_version = self.artifact_version

        codebuild_duration_seconds = self.codebuild_duration_seconds

        codebuild_build_count = self.codebuild_build_count

        codebuild_duration_recorded_at: str | Unset = UNSET
        if not isinstance(self.codebuild_duration_recorded_at, Unset):
            codebuild_duration_recorded_at = self.codebuild_duration_recorded_at.isoformat()

        progress: dict[str, Any] | Unset = UNSET
        if not isinstance(self.progress, Unset):
            progress = self.progress.to_dict()

        error_message = self.error_message

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "function_id": function_id,
            "project_id": project_id,
            "operation": operation,
            "status": status,
            "deploy_source": deploy_source,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if batch_id is not UNSET:
            field_dict["batch_id"] = batch_id
        if initiated_by is not UNSET:
            field_dict["initiated_by"] = initiated_by
        if artifact_bucket is not UNSET:
            field_dict["artifact_bucket"] = artifact_bucket
        if artifact_key is not UNSET:
            field_dict["artifact_key"] = artifact_key
        if artifact_version is not UNSET:
            field_dict["artifact_version"] = artifact_version
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
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.deployment_progress import DeploymentProgress
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        function_id = UUID(d.pop("function_id"))




        project_id = UUID(d.pop("project_id"))




        operation = check_function_deployment_operation(d.pop("operation"))




        status = check_function_deployment_status(d.pop("status"))




        deploy_source = check_function_deployment_deploy_source(d.pop("deploy_source"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        _batch_id = d.pop("batch_id", UNSET)
        batch_id: UUID | Unset
        if isinstance(_batch_id,  Unset):
            batch_id = UNSET
        else:
            batch_id = UUID(_batch_id)




        initiated_by = d.pop("initiated_by", UNSET)

        artifact_bucket = d.pop("artifact_bucket", UNSET)

        artifact_key = d.pop("artifact_key", UNSET)

        artifact_version = d.pop("artifact_version", UNSET)

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

        _completed_at = d.pop("completed_at", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at,  Unset):
            completed_at = UNSET
        else:
            completed_at = datetime.datetime.fromisoformat(_completed_at)




        function_deployment = cls(
            id=id,
            function_id=function_id,
            project_id=project_id,
            operation=operation,
            status=status,
            deploy_source=deploy_source,
            created_at=created_at,
            updated_at=updated_at,
            batch_id=batch_id,
            initiated_by=initiated_by,
            artifact_bucket=artifact_bucket,
            artifact_key=artifact_key,
            artifact_version=artifact_version,
            codebuild_duration_seconds=codebuild_duration_seconds,
            codebuild_build_count=codebuild_build_count,
            codebuild_duration_recorded_at=codebuild_duration_recorded_at,
            progress=progress,
            error_message=error_message,
            completed_at=completed_at,
        )


        function_deployment.additional_properties = d
        return function_deployment

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
