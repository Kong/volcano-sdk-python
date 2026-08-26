from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.import_provider import check_import_provider
from ..models.import_provider import ImportProvider
from ..models.project_import_run_status import check_project_import_run_status
from ..models.project_import_run_status import ProjectImportRunStatus
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.deployment_reference import DeploymentReference
  from ..models.resource_reference import ResourceReference





T = TypeVar("T", bound="ProjectImportRun")



@_attrs_define
class ProjectImportRun:
    """ 
        Attributes:
            id (str):
            provider (ImportProvider):
            source_id (str):
            destination_project_name (str):
            resource (ResourceReference): Stable reference to a Volcano resource.
            deployment (DeploymentReference): Stable reference to a Volcano deployment run.
            status (ProjectImportRunStatus):
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            error_code (str | Unset):
            error_message (str | Unset):
     """

    id: str
    provider: ImportProvider
    source_id: str
    destination_project_name: str
    resource: ResourceReference
    deployment: DeploymentReference
    status: ProjectImportRunStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    error_code: str | Unset = UNSET
    error_message: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.deployment_reference import DeploymentReference
        from ..models.resource_reference import ResourceReference
        id = self.id

        provider: str = self.provider

        source_id = self.source_id

        destination_project_name = self.destination_project_name

        resource = self.resource.to_dict()

        deployment = self.deployment.to_dict()

        status: str = self.status

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        error_code = self.error_code

        error_message = self.error_message


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "provider": provider,
            "source_id": source_id,
            "destination_project_name": destination_project_name,
            "resource": resource,
            "deployment": deployment,
            "status": status,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.deployment_reference import DeploymentReference
        from ..models.resource_reference import ResourceReference
        d = dict(src_dict)
        id = d.pop("id")

        provider = check_import_provider(d.pop("provider"))




        source_id = d.pop("source_id")

        destination_project_name = d.pop("destination_project_name")

        resource = ResourceReference.from_dict(d.pop("resource"))




        deployment = DeploymentReference.from_dict(d.pop("deployment"))




        status = check_project_import_run_status(d.pop("status"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        error_code = d.pop("error_code", UNSET)

        error_message = d.pop("error_message", UNSET)

        project_import_run = cls(
            id=id,
            provider=provider,
            source_id=source_id,
            destination_project_name=destination_project_name,
            resource=resource,
            deployment=deployment,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            error_code=error_code,
            error_message=error_message,
        )


        project_import_run.additional_properties = d
        return project_import_run

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
