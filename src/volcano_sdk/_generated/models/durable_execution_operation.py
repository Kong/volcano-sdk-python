from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.durable_execution_operation_kind import check_durable_execution_operation_kind
from ..models.durable_execution_operation_kind import DurableExecutionOperationKind
from ..models.durable_execution_operation_status import check_durable_execution_operation_status
from ..models.durable_execution_operation_status import DurableExecutionOperationStatus
from ..models.durable_execution_operation_type import check_durable_execution_operation_type
from ..models.durable_execution_operation_type import DurableExecutionOperationType
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.durable_execution_error import DurableExecutionError
  from ..models.durable_execution_operation_attempt import DurableExecutionOperationAttempt





T = TypeVar("T", bound="DurableExecutionOperation")



@_attrs_define
class DurableExecutionOperation:
    """ One operation on an execution's timeline.

        Attributes:
            id (str): Identifies the operation within its execution.
            type_ (DurableExecutionOperationType): The kind of checkpointed operation Volcano recorded.
            kind (DurableExecutionOperationKind): The operation as the handler wrote it: `ctx.step` is `step`,
                `ctx.wait` is `wait`, `ctx.waitUntil` is `wait_until`, `ctx.child`
                is `child`, `ctx.map` is `map` with one `map_item` per item, and
                `ctx.parallel` is `parallel` with one `parallel_branch` per branch.
            status (DurableExecutionOperationStatus): Where the operation stands. `waiting` holds no runtime: a wait that
                has not elapsed, or a `waitUntil` between checks. `retrying` is a step whose last attempt failed and
                whose next one is scheduled at `next_attempt_at`. Work still open
                when the execution ended is `cancelled` at the moment it ended.
                `unknown` is only ever the execution itself, when its outcome was
                lost with its history, as in the execution's own `unknown` status.
            started_at (datetime.datetime):
            parent_id (str | Unset): The operation this one ran inside: a child context, map item or
                parallel branch, or the execution itself for top-level work. Absent
                only on the execution.
            name (str | Unset): The name the handler gave the operation. Map items and parallel
                branches the handler did not name carry the SDK's positional name,
                such as `map-item-0`. Absent for an unnamed operation.
            ended_at (datetime.datetime | Unset): Present once the operation has ended.
            scheduled_end_at (datetime.datetime | Unset): When a wait is due to elapse.
            next_attempt_at (datetime.datetime | Unset): When a step's next attempt, or a `waitUntil`'s next check, is due.
                Present only while one is scheduled.
            attempts (list[DurableExecutionOperationAttempt] | Unset): Each run of a step's body, in order. Present on steps
                and
                `waitUntil` polls, where each check is an attempt.
            error (DurableExecutionError | Unset): Why a failed or timed-out execution ended.
     """

    id: str
    type_: DurableExecutionOperationType
    kind: DurableExecutionOperationKind
    status: DurableExecutionOperationStatus
    started_at: datetime.datetime
    parent_id: str | Unset = UNSET
    name: str | Unset = UNSET
    ended_at: datetime.datetime | Unset = UNSET
    scheduled_end_at: datetime.datetime | Unset = UNSET
    next_attempt_at: datetime.datetime | Unset = UNSET
    attempts: list[DurableExecutionOperationAttempt] | Unset = UNSET
    error: DurableExecutionError | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.durable_execution_error import DurableExecutionError # noqa: PLC0415
        from ..models.durable_execution_operation_attempt import DurableExecutionOperationAttempt # noqa: PLC0415
        id = self.id

        type_: str = self.type_

        kind: str = self.kind

        status: str = self.status

        started_at = self.started_at.isoformat()

        parent_id = self.parent_id

        name = self.name

        ended_at: str | Unset = UNSET
        if not isinstance(self.ended_at, Unset):
            ended_at = self.ended_at.isoformat()

        scheduled_end_at: str | Unset = UNSET
        if not isinstance(self.scheduled_end_at, Unset):
            scheduled_end_at = self.scheduled_end_at.isoformat()

        next_attempt_at: str | Unset = UNSET
        if not isinstance(self.next_attempt_at, Unset):
            next_attempt_at = self.next_attempt_at.isoformat()

        attempts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.attempts, Unset):
            attempts = []
            for attempts_item_data in self.attempts:
                attempts_item = attempts_item_data.to_dict()
                attempts.append(attempts_item)



        error: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "type": type_,
            "kind": kind,
            "status": status,
            "started_at": started_at,
        })
        if parent_id is not UNSET:
            field_dict["parent_id"] = parent_id
        if name is not UNSET:
            field_dict["name"] = name
        if ended_at is not UNSET:
            field_dict["ended_at"] = ended_at
        if scheduled_end_at is not UNSET:
            field_dict["scheduled_end_at"] = scheduled_end_at
        if next_attempt_at is not UNSET:
            field_dict["next_attempt_at"] = next_attempt_at
        if attempts is not UNSET:
            field_dict["attempts"] = attempts
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.durable_execution_error import DurableExecutionError # noqa: PLC0415
        from ..models.durable_execution_operation_attempt import DurableExecutionOperationAttempt # noqa: PLC0415
        d = dict(src_dict)
        id = d.pop("id")

        type_ = check_durable_execution_operation_type(d.pop("type"))




        kind = check_durable_execution_operation_kind(d.pop("kind"))




        status = check_durable_execution_operation_status(d.pop("status"))




        started_at = datetime.datetime.fromisoformat(d.pop("started_at"))




        parent_id = d.pop("parent_id", UNSET)

        name = d.pop("name", UNSET)

        _ended_at = d.pop("ended_at", UNSET)
        ended_at: datetime.datetime | Unset
        if isinstance(_ended_at,  Unset):
            ended_at = UNSET
        else:
            ended_at = datetime.datetime.fromisoformat(_ended_at)




        _scheduled_end_at = d.pop("scheduled_end_at", UNSET)
        scheduled_end_at: datetime.datetime | Unset
        if isinstance(_scheduled_end_at,  Unset):
            scheduled_end_at = UNSET
        else:
            scheduled_end_at = datetime.datetime.fromisoformat(_scheduled_end_at)




        _next_attempt_at = d.pop("next_attempt_at", UNSET)
        next_attempt_at: datetime.datetime | Unset
        if isinstance(_next_attempt_at,  Unset):
            next_attempt_at = UNSET
        else:
            next_attempt_at = datetime.datetime.fromisoformat(_next_attempt_at)




        _attempts = d.pop("attempts", UNSET)
        attempts: list[DurableExecutionOperationAttempt] | Unset = UNSET
        if _attempts is not UNSET:
            attempts = []
            for attempts_item_data in _attempts:
                attempts_item = DurableExecutionOperationAttempt.from_dict(attempts_item_data)



                attempts.append(attempts_item)


        _error = d.pop("error", UNSET)
        error: DurableExecutionError | Unset
        if isinstance(_error,  Unset):
            error = UNSET
        else:
            error = DurableExecutionError.from_dict(_error)




        durable_execution_operation = cls(
            id=id,
            type_=type_,
            kind=kind,
            status=status,
            started_at=started_at,
            parent_id=parent_id,
            name=name,
            ended_at=ended_at,
            scheduled_end_at=scheduled_end_at,
            next_attempt_at=next_attempt_at,
            attempts=attempts,
            error=error,
        )


        durable_execution_operation.additional_properties = d
        return durable_execution_operation

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
