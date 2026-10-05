from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.durable_execution_status import check_durable_execution_status
from ..models.durable_execution_status import DurableExecutionStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.durable_execution_error import DurableExecutionError





T = TypeVar("T", bound="DurableExecution")



@_attrs_define
class DurableExecution:
    """ 
        Attributes:
            id (UUID):
            function_id (UUID):
            name (str): Idempotency key for the execution. Supplied by the client through
                `X-Volcano-Execution-Name`, otherwise generated.
            status (DurableExecutionStatus): Lifecycle state of an execution. `pending` covers the window between the
                platform reserving the execution name and the function accepting the
                start, and has no counterpart once the execution is under way.
                `succeeded`, `failed`, `timed_out`, `stopped` and `unknown` are
                terminal.

                `unknown` means the platform lost track of the execution's outcome: it
                was never seen to finish and is no longer reported, so no result or
                error can be given for it. It is terminal because nothing can settle it
                later, and it is rare — treat it as an outcome to retry under a new
                name rather than a state to wait on. `completed_at` on an `unknown`
                execution is when the platform gave up, not when the work ended.
            region (str): Region the execution runs in. An execution is pinned to one region
                for its whole life because its checkpoints live there.
            created_at (datetime.datetime):
            result (Any | Unset): Whatever the function returned, verbatim. Absent while the execution
                is still running, absent when the result was too large to return and
                was checkpointed instead, and absent once the retention period has
                lapsed.
            result_expired (bool | Unset): `true` when the execution is terminal but its result is no longer
                retained, which distinguishes a discarded result from an empty one.
                Shortly after that the execution itself is dropped and reads answer
                `404`.

                A result that was checkpointed rather than returned leaves this
                unset, so it reads like a function that returned nothing.
            error (DurableExecutionError | Unset): Why a failed or timed-out execution ended.
            completed_at (datetime.datetime | Unset): Present once the execution has reached a terminal status.
     """

    id: UUID
    function_id: UUID
    name: str
    status: DurableExecutionStatus
    region: str
    created_at: datetime.datetime
    result: Any | Unset = UNSET
    result_expired: bool | Unset = UNSET
    error: DurableExecutionError | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.durable_execution_error import DurableExecutionError
        id = str(self.id)

        function_id = str(self.function_id)

        name = self.name

        status: str = self.status

        region = self.region

        created_at = self.created_at.isoformat()

        result = self.result

        result_expired = self.result_expired

        error: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "function_id": function_id,
            "name": name,
            "status": status,
            "region": region,
            "created_at": created_at,
        })
        if result is not UNSET:
            field_dict["result"] = result
        if result_expired is not UNSET:
            field_dict["result_expired"] = result_expired
        if error is not UNSET:
            field_dict["error"] = error
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.durable_execution_error import DurableExecutionError
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        function_id = UUID(d.pop("function_id"))




        name = d.pop("name")

        status = check_durable_execution_status(d.pop("status"))




        region = d.pop("region")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        result = d.pop("result", UNSET)

        result_expired = d.pop("result_expired", UNSET)

        _error = d.pop("error", UNSET)
        error: DurableExecutionError | Unset
        if isinstance(_error,  Unset):
            error = UNSET
        else:
            error = DurableExecutionError.from_dict(_error)




        _completed_at = d.pop("completed_at", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at,  Unset):
            completed_at = UNSET
        else:
            completed_at = datetime.datetime.fromisoformat(_completed_at)




        durable_execution = cls(
            id=id,
            function_id=function_id,
            name=name,
            status=status,
            region=region,
            created_at=created_at,
            result=result,
            result_expired=result_expired,
            error=error,
            completed_at=completed_at,
        )


        durable_execution.additional_properties = d
        return durable_execution

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
