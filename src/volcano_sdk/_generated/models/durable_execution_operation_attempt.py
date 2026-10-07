from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.durable_execution_operation_attempt_status import check_durable_execution_operation_attempt_status
from ..models.durable_execution_operation_attempt_status import DurableExecutionOperationAttemptStatus
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.durable_execution_error import DurableExecutionError





T = TypeVar("T", bound="DurableExecutionOperationAttempt")



@_attrs_define
class DurableExecutionOperationAttempt:
    """ One run of a step's body.

        Attributes:
            attempt (int): The attempt's number, starting at 1.
            status (DurableExecutionOperationAttemptStatus): How the attempt ended. A `waitUntil` check whose condition did
                not
                hold yet is `succeeded`: the check ran, and the poll continues.
            started_at (datetime.datetime):
            ended_at (datetime.datetime | Unset): Present once the attempt has ended.
            error (DurableExecutionError | Unset): Why a failed or timed-out execution ended.
     """

    attempt: int
    status: DurableExecutionOperationAttemptStatus
    started_at: datetime.datetime
    ended_at: datetime.datetime | Unset = UNSET
    error: DurableExecutionError | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.durable_execution_error import DurableExecutionError # noqa: PLC0415
        attempt = self.attempt

        status: str = self.status

        started_at = self.started_at.isoformat()

        ended_at: str | Unset = UNSET
        if not isinstance(self.ended_at, Unset):
            ended_at = self.ended_at.isoformat()

        error: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "attempt": attempt,
            "status": status,
            "started_at": started_at,
        })
        if ended_at is not UNSET:
            field_dict["ended_at"] = ended_at
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.durable_execution_error import DurableExecutionError # noqa: PLC0415
        d = dict(src_dict)
        attempt = d.pop("attempt")

        status = check_durable_execution_operation_attempt_status(d.pop("status"))




        started_at = datetime.datetime.fromisoformat(d.pop("started_at"))




        _ended_at = d.pop("ended_at", UNSET)
        ended_at: datetime.datetime | Unset
        if isinstance(_ended_at,  Unset):
            ended_at = UNSET
        else:
            ended_at = datetime.datetime.fromisoformat(_ended_at)




        _error = d.pop("error", UNSET)
        error: DurableExecutionError | Unset
        if isinstance(_error,  Unset):
            error = UNSET
        else:
            error = DurableExecutionError.from_dict(_error)




        durable_execution_operation_attempt = cls(
            attempt=attempt,
            status=status,
            started_at=started_at,
            ended_at=ended_at,
            error=error,
        )


        durable_execution_operation_attempt.additional_properties = d
        return durable_execution_operation_attempt

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
