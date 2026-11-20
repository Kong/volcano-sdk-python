from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_scan_source import check_lavaflow_scan_source
from ..models.lavaflow_scan_source import LavaflowScanSource
from ..models.lavaflow_scan_status import check_lavaflow_scan_status
from ..models.lavaflow_scan_status import LavaflowScanStatus
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.lavaflow_scan_billed_finding import LavaflowScanBilledFinding
  from ..models.lavaflow_scan_counts import LavaflowScanCounts
  from ..models.lavaflow_scan_resource import LavaflowScanResource





T = TypeVar("T", bound="LavaflowScan")



@_attrs_define
class LavaflowScan:
    """ One Code Quality scan of the code a project's deploys changed.

        Attributes:
            id (None | UUID): The scan's ID, null while it is waiting.
            project_id (UUID):
            source (LavaflowScanSource): What asked for the scan.
            status (LavaflowScanStatus): Where the scan stands. `waiting` is the project's next scan: deploys that went live
                since the last one, waiting out a short settle window or a bound named by `waiting_reason`.
            outcome (None | str): How a finished scan ended: `scanned`; `no_changes` when the deploy changed nothing since
                the last scan, as after a redeploy or a rollback; `no_base` when there was no earlier commit to compare against,
                so the head became the starting point; `unreachable` when the head commit is on neither the project's production
                branch nor the repository's default branch; `repository_changed`; `failed`; or `cancelled`. Null until it ends.
            waiting_reason (None | str): The bound a waiting scan waits at: `findings_limit`, `pull_request_limit`,
                `spend_limit`, `scan_limit` or `feature_unavailable`. Null while it only waits out its settle window, and for a
                scan that started. A waiting scan skips no deploy: it covers every commit since the last scan when it starts.
            repository_id (int): The GitHub repository the scan reads.
            base_sha (None | str): The commit the scan compares against, null while waiting or when there was none.
            head_sha (str): The newest deployed commit the scan covers.
            resources (list[LavaflowScanResource]):
            truncated (bool): Whether the scan reviewed only part of the change. A change too large to review whole keeps
                the files with the most changed lines, a review that stops early keeps what it found, and a repository too large
                to read whole skips the files past what it read. No later scan covers the rest.
            counts (LavaflowScanCounts): What the scan did with the problems it found.
            billed (list[LavaflowScanBilledFinding]): The scan's findings whose runs were billed.
            requested_at (datetime.datetime): When the first deploy the scan covers asked for it.
            started_at (datetime.datetime | None):
            completed_at (datetime.datetime | None):
     """

    id: None | UUID
    project_id: UUID
    source: LavaflowScanSource
    status: LavaflowScanStatus
    outcome: None | str
    waiting_reason: None | str
    repository_id: int
    base_sha: None | str
    head_sha: str
    resources: list[LavaflowScanResource]
    truncated: bool
    counts: LavaflowScanCounts
    billed: list[LavaflowScanBilledFinding]
    requested_at: datetime.datetime
    started_at: datetime.datetime | None
    completed_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_scan_billed_finding import LavaflowScanBilledFinding # noqa: PLC0415
        from ..models.lavaflow_scan_counts import LavaflowScanCounts # noqa: PLC0415
        from ..models.lavaflow_scan_resource import LavaflowScanResource # noqa: PLC0415
        id: None | str
        if isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        project_id = str(self.project_id)

        source: str = self.source

        status: str = self.status

        outcome: None | str
        outcome = self.outcome

        waiting_reason: None | str
        waiting_reason = self.waiting_reason

        repository_id = self.repository_id

        base_sha: None | str
        base_sha = self.base_sha

        head_sha = self.head_sha

        resources = []
        for resources_item_data in self.resources:
            resources_item = resources_item_data.to_dict()
            resources.append(resources_item)



        truncated = self.truncated

        counts = self.counts.to_dict()

        billed = []
        for billed_item_data in self.billed:
            billed_item = billed_item_data.to_dict()
            billed.append(billed_item)



        requested_at = self.requested_at.isoformat()

        started_at: None | str
        if isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        completed_at: None | str
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "project_id": project_id,
            "source": source,
            "status": status,
            "outcome": outcome,
            "waiting_reason": waiting_reason,
            "repository_id": repository_id,
            "base_sha": base_sha,
            "head_sha": head_sha,
            "resources": resources,
            "truncated": truncated,
            "counts": counts,
            "billed": billed,
            "requested_at": requested_at,
            "started_at": started_at,
            "completed_at": completed_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_scan_billed_finding import LavaflowScanBilledFinding # noqa: PLC0415
        from ..models.lavaflow_scan_counts import LavaflowScanCounts # noqa: PLC0415
        from ..models.lavaflow_scan_resource import LavaflowScanResource # noqa: PLC0415
        d = dict(src_dict)
        def _parse_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                id_type_0 = UUID(data)



                return id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        id = _parse_id(d.pop("id"))


        project_id = UUID(d.pop("project_id"))




        source = check_lavaflow_scan_source(d.pop("source"))




        status = check_lavaflow_scan_status(d.pop("status"))




        def _parse_outcome(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        outcome = _parse_outcome(d.pop("outcome"))


        def _parse_waiting_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        waiting_reason = _parse_waiting_reason(d.pop("waiting_reason"))


        repository_id = d.pop("repository_id")

        def _parse_base_sha(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        base_sha = _parse_base_sha(d.pop("base_sha"))


        head_sha = d.pop("head_sha")

        resources = []
        _resources = d.pop("resources")
        for resources_item_data in (_resources):
            resources_item = LavaflowScanResource.from_dict(resources_item_data)



            resources.append(resources_item)


        truncated = d.pop("truncated")

        counts = LavaflowScanCounts.from_dict(d.pop("counts"))




        billed = []
        _billed = d.pop("billed")
        for billed_item_data in (_billed):
            billed_item = LavaflowScanBilledFinding.from_dict(billed_item_data)



            billed.append(billed_item)


        requested_at = datetime.datetime.fromisoformat(d.pop("requested_at"))




        def _parse_started_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = datetime.datetime.fromisoformat(data)



                return started_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        started_at = _parse_started_at(d.pop("started_at"))


        def _parse_completed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = datetime.datetime.fromisoformat(data)



                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        completed_at = _parse_completed_at(d.pop("completed_at"))


        lavaflow_scan = cls(
            id=id,
            project_id=project_id,
            source=source,
            status=status,
            outcome=outcome,
            waiting_reason=waiting_reason,
            repository_id=repository_id,
            base_sha=base_sha,
            head_sha=head_sha,
            resources=resources,
            truncated=truncated,
            counts=counts,
            billed=billed,
            requested_at=requested_at,
            started_at=started_at,
            completed_at=completed_at,
        )


        lavaflow_scan.additional_properties = d
        return lavaflow_scan

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
