from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.function_candidate_configuration_status import check_function_candidate_configuration_status
from ..models.function_candidate_configuration_status import FunctionCandidateConfigurationStatus
from ..models.function_candidate_exposure import check_function_candidate_exposure
from ..models.function_candidate_exposure import FunctionCandidateExposure
from ..models.function_candidate_status import check_function_candidate_status
from ..models.function_candidate_status import FunctionCandidateStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.function_candidate_deployment import FunctionCandidateDeployment





T = TypeVar("T", bound="FunctionCandidate")



@_attrs_define
class FunctionCandidate:
    """ A copy of an ordinary function built from an uploaded source with the function's own variables,
    run on a runtime of its own and invoked at its own host with the project's service key only, so it
    can be checked before it is promoted. It has none of the function's schedules or warmers. Fields
    that do not apply yet are absent.

        Attributes:
            id (UUID):
            function_id (UUID):
            name (str):
            slug (str):
            status (FunctionCandidateStatus): `creating` until its first deployment succeeds, `ready` while it serves,
                `deleting` while its
                runtime is removed, and `error` when its deletion gave up and needs an operator. A deleted
                preview answers `404`.
            exposure (FunctionCandidateExposure): A function preview is always private. Only the project's service key, with
                `functions.invoke`, can invoke it; signed-in users, anon keys and access tokens are refused.
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            serving (bool): The function runs this preview's build.
            kept_for_rollback (bool): A rollback of the function returns to this preview's build.
            url (str | Unset): Where the preview is invoked. Absent until its first deployment succeeds.
            expires_at (datetime.datetime | Unset): When the preview is deleted on its own. Absent when it is kept until
                deleted. A preview the function runs, or keeps for a rollback, is not deleted then; it expires once it is
                neither.
            created_by (str | Unset): The user who created the preview, when a user did.
            current_deployment_id (UUID | Unset): The deployment the preview serves. Absent until its first deployment
                succeeds. It differs from
                `deployment` while a redeploy runs or after one failed.
            deployment (FunctionCandidateDeployment | Unset):
            configuration_status (FunctionCandidateConfigurationStatus | Unset): Present while the preview serves a
                deployment. `current` means that deployment was built with
                the variables, runtime and handler the function would give that source now; `changed` means
                they differ, or can no longer be resolved. Promotion refuses a preview whose status is
                `changed`.
     """

    id: UUID
    function_id: UUID
    name: str
    slug: str
    status: FunctionCandidateStatus
    exposure: FunctionCandidateExposure
    created_at: datetime.datetime
    updated_at: datetime.datetime
    serving: bool
    kept_for_rollback: bool
    url: str | Unset = UNSET
    expires_at: datetime.datetime | Unset = UNSET
    created_by: str | Unset = UNSET
    current_deployment_id: UUID | Unset = UNSET
    deployment: FunctionCandidateDeployment | Unset = UNSET
    configuration_status: FunctionCandidateConfigurationStatus | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.function_candidate_deployment import FunctionCandidateDeployment # noqa: PLC0415
        id = str(self.id)

        function_id = str(self.function_id)

        name = self.name

        slug = self.slug

        status: str = self.status

        exposure: str = self.exposure

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        serving = self.serving

        kept_for_rollback = self.kept_for_rollback

        url = self.url

        expires_at: str | Unset = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        created_by = self.created_by

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
            "function_id": function_id,
            "name": name,
            "slug": slug,
            "status": status,
            "exposure": exposure,
            "created_at": created_at,
            "updated_at": updated_at,
            "serving": serving,
            "kept_for_rollback": kept_for_rollback,
        })
        if url is not UNSET:
            field_dict["url"] = url
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if current_deployment_id is not UNSET:
            field_dict["current_deployment_id"] = current_deployment_id
        if deployment is not UNSET:
            field_dict["deployment"] = deployment
        if configuration_status is not UNSET:
            field_dict["configuration_status"] = configuration_status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.function_candidate_deployment import FunctionCandidateDeployment # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        function_id = UUID(d.pop("function_id"))




        name = d.pop("name")

        slug = d.pop("slug")

        status = check_function_candidate_status(d.pop("status"))




        exposure = check_function_candidate_exposure(d.pop("exposure"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        serving = d.pop("serving")

        kept_for_rollback = d.pop("kept_for_rollback")

        url = d.pop("url", UNSET)

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: datetime.datetime | Unset
        if isinstance(_expires_at,  Unset):
            expires_at = UNSET
        else:
            expires_at = datetime.datetime.fromisoformat(_expires_at)




        created_by = d.pop("created_by", UNSET)

        _current_deployment_id = d.pop("current_deployment_id", UNSET)
        current_deployment_id: UUID | Unset
        if isinstance(_current_deployment_id,  Unset):
            current_deployment_id = UNSET
        else:
            current_deployment_id = UUID(_current_deployment_id)




        _deployment = d.pop("deployment", UNSET)
        deployment: FunctionCandidateDeployment | Unset
        if isinstance(_deployment,  Unset):
            deployment = UNSET
        else:
            deployment = FunctionCandidateDeployment.from_dict(_deployment)




        _configuration_status = d.pop("configuration_status", UNSET)
        configuration_status: FunctionCandidateConfigurationStatus | Unset
        if isinstance(_configuration_status,  Unset):
            configuration_status = UNSET
        else:
            configuration_status = check_function_candidate_configuration_status(_configuration_status)




        function_candidate = cls(
            id=id,
            function_id=function_id,
            name=name,
            slug=slug,
            status=status,
            exposure=exposure,
            created_at=created_at,
            updated_at=updated_at,
            serving=serving,
            kept_for_rollback=kept_for_rollback,
            url=url,
            expires_at=expires_at,
            created_by=created_by,
            current_deployment_id=current_deployment_id,
            deployment=deployment,
            configuration_status=configuration_status,
        )

        return function_candidate

