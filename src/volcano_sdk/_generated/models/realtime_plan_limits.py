from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="RealtimePlanLimits")



@_attrs_define
class RealtimePlanLimits:
    """ Plan-based limits for realtime features

        Attributes:
            plan (str | Unset): Plan name (FREE or PRO) Example: FREE.
            max_connections (int | Unset): Maximum concurrent connections allowed Example: 100.
            messages_per_month (int | Unset): Maximum messages per month Example: 1000000.
            message_size_kb (int | Unset): Maximum message size in KB Example: 32.
            channels_per_conn (int | Unset): Maximum channels per connection Example: 100.
     """

    plan: str | Unset = UNSET
    max_connections: int | Unset = UNSET
    messages_per_month: int | Unset = UNSET
    message_size_kb: int | Unset = UNSET
    channels_per_conn: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        plan = self.plan

        max_connections = self.max_connections

        messages_per_month = self.messages_per_month

        message_size_kb = self.message_size_kb

        channels_per_conn = self.channels_per_conn


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if plan is not UNSET:
            field_dict["plan"] = plan
        if max_connections is not UNSET:
            field_dict["max_connections"] = max_connections
        if messages_per_month is not UNSET:
            field_dict["messages_per_month"] = messages_per_month
        if message_size_kb is not UNSET:
            field_dict["message_size_kb"] = message_size_kb
        if channels_per_conn is not UNSET:
            field_dict["channels_per_conn"] = channels_per_conn

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plan = d.pop("plan", UNSET)

        max_connections = d.pop("max_connections", UNSET)

        messages_per_month = d.pop("messages_per_month", UNSET)

        message_size_kb = d.pop("message_size_kb", UNSET)

        channels_per_conn = d.pop("channels_per_conn", UNSET)

        realtime_plan_limits = cls(
            plan=plan,
            max_connections=max_connections,
            messages_per_month=messages_per_month,
            message_size_kb=message_size_kb,
            channels_per_conn=channels_per_conn,
        )


        realtime_plan_limits.additional_properties = d
        return realtime_plan_limits

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
