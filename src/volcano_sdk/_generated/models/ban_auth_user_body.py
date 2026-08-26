from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="BanAuthUserBody")



@_attrs_define
class BanAuthUserBody:
    """ 
        Attributes:
            banned_until (datetime.datetime | Unset): When the ban expires (omit for permanent ban) Example:
                2026-12-31T23:59:59Z.
     """

    banned_until: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        banned_until: str | Unset = UNSET
        if not isinstance(self.banned_until, Unset):
            banned_until = self.banned_until.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if banned_until is not UNSET:
            field_dict["banned_until"] = banned_until

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _banned_until = d.pop("banned_until", UNSET)
        banned_until: datetime.datetime | Unset
        if isinstance(_banned_until,  Unset):
            banned_until = UNSET
        else:
            banned_until = datetime.datetime.fromisoformat(_banned_until)




        ban_auth_user_body = cls(
            banned_until=banned_until,
        )


        ban_auth_user_body.additional_properties = d
        return ban_auth_user_body

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
