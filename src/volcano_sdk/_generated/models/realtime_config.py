from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="RealtimeConfig")



@_attrs_define
class RealtimeConfig:
    """ Realtime configuration for a project.
    Note: Message size and channels per connection are plan-based (not configurable).

        Attributes:
            project_id (UUID | Unset): Project ID
            enabled (bool | Unset): Whether realtime is enabled for this project Default: False.
            broadcast_enabled (bool | Unset): Whether broadcast channels are enabled Default: True.
            presence_enabled (bool | Unset): Whether presence tracking is enabled Default: True.
            postgres_changes_enabled (bool | Unset): Whether Postgres change notifications are enabled Default: True.
            created_at (datetime.datetime | Unset): When the configuration was created
            updated_at (datetime.datetime | Unset): When the configuration was last updated
     """

    project_id: UUID | Unset = UNSET
    enabled: bool | Unset = False
    broadcast_enabled: bool | Unset = True
    presence_enabled: bool | Unset = True
    postgres_changes_enabled: bool | Unset = True
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        project_id: str | Unset = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        enabled = self.enabled

        broadcast_enabled = self.broadcast_enabled

        presence_enabled = self.presence_enabled

        postgres_changes_enabled = self.postgres_changes_enabled

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if broadcast_enabled is not UNSET:
            field_dict["broadcast_enabled"] = broadcast_enabled
        if presence_enabled is not UNSET:
            field_dict["presence_enabled"] = presence_enabled
        if postgres_changes_enabled is not UNSET:
            field_dict["postgres_changes_enabled"] = postgres_changes_enabled
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _project_id = d.pop("project_id", UNSET)
        project_id: UUID | Unset
        if isinstance(_project_id,  Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)




        enabled = d.pop("enabled", UNSET)

        broadcast_enabled = d.pop("broadcast_enabled", UNSET)

        presence_enabled = d.pop("presence_enabled", UNSET)

        postgres_changes_enabled = d.pop("postgres_changes_enabled", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)




        _updated_at = d.pop("updated_at", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at,  Unset):
            updated_at = UNSET
        else:
            updated_at = datetime.datetime.fromisoformat(_updated_at)




        realtime_config = cls(
            project_id=project_id,
            enabled=enabled,
            broadcast_enabled=broadcast_enabled,
            presence_enabled=presence_enabled,
            postgres_changes_enabled=postgres_changes_enabled,
            created_at=created_at,
            updated_at=updated_at,
        )


        realtime_config.additional_properties = d
        return realtime_config

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
