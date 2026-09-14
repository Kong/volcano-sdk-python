from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="DurableFunctionConfig")



@_attrs_define
class DurableFunctionConfig:
    """ Execution limits the function was created with, derived from the
    project's plan. Fixed for the life of the function: changing them means
    creating a new one.

    The memory the function runs at, and the timeout on one attempt within
    an execution, also come from the plan but are not reported here: they
    are applied to the deployed function rather than recorded on it. Both
    are published per plan in the plans and limits guide.

        Attributes:
            execution_timeout_seconds (int): How long a whole execution may run, including time suspended in a
                wait. This is not a limit on one attempt: an execution outlives any
                single attempt by checkpointing and resuming, and the per-attempt
                timeout is the plan's own, smaller number.
            retention_days (int): How long a finished execution's result and history are retained, for
                as long as the function exists. Deleting the function, or its
                project, ends retention early and takes the history with it.
     """

    execution_timeout_seconds: int
    retention_days: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        execution_timeout_seconds = self.execution_timeout_seconds

        retention_days = self.retention_days


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "execution_timeout_seconds": execution_timeout_seconds,
            "retention_days": retention_days,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        execution_timeout_seconds = d.pop("execution_timeout_seconds")

        retention_days = d.pop("retention_days")

        durable_function_config = cls(
            execution_timeout_seconds=execution_timeout_seconds,
            retention_days=retention_days,
        )


        durable_function_config.additional_properties = d
        return durable_function_config

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
