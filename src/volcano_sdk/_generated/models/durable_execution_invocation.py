from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="DurableExecutionInvocation")



@_attrs_define
class DurableExecutionInvocation:
    """ A window in which the function's code was running.

        Attributes:
            started_at (datetime.datetime):
            ended_at (datetime.datetime):
     """

    started_at: datetime.datetime
    ended_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        started_at = self.started_at.isoformat()

        ended_at = self.ended_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "started_at": started_at,
            "ended_at": ended_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        started_at = datetime.datetime.fromisoformat(d.pop("started_at"))




        ended_at = datetime.datetime.fromisoformat(d.pop("ended_at"))




        durable_execution_invocation = cls(
            started_at=started_at,
            ended_at=ended_at,
        )


        durable_execution_invocation.additional_properties = d
        return durable_execution_invocation

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
