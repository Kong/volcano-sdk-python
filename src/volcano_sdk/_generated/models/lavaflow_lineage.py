from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_lineage_confidence import check_lavaflow_lineage_confidence
from ..models.lavaflow_lineage_confidence import LavaflowLineageConfidence
from ..models.lavaflow_lineage_relation import check_lavaflow_lineage_relation
from ..models.lavaflow_lineage_relation import LavaflowLineageRelation
from ..models.lavaflow_lineage_remedy import check_lavaflow_lineage_remedy
from ..models.lavaflow_lineage_remedy import LavaflowLineageRemedy
from ..models.lavaflow_lineage_state import check_lavaflow_lineage_state
from ..models.lavaflow_lineage_state import LavaflowLineageState
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.lavaflow_run_reference import LavaflowRunReference





T = TypeVar("T", bound="LavaflowLineage")



@_attrs_define
class LavaflowLineage:
    """ A chain of LavaFlow fixes: a merged fix, and the runs that followed up an issue traced to it or to a fix after it.

        Attributes:
            id (UUID): The lineage's root run.
            depth (int): 0 for the root fix.
            relation (LavaflowLineageRelation): `regression` for an issue traced to the parent's deploy, `recurrence` for an
                issue that came back after the parent went live. Null for the root.
            confidence (LavaflowLineageConfidence): Null for the root, and otherwise `strong`. `weak` is reserved: nothing
                writes it.
            parent (LavaflowRunReference | None): The fix this run follows up. Null for the root.
            covered_by (LavaflowRunReference | None): The run whose fix also covers this issue, so this run opened nothing.
            remedy (LavaflowLineageRemedy): How the run follows up its parent. Currently always `fix`: a regression gets a
                follow-up fix. `revert` and `none` are reserved.
            state (LavaflowLineageState):
            hold_reason (None | str): Why the lineage holds: `lineage_cap`, `lineage_held` or `repository_changed`. New
                values may appear. Null unless `state` is `held`.
            pull_requests_opened (int): Pull requests the lineage opened, counting the root's.
            pull_request_cap (int): The most pull requests a lineage opens before it holds.
     """

    id: UUID
    depth: int
    relation: LavaflowLineageRelation
    confidence: LavaflowLineageConfidence
    parent: LavaflowRunReference | None
    covered_by: LavaflowRunReference | None
    remedy: LavaflowLineageRemedy
    state: LavaflowLineageState
    hold_reason: None | str
    pull_requests_opened: int
    pull_request_cap: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_run_reference import LavaflowRunReference # noqa: PLC0415
        id = str(self.id)

        depth = self.depth

        relation: str = self.relation

        confidence: str = self.confidence

        parent: dict[str, Any] | None
        if isinstance(self.parent, LavaflowRunReference):
            parent = self.parent.to_dict()
        else:
            parent = self.parent

        covered_by: dict[str, Any] | None
        if isinstance(self.covered_by, LavaflowRunReference):
            covered_by = self.covered_by.to_dict()
        else:
            covered_by = self.covered_by

        remedy: str = self.remedy

        state: str = self.state

        hold_reason: None | str
        hold_reason = self.hold_reason

        pull_requests_opened = self.pull_requests_opened

        pull_request_cap = self.pull_request_cap


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "depth": depth,
            "relation": relation,
            "confidence": confidence,
            "parent": parent,
            "covered_by": covered_by,
            "remedy": remedy,
            "state": state,
            "hold_reason": hold_reason,
            "pull_requests_opened": pull_requests_opened,
            "pull_request_cap": pull_request_cap,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_run_reference import LavaflowRunReference # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        depth = d.pop("depth")

        relation = check_lavaflow_lineage_relation(d.pop("relation"))




        confidence = check_lavaflow_lineage_confidence(d.pop("confidence"))




        def _parse_parent(data: object) -> LavaflowRunReference | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parent_type_1 = LavaflowRunReference.from_dict(data)



                return parent_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowRunReference | None, data)

        parent = _parse_parent(d.pop("parent"))


        def _parse_covered_by(data: object) -> LavaflowRunReference | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                covered_by_type_1 = LavaflowRunReference.from_dict(data)



                return covered_by_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowRunReference | None, data)

        covered_by = _parse_covered_by(d.pop("covered_by"))


        remedy = check_lavaflow_lineage_remedy(d.pop("remedy"))




        state = check_lavaflow_lineage_state(d.pop("state"))




        def _parse_hold_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        hold_reason = _parse_hold_reason(d.pop("hold_reason"))


        pull_requests_opened = d.pop("pull_requests_opened")

        pull_request_cap = d.pop("pull_request_cap")

        lavaflow_lineage = cls(
            id=id,
            depth=depth,
            relation=relation,
            confidence=confidence,
            parent=parent,
            covered_by=covered_by,
            remedy=remedy,
            state=state,
            hold_reason=hold_reason,
            pull_requests_opened=pull_requests_opened,
            pull_request_cap=pull_request_cap,
        )


        lavaflow_lineage.additional_properties = d
        return lavaflow_lineage

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
