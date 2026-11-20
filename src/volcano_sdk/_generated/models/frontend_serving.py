from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="FrontendServing")



@_attrs_define
class FrontendServing:
    """ What a frontend serves. Until a Candidate is promoted it serves its own runtime and
    `candidate_id` is null. After a promotion, the frontend's traffic is routed to that
    Candidate's runtime, nothing is rebuilt or copied, and `previous_candidate_id` is the runtime a
    rollback returns to (null when that is the frontend's own). A Candidate that serves cannot be
    deleted and does not expire. One kept only as the runtime a rollback returns to does not
    expire either, but it can be deleted, which gives up that rollback; the frontend's own
    runtime stays one `to_production` rollback away.

        Attributes:
            revision (int): Counts changes to what the frontend serves or can roll back to — promotions, rollbacks, and
                deleting the Candidate kept for a rollback. A promotion or rollback names the revision it read, so one that read
                before such a change fails with `409` instead of overwriting it; read the serving state again and retry.
            candidate_id (None | UUID):
            previous_candidate_id (None | UUID):
     """

    revision: int
    candidate_id: None | UUID
    previous_candidate_id: None | UUID





    def to_dict(self) -> dict[str, Any]:
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


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "revision": revision,
            "candidate_id": candidate_id,
            "previous_candidate_id": previous_candidate_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
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


        frontend_serving = cls(
            revision=revision,
            candidate_id=candidate_id,
            previous_candidate_id=previous_candidate_id,
        )

        return frontend_serving

