from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="CreateServiceKeyBody")



@_attrs_define
class CreateServiceKeyBody:
    """ 
        Attributes:
            name (str): Descriptive name for the key (e.g., "admin-dashboard", "background-jobs").
                Can only contain letters, numbers, underscores, and hyphens.
                 Example: admin-dashboard.
            permissions (list[str] | Unset): Optional least-privilege scope for the key. When omitted, empty, or
                containing only blank strings, the key is granted full access (["*"])
                for backward compatibility. Provide an explicit list (e.g.
                ["functions.invoke", "locks.manage"]) to restrict the key; "*"
                grants everything. Scope enforcement applies to function invocation,
                storage object operations, and project locks.
                 Example: ['functions.invoke', 'locks.manage'].
     """

    name: str
    permissions: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        permissions: list[str] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions




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

        permissions = cast(list[str], d.pop("permissions", UNSET))


        create_service_key_body = cls(
            name=name,
            permissions=permissions,
        )


        create_service_key_body.additional_properties = d
        return create_service_key_body

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
