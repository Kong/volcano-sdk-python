from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.database_migration_history_entry import DatabaseMigrationHistoryEntry





T = TypeVar("T", bound="DatabaseMigrations")



@_attrs_define
class DatabaseMigrations:
    """ 
        Attributes:
            history (list[DatabaseMigrationHistoryEntry]): Every file the history records, in name order.
            active_run_id (UUID | Unset): The run that is queued or running, if any.
     """

    history: list[DatabaseMigrationHistoryEntry]
    active_run_id: UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.database_migration_history_entry import DatabaseMigrationHistoryEntry # noqa: PLC0415
        history = []
        for history_item_data in self.history:
            history_item = history_item_data.to_dict()
            history.append(history_item)



        active_run_id: str | Unset = UNSET
        if not isinstance(self.active_run_id, Unset):
            active_run_id = str(self.active_run_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "history": history,
        })
        if active_run_id is not UNSET:
            field_dict["active_run_id"] = active_run_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.database_migration_history_entry import DatabaseMigrationHistoryEntry # noqa: PLC0415
        d = dict(src_dict)
        history = []
        _history = d.pop("history")
        for history_item_data in (_history):
            history_item = DatabaseMigrationHistoryEntry.from_dict(history_item_data)



            history.append(history_item)


        _active_run_id = d.pop("active_run_id", UNSET)
        active_run_id: UUID | Unset
        if isinstance(_active_run_id,  Unset):
            active_run_id = UNSET
        else:
            active_run_id = UUID(_active_run_id)




        database_migrations = cls(
            history=history,
            active_run_id=active_run_id,
        )


        database_migrations.additional_properties = d
        return database_migrations

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
