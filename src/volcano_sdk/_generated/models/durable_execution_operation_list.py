from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.durable_execution_invocation import DurableExecutionInvocation
  from ..models.durable_execution_operation import DurableExecutionOperation





T = TypeVar("T", bound="DurableExecutionOperationList")



@_attrs_define
class DurableExecutionOperationList:
    """ A durable execution's trace.

        Attributes:
            data (list[DurableExecutionOperation]): Every operation the execution began. The execution itself comes
                first and is the only operation without a `parent_id`; the rest
                follow in the order they started.
            invocations (list[DurableExecutionInvocation]): When the function's code was running, oldest first. An execution
                suspended in a wait holds no runtime, so the gaps between these are
                not charged as compute.
            complete (bool): `true` once the execution has finished and nothing more will be
                recorded. Its operations no longer change, and it is no longer
                refreshed on read; a final invocation window can still be added
                shortly after.
            synced_at (datetime.datetime | Unset): When the trace was last refreshed. Absent before it has been
                refreshed at all. A running execution's trace is usually within
                about ten seconds of the execution, and further behind when many
                executions are being watched at once.
     """

    data: list[DurableExecutionOperation]
    invocations: list[DurableExecutionInvocation]
    complete: bool
    synced_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.durable_execution_invocation import DurableExecutionInvocation # noqa: PLC0415
        from ..models.durable_execution_operation import DurableExecutionOperation # noqa: PLC0415
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)



        invocations = []
        for invocations_item_data in self.invocations:
            invocations_item = invocations_item_data.to_dict()
            invocations.append(invocations_item)



        complete = self.complete

        synced_at: str | Unset = UNSET
        if not isinstance(self.synced_at, Unset):
            synced_at = self.synced_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "data": data,
            "invocations": invocations,
            "complete": complete,
        })
        if synced_at is not UNSET:
            field_dict["synced_at"] = synced_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.durable_execution_invocation import DurableExecutionInvocation # noqa: PLC0415
        from ..models.durable_execution_operation import DurableExecutionOperation # noqa: PLC0415
        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in (_data):
            data_item = DurableExecutionOperation.from_dict(data_item_data)



            data.append(data_item)


        invocations = []
        _invocations = d.pop("invocations")
        for invocations_item_data in (_invocations):
            invocations_item = DurableExecutionInvocation.from_dict(invocations_item_data)



            invocations.append(invocations_item)


        complete = d.pop("complete")

        _synced_at = d.pop("synced_at", UNSET)
        synced_at: datetime.datetime | Unset
        if isinstance(_synced_at,  Unset):
            synced_at = UNSET
        else:
            synced_at = datetime.datetime.fromisoformat(_synced_at)




        durable_execution_operation_list = cls(
            data=data,
            invocations=invocations,
            complete=complete,
            synced_at=synced_at,
        )


        durable_execution_operation_list.additional_properties = d
        return durable_execution_operation_list

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
