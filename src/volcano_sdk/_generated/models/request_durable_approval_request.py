from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="RequestDurableApprovalRequest")



@_attrs_define
class RequestDurableApprovalRequest:
    """ 
        Attributes:
            execution_ref (str): Opaque reference to the running execution, supplied by the SDK.
            callback_id (str): Opaque approval reference, supplied by the SDK.
            name (str):
            title (str):
            description (str | Unset):
            details (Any | Unset): Any JSON value to show the person deciding. The whole request is
                limited to 64 KiB.
     """

    execution_ref: str
    callback_id: str
    name: str
    title: str
    description: str | Unset = UNSET
    details: Any | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        execution_ref = self.execution_ref

        callback_id = self.callback_id

        name = self.name

        title = self.title

        description = self.description

        details = self.details


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "execution_ref": execution_ref,
            "callback_id": callback_id,
            "name": name,
            "title": title,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        execution_ref = d.pop("execution_ref")

        callback_id = d.pop("callback_id")

        name = d.pop("name")

        title = d.pop("title")

        description = d.pop("description", UNSET)

        details = d.pop("details", UNSET)

        request_durable_approval_request = cls(
            execution_ref=execution_ref,
            callback_id=callback_id,
            name=name,
            title=title,
            description=description,
            details=details,
        )

        return request_durable_approval_request

