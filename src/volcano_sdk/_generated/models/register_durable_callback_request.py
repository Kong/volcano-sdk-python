from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="RegisterDurableCallbackRequest")



@_attrs_define
class RegisterDurableCallbackRequest:
    """ 
        Attributes:
            execution_ref (str): Opaque reference to the running execution, supplied by the SDK.
            callback_id (str): Opaque reference to the waiting step, supplied by the SDK.
            name (str): The waiting step's name, up to 237 printable ASCII characters.
            operation_id (str | Unset): The operation an earlier run of the workflow opened the waiting step
                under, supplied by the SDK when a replay registers it. Volcano then
                looks for the step further back in the execution's history than a
                first registration reads.
     """

    execution_ref: str
    callback_id: str
    name: str
    operation_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        execution_ref = self.execution_ref

        callback_id = self.callback_id

        name = self.name

        operation_id = self.operation_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "execution_ref": execution_ref,
            "callback_id": callback_id,
            "name": name,
        })
        if operation_id is not UNSET:
            field_dict["operation_id"] = operation_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        execution_ref = d.pop("execution_ref")

        callback_id = d.pop("callback_id")

        name = d.pop("name")

        operation_id = d.pop("operation_id", UNSET)

        register_durable_callback_request = cls(
            execution_ref=execution_ref,
            callback_id=callback_id,
            name=name,
            operation_id=operation_id,
        )

        return register_durable_callback_request

