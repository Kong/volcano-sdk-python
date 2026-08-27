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






T = TypeVar("T", bound="ServiceKey")



@_attrs_define
class ServiceKey:
    """ Service role key for admin operations.
    **WARNING:** Bypasses all RLS - backend use only!

        Attributes:
            id (UUID):
            name (str): Descriptive name for the key
            key_prefix (str): First 12 characters of the key for display/identification
            permissions (list[str]): Operations this key may perform. ["*"] grants full admin access
                (default for keys created without an explicit scope). Scoped keys
                list specific permissions, e.g. ["functions.invoke", "locks.manage"].
                 Example: ['*'].
            project_id (UUID | Unset):
            key_value (str | Unset): Full JWT token for Authorization header.
                Returned on create, get, and list (decrypted from storage).
                **Store securely - NEVER expose in frontend code!**
            created_at (datetime.datetime | Unset):
            updated_at (datetime.datetime | Unset):
     """

    id: UUID
    name: str
    key_prefix: str
    permissions: list[str]
    project_id: UUID | Unset = UNSET
    key_value: str | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        key_prefix = self.key_prefix

        permissions = self.permissions



        project_id: str | Unset = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        key_value = self.key_value

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
            "key_prefix": key_prefix,
            "permissions": permissions,
        })
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if key_value is not UNSET:
            field_dict["key_value"] = key_value
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        name = d.pop("name")

        key_prefix = d.pop("key_prefix")

        permissions = cast(list[str], d.pop("permissions"))


        _project_id = d.pop("project_id", UNSET)
        project_id: UUID | Unset
        if isinstance(_project_id,  Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)




        key_value = d.pop("key_value", UNSET)

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




        service_key = cls(
            id=id,
            name=name,
            key_prefix=key_prefix,
            permissions=permissions,
            project_id=project_id,
            key_value=key_value,
            created_at=created_at,
            updated_at=updated_at,
        )


        service_key.additional_properties = d
        return service_key

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
