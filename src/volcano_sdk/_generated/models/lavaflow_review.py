from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_review_stop import check_lavaflow_review_stop
from ..models.lavaflow_review_stop import LavaflowReviewStop
from ..models.lavaflow_review_verdict import check_lavaflow_review_verdict
from ..models.lavaflow_review_verdict import LavaflowReviewVerdict
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.lavaflow_review_finding import LavaflowReviewFinding
  from ..models.lavaflow_review_person_reason import LavaflowReviewPersonReason





T = TypeVar("T", bound="LavaflowReview")



@_attrs_define
class LavaflowReview:
    """ 
        Attributes:
            verdict (LavaflowReviewVerdict): The last review round's verdict. `blocked` means a critical or major finding
                stops the fix; `changes_requested` means only minor findings do; `error` means a reviewer failed without a
                blocking finding, or no reviewer could run.
            rounds (int): The review rounds that ran, 0 when no reviewer could run.
            stopped (LavaflowReviewStop | None): Why the review ended without passing the fix, null when it passed the fix
                or when the run saved no fix.
            open_findings (list[LavaflowReviewFinding] | Unset): The findings the review saved with the fix left open.
                Absent when the review passed the fix, left none open, or the run saved no fix.
            person_reasons (list[LavaflowReviewPersonReason] | Unset): What the review saved with the fix asks a person to
                decide before the fix merges. Absent when it asks nothing or the run saved no fix.
     """

    verdict: LavaflowReviewVerdict
    rounds: int
    stopped: LavaflowReviewStop | None
    open_findings: list[LavaflowReviewFinding] | Unset = UNSET
    person_reasons: list[LavaflowReviewPersonReason] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_review_finding import LavaflowReviewFinding # noqa: PLC0415
        from ..models.lavaflow_review_person_reason import LavaflowReviewPersonReason # noqa: PLC0415
        verdict: str = self.verdict

        rounds = self.rounds

        stopped: None | str
        if isinstance(self.stopped, str):
            stopped = self.stopped
        else:
            stopped = self.stopped

        open_findings: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.open_findings, Unset):
            open_findings = []
            for open_findings_item_data in self.open_findings:
                open_findings_item = open_findings_item_data.to_dict()
                open_findings.append(open_findings_item)



        person_reasons: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.person_reasons, Unset):
            person_reasons = []
            for person_reasons_item_data in self.person_reasons:
                person_reasons_item = person_reasons_item_data.to_dict()
                person_reasons.append(person_reasons_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "verdict": verdict,
            "rounds": rounds,
            "stopped": stopped,
        })
        if open_findings is not UNSET:
            field_dict["open_findings"] = open_findings
        if person_reasons is not UNSET:
            field_dict["person_reasons"] = person_reasons

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_review_finding import LavaflowReviewFinding # noqa: PLC0415
        from ..models.lavaflow_review_person_reason import LavaflowReviewPersonReason # noqa: PLC0415
        d = dict(src_dict)
        verdict = check_lavaflow_review_verdict(d.pop("verdict"))




        rounds = d.pop("rounds")

        def _parse_stopped(data: object) -> LavaflowReviewStop | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                stopped_type_1 = check_lavaflow_review_stop(data)



                return stopped_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowReviewStop | None, data)

        stopped = _parse_stopped(d.pop("stopped"))


        _open_findings = d.pop("open_findings", UNSET)
        open_findings: list[LavaflowReviewFinding] | Unset = UNSET
        if _open_findings is not UNSET:
            open_findings = []
            for open_findings_item_data in _open_findings:
                open_findings_item = LavaflowReviewFinding.from_dict(open_findings_item_data)



                open_findings.append(open_findings_item)


        _person_reasons = d.pop("person_reasons", UNSET)
        person_reasons: list[LavaflowReviewPersonReason] | Unset = UNSET
        if _person_reasons is not UNSET:
            person_reasons = []
            for person_reasons_item_data in _person_reasons:
                person_reasons_item = LavaflowReviewPersonReason.from_dict(person_reasons_item_data)



                person_reasons.append(person_reasons_item)


        lavaflow_review = cls(
            verdict=verdict,
            rounds=rounds,
            stopped=stopped,
            open_findings=open_findings,
            person_reasons=person_reasons,
        )


        lavaflow_review.additional_properties = d
        return lavaflow_review

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
