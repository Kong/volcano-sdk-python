from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.autofix_evidence_kind import AutofixEvidenceKind
from ..models.autofix_evidence_kind import check_autofix_evidence_kind
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="AutofixEvidence")



@_attrs_define
class AutofixEvidence:
    """ 
        Attributes:
            kind (AutofixEvidenceKind):
            detail (str):
            location (str | Unset): A file and line, or a log timestamp. Absent when the evidence has none.
     """

    kind: AutofixEvidenceKind
    detail: str
    location: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        detail = self.detail

        location = self.location


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "detail": detail,
        })
        if location is not UNSET:
            field_dict["location"] = location

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_autofix_evidence_kind(d.pop("kind"))




        detail = d.pop("detail")

        location = d.pop("location", UNSET)

        autofix_evidence = cls(
            kind=kind,
            detail=detail,
            location=location,
        )

        return autofix_evidence

