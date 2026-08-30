from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="CreateDatabaseRestoreRequest")



@_attrs_define
class CreateDatabaseRestoreRequest:
    """ Names what to restore. Supply exactly one of `backup_name` or
    `restore_to`.

        Attributes:
            backup_name (str | Unset): A backup of this database to restore, exactly as returned by the list
                endpoint.

                Deliberately looser than the names you can create, like the backup
                path parameter: a backup made by a schedule is named for you, so
                restoring one accepts any name a backup can have.
                 Example: before_migration.
            restore_to (datetime.datetime | Unset): A point in time to restore to, which must fall inside the
                `restore_window` reported when listing backups.
                 Example: 2026-01-15T09:30:00Z.
     """

    backup_name: str | Unset = UNSET
    restore_to: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        backup_name = self.backup_name

        restore_to: str | Unset = UNSET
        if not isinstance(self.restore_to, Unset):
            restore_to = self.restore_to.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if backup_name is not UNSET:
            field_dict["backup_name"] = backup_name
        if restore_to is not UNSET:
            field_dict["restore_to"] = restore_to

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        backup_name = d.pop("backup_name", UNSET)

        _restore_to = d.pop("restore_to", UNSET)
        restore_to: datetime.datetime | Unset
        if isinstance(_restore_to,  Unset):
            restore_to = UNSET
        else:
            restore_to = datetime.datetime.fromisoformat(_restore_to)




        create_database_restore_request = cls(
            backup_name=backup_name,
            restore_to=restore_to,
        )


        create_database_restore_request.additional_properties = d
        return create_database_restore_request

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
