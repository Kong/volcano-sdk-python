from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.function_candidate_deployment_operation import check_function_candidate_deployment_operation
from ..models.function_candidate_deployment_operation import FunctionCandidateDeploymentOperation
from ..models.function_candidate_deployment_status import check_function_candidate_deployment_status
from ..models.function_candidate_deployment_status import FunctionCandidateDeploymentStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.function_image_digest import FunctionImageDigest





T = TypeVar("T", bound="FunctionCandidateDeployment")



@_attrs_define
class FunctionCandidateDeployment:
    """ 
        Attributes:
            id (UUID):
            status (FunctionCandidateDeploymentStatus): `provisioning` while the build and deploy run, `active` once the
                preview serves this
                deployment, and `failed` when it could not be built or deployed. A failed deployment of a
                preview that already served keeps the previous deployment serving.
            operation (FunctionCandidateDeploymentOperation):
            configuration_digest (str): Identifies the variables the build used without carrying any value.
            regions (list[str]):
            created_at (datetime.datetime):
            image_digests (list[FunctionImageDigest] | Unset): The digest of the image this deployment published, per
                region. Present once the deployment
                succeeded. A promotion points the function at this image and deploys nothing.
            error_message (str | Unset): Why a failed deployment failed.
            completed_at (datetime.datetime | Unset): Set once the deployment is no longer provisioning.
     """

    id: UUID
    status: FunctionCandidateDeploymentStatus
    operation: FunctionCandidateDeploymentOperation
    configuration_digest: str
    regions: list[str]
    created_at: datetime.datetime
    image_digests: list[FunctionImageDigest] | Unset = UNSET
    error_message: str | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.function_image_digest import FunctionImageDigest # noqa: PLC0415
        id = str(self.id)

        status: str = self.status

        operation: str = self.operation

        configuration_digest = self.configuration_digest

        regions = self.regions



        created_at = self.created_at.isoformat()

        image_digests: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.image_digests, Unset):
            image_digests = []
            for image_digests_item_data in self.image_digests:
                image_digests_item = image_digests_item_data.to_dict()
                image_digests.append(image_digests_item)



        error_message = self.error_message

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "status": status,
            "operation": operation,
            "configuration_digest": configuration_digest,
            "regions": regions,
            "created_at": created_at,
        })
        if image_digests is not UNSET:
            field_dict["image_digests"] = image_digests
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.function_image_digest import FunctionImageDigest # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        status = check_function_candidate_deployment_status(d.pop("status"))




        operation = check_function_candidate_deployment_operation(d.pop("operation"))




        configuration_digest = d.pop("configuration_digest")

        regions = cast(list[str], d.pop("regions"))


        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        _image_digests = d.pop("image_digests", UNSET)
        image_digests: list[FunctionImageDigest] | Unset = UNSET
        if _image_digests is not UNSET:
            image_digests = []
            for image_digests_item_data in _image_digests:
                image_digests_item = FunctionImageDigest.from_dict(image_digests_item_data)



                image_digests.append(image_digests_item)


        error_message = d.pop("error_message", UNSET)

        _completed_at = d.pop("completed_at", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at,  Unset):
            completed_at = UNSET
        else:
            completed_at = datetime.datetime.fromisoformat(_completed_at)




        function_candidate_deployment = cls(
            id=id,
            status=status,
            operation=operation,
            configuration_digest=configuration_digest,
            regions=regions,
            created_at=created_at,
            image_digests=image_digests,
            error_message=error_message,
            completed_at=completed_at,
        )

        return function_candidate_deployment

