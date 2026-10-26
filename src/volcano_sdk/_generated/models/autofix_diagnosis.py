from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.autofix_diagnosis_confidence import AutofixDiagnosisConfidence
from ..models.autofix_diagnosis_confidence import check_autofix_diagnosis_confidence
from typing import cast

if TYPE_CHECKING:
  from ..models.autofix_evidence import AutofixEvidence





T = TypeVar("T", bound="AutofixDiagnosis")



@_attrs_define
class AutofixDiagnosis:
    """ 
        Attributes:
            summary (str): One or two sentences on what goes wrong.
            root_cause (str):
            evidence (list[AutofixEvidence]):
            suggested_fix (str):
            confidence (AutofixDiagnosisConfidence):
            fixable (bool): Whether a change to the project's code would fix the issue.
            files (list[str]): Repository paths a fix would change.
     """

    summary: str
    root_cause: str
    evidence: list[AutofixEvidence]
    suggested_fix: str
    confidence: AutofixDiagnosisConfidence
    fixable: bool
    files: list[str]





    def to_dict(self) -> dict[str, Any]:
        from ..models.autofix_evidence import AutofixEvidence # noqa: PLC0415
        summary = self.summary

        root_cause = self.root_cause

        evidence = []
        for evidence_item_data in self.evidence:
            evidence_item = evidence_item_data.to_dict()
            evidence.append(evidence_item)



        suggested_fix = self.suggested_fix

        confidence: str = self.confidence

        fixable = self.fixable

        files = self.files




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "summary": summary,
            "root_cause": root_cause,
            "evidence": evidence,
            "suggested_fix": suggested_fix,
            "confidence": confidence,
            "fixable": fixable,
            "files": files,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.autofix_evidence import AutofixEvidence # noqa: PLC0415
        d = dict(src_dict)
        summary = d.pop("summary")

        root_cause = d.pop("root_cause")

        evidence = []
        _evidence = d.pop("evidence")
        for evidence_item_data in (_evidence):
            evidence_item = AutofixEvidence.from_dict(evidence_item_data)



            evidence.append(evidence_item)


        suggested_fix = d.pop("suggested_fix")

        confidence = check_autofix_diagnosis_confidence(d.pop("confidence"))




        fixable = d.pop("fixable")

        files = cast(list[str], d.pop("files"))


        autofix_diagnosis = cls(
            summary=summary,
            root_cause=root_cause,
            evidence=evidence,
            suggested_fix=suggested_fix,
            confidence=confidence,
            fixable=fixable,
            files=files,
        )

        return autofix_diagnosis

