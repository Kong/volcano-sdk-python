from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="DatabaseRestoreWindow")



@_attrs_define
class DatabaseRestoreWindow:
    """ The span a point-in-time restore may target. Absent from the response
    when the owner's plan does not include point-in-time restore, and while
    the storage provider has no history window in place yet — briefly the
    case after an upgrade, since the window is applied asynchronously. The
    window is read from the provider rather than from the plan, so it never
    advertises a point a restore could not actually reach.

        Attributes:
            earliest_restore_at (datetime.datetime | Unset): The oldest point that can still be restored. Moves forward
                continuously as history ages out, so treat it as a lower bound at
                the moment it was read rather than a fixed value.
            latest_restore_at (datetime.datetime | Unset): The most recent point that can be restored, which is now.
     """

    earliest_restore_at: datetime.datetime | Unset = UNSET
    latest_restore_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        earliest_restore_at: str | Unset = UNSET
        if not isinstance(self.earliest_restore_at, Unset):
            earliest_restore_at = self.earliest_restore_at.isoformat()

        latest_restore_at: str | Unset = UNSET
        if not isinstance(self.latest_restore_at, Unset):
            latest_restore_at = self.latest_restore_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if earliest_restore_at is not UNSET:
            field_dict["earliest_restore_at"] = earliest_restore_at
        if latest_restore_at is not UNSET:
            field_dict["latest_restore_at"] = latest_restore_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _earliest_restore_at = d.pop("earliest_restore_at", UNSET)
        earliest_restore_at: datetime.datetime | Unset
        if isinstance(_earliest_restore_at,  Unset):
            earliest_restore_at = UNSET
        else:
            earliest_restore_at = datetime.datetime.fromisoformat(_earliest_restore_at)




        _latest_restore_at = d.pop("latest_restore_at", UNSET)
        latest_restore_at: datetime.datetime | Unset
        if isinstance(_latest_restore_at,  Unset):
            latest_restore_at = UNSET
        else:
            latest_restore_at = datetime.datetime.fromisoformat(_latest_restore_at)




        database_restore_window = cls(
            earliest_restore_at=earliest_restore_at,
            latest_restore_at=latest_restore_at,
        )


        database_restore_window.additional_properties = d
        return database_restore_window

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
