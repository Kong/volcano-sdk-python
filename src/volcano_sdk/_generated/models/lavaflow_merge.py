from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_merge_status import check_lavaflow_merge_status
from ..models.lavaflow_merge_status import LavaflowMergeStatus
from typing import cast

if TYPE_CHECKING:
  from ..models.lavaflow_hold_reason import LavaflowHoldReason





T = TypeVar("T", bound="LavaflowMerge")



@_attrs_define
class LavaflowMerge:
    """ Where the run's merge stands. Present for a run that may merge its fix, once its pull request opens.

        Attributes:
            status (LavaflowMergeStatus): `waiting_for_checks`: LavaFlow waits for the checks on the fix's commit. `queued`:
                the fix is in the repository's merge queue. `merged`: the pull request merged. `held`: something in
                `hold_reasons` needs a person. LavaFlow commented on the pull request once and never merges, pushes to, rebases
                or dequeues it again; review it and merge it yourself if you want it. `stopped`: LavaFlow left the pull request
                open for you, for `reason`.
            reason (None | str):
            hold_reasons (list[LavaflowHoldReason]): Why LavaFlow holds the fix. Empty unless `status` is `held`.
            merged_by_lavaflow (bool | None): Whether LavaFlow made the merge: `true` when it merged the fix's commit itself
                or through the merge queue, `false` when someone else merged the pull request while LavaFlow waited. `null`
                unless `status` is `merged`.
     """

    status: LavaflowMergeStatus
    reason: None | str
    hold_reasons: list[LavaflowHoldReason]
    merged_by_lavaflow: bool | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_hold_reason import LavaflowHoldReason # noqa: PLC0415
        status: str = self.status

        reason: None | str
        reason = self.reason

        hold_reasons = []
        for hold_reasons_item_data in self.hold_reasons:
            hold_reasons_item = hold_reasons_item_data.to_dict()
            hold_reasons.append(hold_reasons_item)



        merged_by_lavaflow: bool | None
        merged_by_lavaflow = self.merged_by_lavaflow


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "status": status,
            "reason": reason,
            "hold_reasons": hold_reasons,
            "merged_by_lavaflow": merged_by_lavaflow,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_hold_reason import LavaflowHoldReason # noqa: PLC0415
        d = dict(src_dict)
        status = check_lavaflow_merge_status(d.pop("status"))




        def _parse_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        reason = _parse_reason(d.pop("reason"))


        hold_reasons = []
        _hold_reasons = d.pop("hold_reasons")
        for hold_reasons_item_data in (_hold_reasons):
            hold_reasons_item = LavaflowHoldReason.from_dict(hold_reasons_item_data)



            hold_reasons.append(hold_reasons_item)


        def _parse_merged_by_lavaflow(data: object) -> bool | None:
            if data is None:
                return data
            return cast(bool | None, data)

        merged_by_lavaflow = _parse_merged_by_lavaflow(d.pop("merged_by_lavaflow"))


        lavaflow_merge = cls(
            status=status,
            reason=reason,
            hold_reasons=hold_reasons,
            merged_by_lavaflow=merged_by_lavaflow,
        )


        lavaflow_merge.additional_properties = d
        return lavaflow_merge

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
