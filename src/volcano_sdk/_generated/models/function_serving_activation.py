from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.function_serving_activation_kind import check_function_serving_activation_kind
from ..models.function_serving_activation_kind import FunctionServingActivationKind
from ..models.function_serving_activation_status import check_function_serving_activation_status
from ..models.function_serving_activation_status import FunctionServingActivationStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.function_image_digest import FunctionImageDigest





T = TypeVar("T", bound="FunctionServingActivation")



@_attrs_define
class FunctionServingActivation:
    """ The latest change to what serves the function's traffic: a promotion, a rollback, or a deployment
    of the function that returned its traffic to its own build. Each takes effect at once. Absent until
    the function's first promotion.

        Attributes:
            id (UUID):
            kind (FunctionServingActivationKind): `deploy`: a successful deployment of the function cleared the preview
                pointers.
            status (FunctionServingActivationStatus): `applied`: the change takes effect when it is recorded.
            revision (int):
            candidate_id (UUID | Unset): The preview the activation pointed the function at. Absent for the function's own
                build.
            image_digests (list[FunctionImageDigest] | Unset): The digests of the image the activation pointed the function
                at. Absent for the function's own build.
     """

    id: UUID
    kind: FunctionServingActivationKind
    status: FunctionServingActivationStatus
    revision: int
    candidate_id: UUID | Unset = UNSET
    image_digests: list[FunctionImageDigest] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.function_image_digest import FunctionImageDigest # noqa: PLC0415
        id = str(self.id)

        kind: str = self.kind

        status: str = self.status

        revision = self.revision

        candidate_id: str | Unset = UNSET
        if not isinstance(self.candidate_id, Unset):
            candidate_id = str(self.candidate_id)

        image_digests: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.image_digests, Unset):
            image_digests = []
            for image_digests_item_data in self.image_digests:
                image_digests_item = image_digests_item_data.to_dict()
                image_digests.append(image_digests_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "kind": kind,
            "status": status,
            "revision": revision,
        })
        if candidate_id is not UNSET:
            field_dict["candidate_id"] = candidate_id
        if image_digests is not UNSET:
            field_dict["image_digests"] = image_digests

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.function_image_digest import FunctionImageDigest # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        kind = check_function_serving_activation_kind(d.pop("kind"))




        status = check_function_serving_activation_status(d.pop("status"))




        revision = d.pop("revision")

        _candidate_id = d.pop("candidate_id", UNSET)
        candidate_id: UUID | Unset
        if isinstance(_candidate_id,  Unset):
            candidate_id = UNSET
        else:
            candidate_id = UUID(_candidate_id)




        _image_digests = d.pop("image_digests", UNSET)
        image_digests: list[FunctionImageDigest] | Unset = UNSET
        if _image_digests is not UNSET:
            image_digests = []
            for image_digests_item_data in _image_digests:
                image_digests_item = FunctionImageDigest.from_dict(image_digests_item_data)



                image_digests.append(image_digests_item)


        function_serving_activation = cls(
            id=id,
            kind=kind,
            status=status,
            revision=revision,
            candidate_id=candidate_id,
            image_digests=image_digests,
        )

        return function_serving_activation

