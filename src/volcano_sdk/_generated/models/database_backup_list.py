from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.database_backup import DatabaseBackup
  from ..models.database_restore_window import DatabaseRestoreWindow





T = TypeVar("T", bound="DatabaseBackupList")



@_attrs_define
class DatabaseBackupList:
    """ 
        Attributes:
            data (list[DatabaseBackup]):
            restore_window (DatabaseRestoreWindow | Unset): The span a point-in-time restore may target. Absent from the
                response
                when the owner's plan does not include point-in-time restore, and while
                the storage provider has no history window in place yet — briefly the
                case after an upgrade, since the window is applied asynchronously. The
                window is read from the provider rather than from the plan, so it never
                advertises a point a restore could not actually reach.
     """

    data: list[DatabaseBackup]
    restore_window: DatabaseRestoreWindow | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.database_backup import DatabaseBackup
        from ..models.database_restore_window import DatabaseRestoreWindow
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)



        restore_window: dict[str, Any] | Unset = UNSET
        if not isinstance(self.restore_window, Unset):
            restore_window = self.restore_window.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "data": data,
        })
        if restore_window is not UNSET:
            field_dict["restore_window"] = restore_window

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.database_backup import DatabaseBackup
        from ..models.database_restore_window import DatabaseRestoreWindow
        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in (_data):
            data_item = DatabaseBackup.from_dict(data_item_data)



            data.append(data_item)


        _restore_window = d.pop("restore_window", UNSET)
        restore_window: DatabaseRestoreWindow | Unset
        if isinstance(_restore_window,  Unset):
            restore_window = UNSET
        else:
            restore_window = DatabaseRestoreWindow.from_dict(_restore_window)




        database_backup_list = cls(
            data=data,
            restore_window=restore_window,
        )


        database_backup_list.additional_properties = d
        return database_backup_list

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
