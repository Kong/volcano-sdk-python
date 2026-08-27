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






T = TypeVar("T", bound="AnonKey")



@_attrs_define
class AnonKey:
    """ 
        Attributes:
            id (UUID):
            name (str):
            key_value (str): JWT token - use this in frontend Authorization header
            project_id (UUID | Unset):
            permissions (list[str] | Unset): Permissions granted to this anon key.
                Auth permissions: auth.signup, auth.signin, auth.refresh, auth.logout, auth.password_reset, auth.confirm_email,
                auth.resend_confirmation
                Storage permissions: storage.upload, storage.download, storage.list, storage.delete
                Realtime permissions: realtime.connect, realtime.subscribe, realtime.publish
                Functions permissions: functions.invoke
                 Example: ['auth.signup', 'auth.signin', 'auth.refresh', 'auth.logout'].
            is_default (bool | Unset): Whether this is the project's configured default anon key. Only one key per project
                can be default.
            created_at (datetime.datetime | Unset):
     """

    id: UUID
    name: str
    key_value: str
    project_id: UUID | Unset = UNSET
    permissions: list[str] | Unset = UNSET
    is_default: bool | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        key_value = self.key_value

        project_id: str | Unset = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        permissions: list[str] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions



        is_default = self.is_default

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
            "key_value": key_value,
        })
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if is_default is not UNSET:
            field_dict["is_default"] = is_default
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        name = d.pop("name")

        key_value = d.pop("key_value")

        _project_id = d.pop("project_id", UNSET)
        project_id: UUID | Unset
        if isinstance(_project_id,  Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)




        permissions = cast(list[str], d.pop("permissions", UNSET))


        is_default = d.pop("is_default", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)




        anon_key = cls(
            id=id,
            name=name,
            key_value=key_value,
            project_id=project_id,
            permissions=permissions,
            is_default=is_default,
            created_at=created_at,
        )


        anon_key.additional_properties = d
        return anon_key

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
