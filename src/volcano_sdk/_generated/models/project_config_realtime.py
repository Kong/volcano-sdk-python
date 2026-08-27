from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ProjectConfigRealtime")



@_attrs_define
class ProjectConfigRealtime:
    """ 
        Attributes:
            enabled (bool | Unset):
            broadcast_enabled (bool | Unset):
            presence_enabled (bool | Unset):
            postgres_changes_enabled (bool | Unset):
     """

    enabled: bool | Unset = UNSET
    broadcast_enabled: bool | Unset = UNSET
    presence_enabled: bool | Unset = UNSET
    postgres_changes_enabled: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        broadcast_enabled = self.broadcast_enabled

        presence_enabled = self.presence_enabled

        postgres_changes_enabled = self.postgres_changes_enabled


        field_dict: dict[str, Any] = {}

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

        project_config_realtime = cls(
            enabled=enabled,
            broadcast_enabled=broadcast_enabled,
            presence_enabled=presence_enabled,
            postgres_changes_enabled=postgres_changes_enabled,
        )

        return project_config_realtime

