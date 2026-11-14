from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_review_finding_severity import check_lavaflow_review_finding_severity
from ..models.lavaflow_review_finding_severity import LavaflowReviewFindingSeverity
from typing import cast






T = TypeVar("T", bound="LavaflowReviewFinding")



@_attrs_define
class LavaflowReviewFinding:
    """ A finding the review left open, in the reviewer's words. `explanation` reads `Hidden: this field matched a secret.`
    when it holds one of the project's secret values or a secret gitleaks detects, or when `file` reads `""`, and
    `Hidden: the fix may add a credential.` when the run is held with `possible_credential`.

        Attributes:
            severity (LavaflowReviewFindingSeverity):
            file (None | str): The file the finding is about, null when it is about no file. `""` when the path holds a
                control character, one of the project's secret values or a secret gitleaks detects.
            line (int | None): The line of `file` the finding is about, null when it is about no one line.
            explanation (str):
     """

    severity: LavaflowReviewFindingSeverity
    file: None | str
    line: int | None
    explanation: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        severity: str = self.severity

        file: None | str
        file = self.file

        line: int | None
        line = self.line

        explanation = self.explanation


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "severity": severity,
            "file": file,
            "line": line,
            "explanation": explanation,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        severity = check_lavaflow_review_finding_severity(d.pop("severity"))




        def _parse_file(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        file = _parse_file(d.pop("file"))


        def _parse_line(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        line = _parse_line(d.pop("line"))


        explanation = d.pop("explanation")

        lavaflow_review_finding = cls(
            severity=severity,
            file=file,
            line=line,
            explanation=explanation,
        )


        lavaflow_review_finding.additional_properties = d
        return lavaflow_review_finding

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
