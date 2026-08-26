from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_anon_key_body_permissions_item import check_create_anon_key_body_permissions_item
from ..models.create_anon_key_body_permissions_item import CreateAnonKeyBodyPermissionsItem
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="CreateAnonKeyBody")



@_attrs_define
class CreateAnonKeyBody:
    """ 
        Attributes:
            name (str): Key name for identification.
                Can only contain letters, numbers, underscores, and hyphens.
                 Example: frontend-app.
            permissions (list[CreateAnonKeyBodyPermissionsItem] | Unset): Optional list of permissions for this key.
                If not provided, defaults to auth-only permissions: auth.signup, auth.signin, auth.refresh, auth.logout,
                auth.password_reset, auth.confirm_email, auth.resend_confirmation.
                Storage, realtime, and functions permissions must be explicitly added if needed.
                 Example: ['auth.signup', 'auth.signin', 'auth.refresh', 'auth.logout'].
     """

    name: str
    permissions: list[CreateAnonKeyBodyPermissionsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        permissions: list[str] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item: str = permissions_item_data
                permissions.append(permissions_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
        })
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        _permissions = d.pop("permissions", UNSET)
        permissions: list[CreateAnonKeyBodyPermissionsItem] | Unset = UNSET
        if _permissions is not UNSET:
            permissions = []
            for permissions_item_data in _permissions:
                permissions_item = check_create_anon_key_body_permissions_item(permissions_item_data)



                permissions.append(permissions_item)


        create_anon_key_body = cls(
            name=name,
            permissions=permissions,
        )


        create_anon_key_body.additional_properties = d
        return create_anon_key_body

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
