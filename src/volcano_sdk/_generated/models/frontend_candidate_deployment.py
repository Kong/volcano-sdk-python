from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.frontend_candidate_deployment_status import check_frontend_candidate_deployment_status
from ..models.frontend_candidate_deployment_status import FrontendCandidateDeploymentStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="FrontendCandidateDeployment")



@_attrs_define
class FrontendCandidateDeployment:
    """ 
        Attributes:
            id (UUID):
            status (FrontendCandidateDeploymentStatus): `provisioning` while the build and deploy run, `active` once the
                Candidate serves this
                deployment, and `failed` when it could not be built or deployed. A failed deployment of a
                Candidate that already served keeps the previous deployment serving.
            configuration_digest (str): Identifies the resolved configuration the deployment was built with. It carries no
                value.
            created_at (datetime.datetime):
            error_message (str | Unset): Why a failed deployment failed.
            completed_at (datetime.datetime | Unset): Set once the deployment is no longer provisioning.
     """

    id: UUID
    status: FrontendCandidateDeploymentStatus
    configuration_digest: str
    created_at: datetime.datetime
    error_message: str | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        status: str = self.status

        configuration_digest = self.configuration_digest

        created_at = self.created_at.isoformat()

        error_message = self.error_message

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "status": status,
            "configuration_digest": configuration_digest,
            "created_at": created_at,
        })
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        status = check_frontend_candidate_deployment_status(d.pop("status"))




        configuration_digest = d.pop("configuration_digest")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        error_message = d.pop("error_message", UNSET)

        _completed_at = d.pop("completed_at", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at,  Unset):
            completed_at = UNSET
        else:
            completed_at = datetime.datetime.fromisoformat(_completed_at)




        frontend_candidate_deployment = cls(
            id=id,
            status=status,
            configuration_digest=configuration_digest,
            created_at=created_at,
            error_message=error_message,
            completed_at=completed_at,
        )

        return frontend_candidate_deployment

