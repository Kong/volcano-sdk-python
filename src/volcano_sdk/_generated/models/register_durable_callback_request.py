from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="RegisterDurableCallbackRequest")



@_attrs_define
class RegisterDurableCallbackRequest:
    """ 
        Attributes:
            execution_ref (str): Opaque reference to the running execution, supplied by the SDK.
            callback_id (str): Opaque reference to the waiting step, supplied by the SDK.
            name (str): The waiting step's name, up to 237 printable ASCII characters.
     """

    execution_ref: str
    callback_id: str
    name: str





    def to_dict(self) -> dict[str, Any]:
        execution_ref = self.execution_ref

        callback_id = self.callback_id

        name = self.name


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "execution_ref": execution_ref,
            "callback_id": callback_id,
            "name": name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        execution_ref = d.pop("execution_ref")

        callback_id = d.pop("callback_id")

        name = d.pop("name")

        register_durable_callback_request = cls(
            execution_ref=execution_ref,
            callback_id=callback_id,
            name=name,
        )

        return register_durable_callback_request

