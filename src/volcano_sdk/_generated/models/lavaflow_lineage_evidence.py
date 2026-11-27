from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_lineage_evidence_confidence import check_lavaflow_lineage_evidence_confidence
from ..models.lavaflow_lineage_evidence_confidence import LavaflowLineageEvidenceConfidence
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.lavaflow_lineage_evidence_deployment import LavaflowLineageEvidenceDeployment
  from ..models.lavaflow_run_reference import LavaflowRunReference





T = TypeVar("T", bound="LavaflowLineageEvidence")



@_attrs_define
class LavaflowLineageEvidence:
    """ What tied the run's issue to a recent LavaFlow fix. A `display` link rests on less than a strong one and joins no
    lineage.

        Attributes:
            confidence (LavaflowLineageEvidenceConfidence): `strong` or `display`. `weak` is reserved: nothing writes it.
            parent (LavaflowRunReference): Another LavaFlow run of the same project.
            deployment (LavaflowLineageEvidenceDeployment):
            previous_commit_sha (None | str): The commit of the deployment before it.
            fix_live_at (datetime.datetime):
            opened_at (datetime.datetime): The occurrence attribution judged.
            overlapping_functions (list[str]):
            overlapping_files (list[str]):
     """

    confidence: LavaflowLineageEvidenceConfidence
    parent: LavaflowRunReference
    deployment: LavaflowLineageEvidenceDeployment
    previous_commit_sha: None | str
    fix_live_at: datetime.datetime
    opened_at: datetime.datetime
    overlapping_functions: list[str]
    overlapping_files: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_lineage_evidence_deployment import LavaflowLineageEvidenceDeployment # noqa: PLC0415
        from ..models.lavaflow_run_reference import LavaflowRunReference # noqa: PLC0415
        confidence: str = self.confidence

        parent = self.parent.to_dict()

        deployment = self.deployment.to_dict()

        previous_commit_sha: None | str
        previous_commit_sha = self.previous_commit_sha

        fix_live_at = self.fix_live_at.isoformat()

        opened_at = self.opened_at.isoformat()

        overlapping_functions = self.overlapping_functions



        overlapping_files = self.overlapping_files




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "confidence": confidence,
            "parent": parent,
            "deployment": deployment,
            "previous_commit_sha": previous_commit_sha,
            "fix_live_at": fix_live_at,
            "opened_at": opened_at,
            "overlapping_functions": overlapping_functions,
            "overlapping_files": overlapping_files,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_lineage_evidence_deployment import LavaflowLineageEvidenceDeployment # noqa: PLC0415
        from ..models.lavaflow_run_reference import LavaflowRunReference # noqa: PLC0415
        d = dict(src_dict)
        confidence = check_lavaflow_lineage_evidence_confidence(d.pop("confidence"))




        parent = LavaflowRunReference.from_dict(d.pop("parent"))




        deployment = LavaflowLineageEvidenceDeployment.from_dict(d.pop("deployment"))




        def _parse_previous_commit_sha(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        previous_commit_sha = _parse_previous_commit_sha(d.pop("previous_commit_sha"))


        fix_live_at = datetime.datetime.fromisoformat(d.pop("fix_live_at"))




        opened_at = datetime.datetime.fromisoformat(d.pop("opened_at"))




        overlapping_functions = cast(list[str], d.pop("overlapping_functions"))


        overlapping_files = cast(list[str], d.pop("overlapping_files"))


        lavaflow_lineage_evidence = cls(
            confidence=confidence,
            parent=parent,
            deployment=deployment,
            previous_commit_sha=previous_commit_sha,
            fix_live_at=fix_live_at,
            opened_at=opened_at,
            overlapping_functions=overlapping_functions,
            overlapping_files=overlapping_files,
        )


        lavaflow_lineage_evidence.additional_properties = d
        return lavaflow_lineage_evidence

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
