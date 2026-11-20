from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowReviewPersonReason")



@_attrs_define
class LavaflowReviewPersonReason:
    """ One decision the review leaves to a person. `question` reads `Hidden: this field matched a secret.` when it holds
    one of the project's secret values or a secret gitleaks detects, and `Hidden: the fix may add a credential.` when
    the run is held with `possible_credential`.

        Attributes:
            kind (str): `irreversible`: merging the fix itself does what a revert can't undo, such as deleting or migrating
                stored data. `trust_boundary`: it changes authentication, authorization, secrets, who can reach what, or rate
                limits, quotas or other abuse controls, including whether they fail open. `breaks_contract`: it removes or
                renames an existing field, status, event, or accepted input that other code or users rely on, or changes what
                one means, or it newly rejects a request the code could serve before it, or input it served even when its
                documentation marks that input invalid, with a client error, validation error, or limit, or drops or skips
                records the code handled. `billing`: it touches payments, pricing, metering, or charges. `unexplained`: it
                changes behavior that neither the diagnosis nor the fix's stated choices justify, and that the code doesn't
                support. `not_reviewable`: it couldn't be reviewed closely. New kinds may appear.
            question (str): What the person decides, written to show as given.
     """

    kind: str
    question: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        kind = self.kind

        question = self.question


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "kind": kind,
            "question": question,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = d.pop("kind")

        question = d.pop("question")

        lavaflow_review_person_reason = cls(
            kind=kind,
            question=question,
        )


        lavaflow_review_person_reason.additional_properties = d
        return lavaflow_review_person_reason

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
