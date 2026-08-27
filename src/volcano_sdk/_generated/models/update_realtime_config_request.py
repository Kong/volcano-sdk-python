from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateRealtimeConfigRequest")



@_attrs_define
class UpdateRealtimeConfigRequest:
    """ Request to update realtime configuration.
    Limits (message size, channels per connection) are plan-based and cannot be configured.

        Attributes:
            enabled (bool | Unset): Whether realtime is enabled for this project
            broadcast_enabled (bool | Unset): Whether broadcast channels are enabled
            presence_enabled (bool | Unset): Whether presence tracking is enabled
            postgres_changes_enabled (bool | Unset): Whether Postgres change notifications are enabled
     """

    enabled: bool | Unset = UNSET
    broadcast_enabled: bool | Unset = UNSET
    presence_enabled: bool | Unset = UNSET
    postgres_changes_enabled: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        broadcast_enabled = self.broadcast_enabled

        presence_enabled = self.presence_enabled

        postgres_changes_enabled = self.postgres_changes_enabled


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if broadcast_enabled is not UNSET:
            field_dict["broadcast_enabled"] = broadcast_enabled
        if presence_enabled is not UNSET:
            field_dict["presence_enabled"] = presence_enabled
        if postgres_changes_enabled is not UNSET:
            field_dict["postgres_changes_enabled"] = postgres_changes_enabled

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        broadcast_enabled = d.pop("broadcast_enabled", UNSET)

        presence_enabled = d.pop("presence_enabled", UNSET)

        postgres_changes_enabled = d.pop("postgres_changes_enabled", UNSET)

        update_realtime_config_request = cls(
            enabled=enabled,
            broadcast_enabled=broadcast_enabled,
            presence_enabled=presence_enabled,
            postgres_changes_enabled=postgres_changes_enabled,
        )


        update_realtime_config_request.additional_properties = d
        return update_realtime_config_request

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
