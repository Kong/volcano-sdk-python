from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.issue_finding_severity import check_issue_finding_severity
from ..models.issue_finding_severity import IssueFindingSeverity
from typing import cast






T = TypeVar("T", bound="IssueFinding")



@_attrs_define
class IssueFinding:
    """ The LavaFlow Code Quality finding behind a `code_quality` issue.

        Attributes:
            rule (str): The rule the finding names, such as `null-dereference`.
            severity (IssueFindingSeverity): How much the problem matters, as the finding was confirmed.
            commit_sha (str): The deployed commit the scan found the problem in.
            path (str): The file, from the repository root.
            start_line (int): The first line of the problem in that commit, from 1.
            end_line (int): The last line of the problem in that commit.
            explanation (str): What fails and on which input, as plain text. When it holds one of the project's secret
                values or a secret gitleaks' default rules detect, it reads `Hidden: this field matched a secret.` in place of
                all of it.
     """

    rule: str
    severity: IssueFindingSeverity
    commit_sha: str
    path: str
    start_line: int
    end_line: int
    explanation: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        rule = self.rule

        severity: str = self.severity

        commit_sha = self.commit_sha

        path = self.path

        start_line = self.start_line

        end_line = self.end_line

        explanation = self.explanation


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "rule": rule,
            "severity": severity,
            "commit_sha": commit_sha,
            "path": path,
            "start_line": start_line,
            "end_line": end_line,
            "explanation": explanation,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        rule = d.pop("rule")

        severity = check_issue_finding_severity(d.pop("severity"))




        commit_sha = d.pop("commit_sha")

        path = d.pop("path")

        start_line = d.pop("start_line")

        end_line = d.pop("end_line")

        explanation = d.pop("explanation")

        issue_finding = cls(
            rule=rule,
            severity=severity,
            commit_sha=commit_sha,
            path=path,
            start_line=start_line,
            end_line=end_line,
            explanation=explanation,
        )


        issue_finding.additional_properties = d
        return issue_finding

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
