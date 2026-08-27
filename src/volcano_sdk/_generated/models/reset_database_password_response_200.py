from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ResetDatabasePasswordResponse200")



@_attrs_define
class ResetDatabasePasswordResponse200:
    """ 
        Attributes:
            message (str | Unset):
            role_name (str | Unset): Volcano-managed per-database client login (also the pgproxy routing username) Example:
                volcano_client_11111111-1111-1111-1111-111111111111.
            new_password (str | Unset): New Volcano-managed client password. Always starts with `vpg_`.
            connection_string (str | Unset): Updated pgproxy connection string using Volcano-managed credentials.
     """

    message: str | Unset = UNSET
    role_name: str | Unset = UNSET
    new_password: str | Unset = UNSET
    connection_string: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        message = self.message

        role_name = self.role_name

        new_password = self.new_password

        connection_string = self.connection_string


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if message is not UNSET:
            field_dict["message"] = message
        if role_name is not UNSET:
            field_dict["role_name"] = role_name
        if new_password is not UNSET:
            field_dict["new_password"] = new_password
        if connection_string is not UNSET:
            field_dict["connection_string"] = connection_string

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message", UNSET)

        role_name = d.pop("role_name", UNSET)

        new_password = d.pop("new_password", UNSET)

        connection_string = d.pop("connection_string", UNSET)

        reset_database_password_response_200 = cls(
            message=message,
            role_name=role_name,
            new_password=new_password,
            connection_string=connection_string,
        )


        reset_database_password_response_200.additional_properties = d
        return reset_database_password_response_200

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
