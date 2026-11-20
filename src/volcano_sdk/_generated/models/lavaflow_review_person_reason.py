from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowReviewPersonReason")



@_attrs_define
class LavaflowReviewPersonReason:
    """ One decision the review leaves to a person. When LavaFlow withholds `question`, a sentence that says why stands in:
    `LavaFlow left this question out because it may contain a credential` when it may contain a credential or holds one
    of the project's secret values; `… because it's too long to check for a credential` when it is over 4,000
    characters; and `… because the fix may add a credential` when the run is held with `possible_credential`.

        Attributes:
            kind (str): `irreversible`: the fix deletes or migrates data, or does what a revert can't undo.
                `trust_boundary`: it changes authentication, authorization, secrets, or who can reach what. `breaks_contract`:
                it changes an interface other code or users depend on. `billing`: it touches payments, pricing, metering, or
                charges. `unexplained`: it changes behavior its context doesn't explain. `not_reviewable`: it couldn't be
                reviewed closely. New kinds may appear.
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
