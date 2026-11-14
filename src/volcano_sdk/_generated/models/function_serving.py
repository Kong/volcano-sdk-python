from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.function_production_environment import FunctionProductionEnvironment
  from ..models.function_serving_activation import FunctionServingActivation





T = TypeVar("T", bound="FunctionServing")



@_attrs_define
class FunctionServing:
    """ What a function runs. Until a preview is promoted it runs its own build and `candidate_id` is
    null. After a promotion, the function's traffic runs on that preview's runtime, nothing is rebuilt
    or deployed, and `previous_candidate_id` is what a rollback returns to (null when that is the
    function's own build). A preview the function runs cannot be deleted and does not expire. One kept
    only as what a rollback returns to does not expire either, but it can be deleted, which gives up
    that rollback; the function's own build stays one `to_production` rollback away.

        Attributes:
            revision (int): Counts changes to what the function runs or can roll back to — promotions, rollbacks, a
                deployment that returns the traffic to the function's own build, and deleting the preview kept for a rollback. A
                promotion or rollback names the revision it read, so one that read before such a change fails with `409`
                (`stale_revision`) instead of overwriting it; read the serving state again and retry.
            candidate_id (None | UUID): The preview whose build the function runs; null for its own.
            previous_candidate_id (None | UUID): The preview a rollback returns to; null for the function's own build.
            production_environment (FunctionProductionEnvironment): Whether the function's own build has the project's
                current variables. While a preview serves the
                function, `volcano config deploy` and replacing the shared variable list skip the function, so its
                own build keeps the values it had. A rollback to the function's own build starts synchronizing them
                as it returns the traffic, and the status reads `current` once that synchronization completes or a
                deployment of the function activates. A synchronization that fails leaves it `out_of_date`.
            activation (FunctionServingActivation | Unset): The latest change to what serves the function's traffic: a
                promotion, a rollback, or a deployment
                of the function that returned its traffic to its own build. Each takes effect at once. Absent until
                the function's first promotion.
     """

    revision: int
    candidate_id: None | UUID
    previous_candidate_id: None | UUID
    production_environment: FunctionProductionEnvironment
    activation: FunctionServingActivation | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.function_production_environment import FunctionProductionEnvironment # noqa: PLC0415
        from ..models.function_serving_activation import FunctionServingActivation # noqa: PLC0415
        revision = self.revision

        candidate_id: None | str
        if isinstance(self.candidate_id, UUID):
            candidate_id = str(self.candidate_id)
        else:
            candidate_id = self.candidate_id

        previous_candidate_id: None | str
        if isinstance(self.previous_candidate_id, UUID):
            previous_candidate_id = str(self.previous_candidate_id)
        else:
            previous_candidate_id = self.previous_candidate_id

        production_environment = self.production_environment.to_dict()

        activation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.activation, Unset):
            activation = self.activation.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "revision": revision,
            "candidate_id": candidate_id,
            "previous_candidate_id": previous_candidate_id,
            "production_environment": production_environment,
        })
        if activation is not UNSET:
            field_dict["activation"] = activation

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.function_production_environment import FunctionProductionEnvironment # noqa: PLC0415
        from ..models.function_serving_activation import FunctionServingActivation # noqa: PLC0415
        d = dict(src_dict)
        revision = d.pop("revision")

        def _parse_candidate_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                candidate_id_type_0 = UUID(data)



                return candidate_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        candidate_id = _parse_candidate_id(d.pop("candidate_id"))


        def _parse_previous_candidate_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                previous_candidate_id_type_0 = UUID(data)



                return previous_candidate_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        previous_candidate_id = _parse_previous_candidate_id(d.pop("previous_candidate_id"))


        production_environment = FunctionProductionEnvironment.from_dict(d.pop("production_environment"))




        _activation = d.pop("activation", UNSET)
        activation: FunctionServingActivation | Unset
        if isinstance(_activation,  Unset):
            activation = UNSET
        else:
            activation = FunctionServingActivation.from_dict(_activation)




        function_serving = cls(
            revision=revision,
            candidate_id=candidate_id,
            previous_candidate_id=previous_candidate_id,
            production_environment=production_environment,
            activation=activation,
        )

        return function_serving

