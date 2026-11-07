from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.issue_status import check_issue_status
from ..models.issue_status import IssueStatus
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="LavaflowIssueSummary")



@_attrs_define
class LavaflowIssueSummary:
    """ The project issue a run works on.

        Attributes:
            id (UUID):
            title (str): The issue's title: the error type and message, a Code Quality finding's title, or a reported
                problem's title.
            culprit (None | str): The innermost frame of your code, as `function (file)`; for a Code Quality finding, the
                symbol and file it is in, as `symbol (file)`, or the file alone. Null for an error without a stack and for a
                reported problem.
            status (IssueStatus): `open` until someone resolves or ignores the issue. A resolved issue
                seen again reopens. A reported problem resolves when its LavaFlow fix
                merges. Volcano ignores one whose report it deleted before any fix
                merged, so it no longer counts toward the project's open issues.
            event_count (int): Errors the issue has grouped so far; for a Code Quality finding, the scans that saw it; 0 for
                a reported problem.
            last_seen_at (datetime.datetime):
            resolved_at (datetime.datetime | None): When the issue was resolved; null unless it is resolved now.
            regressed_at (datetime.datetime | None): When the issue was last seen again after it was resolved, and reopened;
                null if it never was.
            run_count (int): LavaFlow runs on this issue, this one included.
     """

    id: UUID
    title: str
    culprit: None | str
    status: IssueStatus
    event_count: int
    last_seen_at: datetime.datetime
    resolved_at: datetime.datetime | None
    regressed_at: datetime.datetime | None
    run_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        title = self.title

        culprit: None | str
        culprit = self.culprit

        status: str = self.status

        event_count = self.event_count

        last_seen_at = self.last_seen_at.isoformat()

        resolved_at: None | str
        if isinstance(self.resolved_at, datetime.datetime):
            resolved_at = self.resolved_at.isoformat()
        else:
            resolved_at = self.resolved_at

        regressed_at: None | str
        if isinstance(self.regressed_at, datetime.datetime):
            regressed_at = self.regressed_at.isoformat()
        else:
            regressed_at = self.regressed_at

        run_count = self.run_count


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "title": title,
            "culprit": culprit,
            "status": status,
            "event_count": event_count,
            "last_seen_at": last_seen_at,
            "resolved_at": resolved_at,
            "regressed_at": regressed_at,
            "run_count": run_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        title = d.pop("title")

        def _parse_culprit(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        culprit = _parse_culprit(d.pop("culprit"))


        status = check_issue_status(d.pop("status"))




        event_count = d.pop("event_count")

        last_seen_at = datetime.datetime.fromisoformat(d.pop("last_seen_at"))




        def _parse_resolved_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resolved_at_type_0 = datetime.datetime.fromisoformat(data)



                return resolved_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        resolved_at = _parse_resolved_at(d.pop("resolved_at"))


        def _parse_regressed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                regressed_at_type_0 = datetime.datetime.fromisoformat(data)



                return regressed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        regressed_at = _parse_regressed_at(d.pop("regressed_at"))


        run_count = d.pop("run_count")

        lavaflow_issue_summary = cls(
            id=id,
            title=title,
            culprit=culprit,
            status=status,
            event_count=event_count,
            last_seen_at=last_seen_at,
            resolved_at=resolved_at,
            regressed_at=regressed_at,
            run_count=run_count,
        )


        lavaflow_issue_summary.additional_properties = d
        return lavaflow_issue_summary

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
