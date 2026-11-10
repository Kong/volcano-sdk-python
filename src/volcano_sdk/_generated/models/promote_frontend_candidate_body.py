from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="PromoteFrontendCandidateBody")



@_attrs_define
class PromoteFrontendCandidateBody:
    """ 
        Attributes:
            expected_revision (int):
     """

    expected_revision: int





    def to_dict(self) -> dict[str, Any]:
        expected_revision = self.expected_revision


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "expected_revision": expected_revision,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        expected_revision = d.pop("expected_revision")

        promote_frontend_candidate_body = cls(
            expected_revision=expected_revision,
        )

        return promote_frontend_candidate_body

