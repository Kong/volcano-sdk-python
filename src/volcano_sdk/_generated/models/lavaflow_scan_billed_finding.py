from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.lavaflow_scan_billed_finding_billable_events import LavaflowScanBilledFindingBillableEvents





T = TypeVar("T", bound="LavaflowScanBilledFinding")



@_attrs_define
class LavaflowScanBilledFinding:
    """ A finding of the scan whose Code Quality runs were billed.

        Attributes:
            issue_id (UUID): The finding's issue. Its `finding` says where the problem is and why.
            rule (str): The rule the finding is about.
            title (str):
            billable_events (LavaflowScanBilledFindingBillableEvents): How many billable events of each kind the finding's
                runs recorded, keyed by kind, such as `issue_diagnosed` and `pull_request_opened`.
     """

    issue_id: UUID
    rule: str
    title: str
    billable_events: LavaflowScanBilledFindingBillableEvents
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_scan_billed_finding_billable_events import LavaflowScanBilledFindingBillableEvents # noqa: PLC0415
        issue_id = str(self.issue_id)

        rule = self.rule

        title = self.title

        billable_events = self.billable_events.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "issue_id": issue_id,
            "rule": rule,
            "title": title,
            "billable_events": billable_events,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_scan_billed_finding_billable_events import LavaflowScanBilledFindingBillableEvents # noqa: PLC0415
        d = dict(src_dict)
        issue_id = UUID(d.pop("issue_id"))




        rule = d.pop("rule")

        title = d.pop("title")

        billable_events = LavaflowScanBilledFindingBillableEvents.from_dict(d.pop("billable_events"))




        lavaflow_scan_billed_finding = cls(
            issue_id=issue_id,
            rule=rule,
            title=title,
            billable_events=billable_events,
        )


        lavaflow_scan_billed_finding.additional_properties = d
        return lavaflow_scan_billed_finding

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
