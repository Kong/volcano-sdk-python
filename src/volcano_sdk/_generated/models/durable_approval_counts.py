from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="DurableApprovalCounts")



@_attrs_define
class DurableApprovalCounts:
    """ Approvals by status. `requested` is every approval, whatever its status.

        Attributes:
            requested (int):
            pending (int):
            approved (int):
            denied (int):
            expired (int):
            cancelled (int):
     """

    requested: int
    pending: int
    approved: int
    denied: int
    expired: int
    cancelled: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        requested = self.requested

        pending = self.pending

        approved = self.approved

        denied = self.denied

        expired = self.expired

        cancelled = self.cancelled


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "requested": requested,
            "pending": pending,
            "approved": approved,
            "denied": denied,
            "expired": expired,
            "cancelled": cancelled,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        requested = d.pop("requested")

        pending = d.pop("pending")

        approved = d.pop("approved")

        denied = d.pop("denied")

        expired = d.pop("expired")

        cancelled = d.pop("cancelled")

        durable_approval_counts = cls(
            requested=requested,
            pending=pending,
            approved=approved,
            denied=denied,
            expired=expired,
            cancelled=cancelled,
        )


        durable_approval_counts.additional_properties = d
        return durable_approval_counts

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
