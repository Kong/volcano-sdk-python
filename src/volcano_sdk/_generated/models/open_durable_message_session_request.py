from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="OpenDurableMessageSessionRequest")



@_attrs_define
class OpenDurableMessageSessionRequest:
    """ 
        Attributes:
            execution_ref (str): Opaque reference to the running execution, supplied by the SDK.
            callback_id (str): Opaque session reference, supplied by the SDK.
     """

    execution_ref: str
    callback_id: str





    def to_dict(self) -> dict[str, Any]:
        execution_ref = self.execution_ref

        callback_id = self.callback_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "execution_ref": execution_ref,
            "callback_id": callback_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        execution_ref = d.pop("execution_ref")

        callback_id = d.pop("callback_id")

        open_durable_message_session_request = cls(
            execution_ref=execution_ref,
            callback_id=callback_id,
        )

        return open_durable_message_session_request

