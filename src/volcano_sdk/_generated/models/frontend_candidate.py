from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.frontend_candidate_configuration_status import check_frontend_candidate_configuration_status
from ..models.frontend_candidate_configuration_status import FrontendCandidateConfigurationStatus
from ..models.frontend_candidate_status import check_frontend_candidate_status
from ..models.frontend_candidate_status import FrontendCandidateStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.frontend_candidate_deployment import FrontendCandidateDeployment





T = TypeVar("T", bound="FrontendCandidate")



@_attrs_define
class FrontendCandidate:
    """ A copy of a frontend built from an uploaded archive with the frontend's own configuration, so
    it can be checked before anything is promoted. A Candidate is reachable by anyone who holds its
    URL and is not indexed or listed; it is never public, and it does not claim to be private.

        Attributes:
            id (UUID):
            frontend_id (UUID):
            name (str):
            status (FrontendCandidateStatus): `creating` until its first deployment succeeds, `ready` while it serves,
                `deleting` while
                its runtime is removed, and `error` when its deletion gave up and needs an operator.
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            url (str | Unset): Where the Candidate is served. Absent until its first deployment succeeds.
            expires_at (datetime.datetime | Unset): When the Candidate is deleted on its own. Absent when it is kept until
                deleted.
            current_deployment_id (UUID | Unset): The deployment the Candidate serves. Absent until its first
                deployment succeeds. It differs from `deployment` while a redeploy runs or after one failed.
            deployment (FrontendCandidateDeployment | Unset):
            configuration_status (FrontendCandidateConfigurationStatus | Unset): Present while the Candidate serves a
                deployment. `current` means that deployment was built
                with the variables the frontend selects now; `changed` means they differ, or can no longer
                be resolved. Promotion refuses a Candidate whose status is `changed`.
     """

    id: UUID
    frontend_id: UUID
    name: str
    status: FrontendCandidateStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    url: str | Unset = UNSET
    expires_at: datetime.datetime | Unset = UNSET
    current_deployment_id: UUID | Unset = UNSET
    deployment: FrontendCandidateDeployment | Unset = UNSET
    configuration_status: FrontendCandidateConfigurationStatus | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.frontend_candidate_deployment import FrontendCandidateDeployment # noqa: PLC0415
        id = str(self.id)

        frontend_id = str(self.frontend_id)

        name = self.name

        status: str = self.status

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        url = self.url

        expires_at: str | Unset = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        current_deployment_id: str | Unset = UNSET
        if not isinstance(self.current_deployment_id, Unset):
            current_deployment_id = str(self.current_deployment_id)

        deployment: dict[str, Any] | Unset = UNSET
        if not isinstance(self.deployment, Unset):
            deployment = self.deployment.to_dict()

        configuration_status: str | Unset = UNSET
        if not isinstance(self.configuration_status, Unset):
            configuration_status = self.configuration_status



        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "frontend_id": frontend_id,
            "name": name,
            "status": status,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if url is not UNSET:
            field_dict["url"] = url
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if current_deployment_id is not UNSET:
            field_dict["current_deployment_id"] = current_deployment_id
        if deployment is not UNSET:
            field_dict["deployment"] = deployment
        if configuration_status is not UNSET:
            field_dict["configuration_status"] = configuration_status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.frontend_candidate_deployment import FrontendCandidateDeployment # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        frontend_id = UUID(d.pop("frontend_id"))




        name = d.pop("name")

        status = check_frontend_candidate_status(d.pop("status"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        url = d.pop("url", UNSET)

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: datetime.datetime | Unset
        if isinstance(_expires_at,  Unset):
            expires_at = UNSET
        else:
            expires_at = datetime.datetime.fromisoformat(_expires_at)




        _current_deployment_id = d.pop("current_deployment_id", UNSET)
        current_deployment_id: UUID | Unset
        if isinstance(_current_deployment_id,  Unset):
            current_deployment_id = UNSET
        else:
            current_deployment_id = UUID(_current_deployment_id)




        _deployment = d.pop("deployment", UNSET)
        deployment: FrontendCandidateDeployment | Unset
        if isinstance(_deployment,  Unset):
            deployment = UNSET
        else:
            deployment = FrontendCandidateDeployment.from_dict(_deployment)




        _configuration_status = d.pop("configuration_status", UNSET)
        configuration_status: FrontendCandidateConfigurationStatus | Unset
        if isinstance(_configuration_status,  Unset):
            configuration_status = UNSET
        else:
            configuration_status = check_frontend_candidate_configuration_status(_configuration_status)




        frontend_candidate = cls(
            id=id,
            frontend_id=frontend_id,
            name=name,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            url=url,
            expires_at=expires_at,
            current_deployment_id=current_deployment_id,
            deployment=deployment,
            configuration_status=configuration_status,
        )

        return frontend_candidate

