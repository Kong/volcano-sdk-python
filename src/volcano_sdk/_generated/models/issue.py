from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.issue_status import check_issue_status
from ..models.issue_status import IssueStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.resource_reference import ResourceReference





T = TypeVar("T", bound="Issue")



@_attrs_define
class Issue:
    """ Runtime errors from one function or frontend, grouped by error type and stack.

        Attributes:
            id (UUID):
            project_id (UUID):
            resource (ResourceReference): Stable reference to a Volcano resource.
            title (str): The error type and message, with values such as IDs, numbers, and
                URLs replaced by placeholders like `<uuid>` and `<n>`.
            status (IssueStatus): `open` until someone resolves or ignores the issue. A resolved issue
                seen again reopens.
            exception (bool): Whether the issue holds an exception: one your code threw, or one it
                logged with `console.error(err)` or Python's `logger.exception()`.
                `false` for an error logged any other way, such as a structured log
                line, a logger's error line, or a printed traceback. Once `true`, it
                stays `true`.
            event_count (int): Errors counted in this issue. A retried delivery can count an error twice.
            first_seen_at (datetime.datetime):
            last_seen_at (datetime.datetime):
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            error_type (str | Unset): The exception class, such as `TypeError`. Omitted when the error has none.
            culprit (str | Unset): The innermost frame of your code in the stack, as `function (file)`. For a frontend's
                Next.js build output, the outermost route or page file of the build in the stack, such as
                `.next/server/app/checkout/route.js`, or without one, the outermost file of the build. Omitted without a stack.
            last_region (str | Unset): The region that served the latest error, such as `us-east-1`.
            sample_event_id (str | Unset): The ID of the latest error's log event, while logs retain it.
            sample_event_at (datetime.datetime | Unset): When the latest error's log event was written.
            resolved_at (datetime.datetime | Unset): When the issue was resolved. Present only while it is resolved.
            regressed_at (datetime.datetime | Unset): When a resolved issue was last seen again and reopened.
     """

    id: UUID
    project_id: UUID
    resource: ResourceReference
    title: str
    status: IssueStatus
    exception: bool
    event_count: int
    first_seen_at: datetime.datetime
    last_seen_at: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime
    error_type: str | Unset = UNSET
    culprit: str | Unset = UNSET
    last_region: str | Unset = UNSET
    sample_event_id: str | Unset = UNSET
    sample_event_at: datetime.datetime | Unset = UNSET
    resolved_at: datetime.datetime | Unset = UNSET
    regressed_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.resource_reference import ResourceReference # noqa: PLC0415
        id = str(self.id)

        project_id = str(self.project_id)

        resource = self.resource.to_dict()

        title = self.title

        status: str = self.status

        exception = self.exception

        event_count = self.event_count

        first_seen_at = self.first_seen_at.isoformat()

        last_seen_at = self.last_seen_at.isoformat()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        error_type = self.error_type

        culprit = self.culprit

        last_region = self.last_region

        sample_event_id = self.sample_event_id

        sample_event_at: str | Unset = UNSET
        if not isinstance(self.sample_event_at, Unset):
            sample_event_at = self.sample_event_at.isoformat()

        resolved_at: str | Unset = UNSET
        if not isinstance(self.resolved_at, Unset):
            resolved_at = self.resolved_at.isoformat()

        regressed_at: str | Unset = UNSET
        if not isinstance(self.regressed_at, Unset):
            regressed_at = self.regressed_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "project_id": project_id,
            "resource": resource,
            "title": title,
            "status": status,
            "exception": exception,
            "event_count": event_count,
            "first_seen_at": first_seen_at,
            "last_seen_at": last_seen_at,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if error_type is not UNSET:
            field_dict["error_type"] = error_type
        if culprit is not UNSET:
            field_dict["culprit"] = culprit
        if last_region is not UNSET:
            field_dict["last_region"] = last_region
        if sample_event_id is not UNSET:
            field_dict["sample_event_id"] = sample_event_id
        if sample_event_at is not UNSET:
            field_dict["sample_event_at"] = sample_event_at
        if resolved_at is not UNSET:
            field_dict["resolved_at"] = resolved_at
        if regressed_at is not UNSET:
            field_dict["regressed_at"] = regressed_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_reference import ResourceReference # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        resource = ResourceReference.from_dict(d.pop("resource"))




        title = d.pop("title")

        status = check_issue_status(d.pop("status"))




        exception = d.pop("exception")

        event_count = d.pop("event_count")

        first_seen_at = datetime.datetime.fromisoformat(d.pop("first_seen_at"))




        last_seen_at = datetime.datetime.fromisoformat(d.pop("last_seen_at"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        error_type = d.pop("error_type", UNSET)

        culprit = d.pop("culprit", UNSET)

        last_region = d.pop("last_region", UNSET)

        sample_event_id = d.pop("sample_event_id", UNSET)

        _sample_event_at = d.pop("sample_event_at", UNSET)
        sample_event_at: datetime.datetime | Unset
        if isinstance(_sample_event_at,  Unset):
            sample_event_at = UNSET
        else:
            sample_event_at = datetime.datetime.fromisoformat(_sample_event_at)




        _resolved_at = d.pop("resolved_at", UNSET)
        resolved_at: datetime.datetime | Unset
        if isinstance(_resolved_at,  Unset):
            resolved_at = UNSET
        else:
            resolved_at = datetime.datetime.fromisoformat(_resolved_at)




        _regressed_at = d.pop("regressed_at", UNSET)
        regressed_at: datetime.datetime | Unset
        if isinstance(_regressed_at,  Unset):
            regressed_at = UNSET
        else:
            regressed_at = datetime.datetime.fromisoformat(_regressed_at)




        issue = cls(
            id=id,
            project_id=project_id,
            resource=resource,
            title=title,
            status=status,
            exception=exception,
            event_count=event_count,
            first_seen_at=first_seen_at,
            last_seen_at=last_seen_at,
            created_at=created_at,
            updated_at=updated_at,
            error_type=error_type,
            culprit=culprit,
            last_region=last_region,
            sample_event_id=sample_event_id,
            sample_event_at=sample_event_at,
            resolved_at=resolved_at,
            regressed_at=regressed_at,
        )


        issue.additional_properties = d
        return issue

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
