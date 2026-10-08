from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="DurableApprovalDecisionRequest")



@_attrs_define
class DurableApprovalDecisionRequest:
    """ 
        Attributes:
            comment (str | Unset): A note for the workflow and the approval's history.
     """

    comment: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        comment = self.comment


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        comment = d.pop("comment", UNSET)

        durable_approval_decision_request = cls(
            comment=comment,
        )

        return durable_approval_decision_request

