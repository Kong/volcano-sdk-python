from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ListPostgresVersionsResponse200Item")



@_attrs_define
class ListPostgresVersionsResponse200Item:
    """ 
        Attributes:
            version (str | Unset): PostgreSQL major version number Example: 16.
            name (str | Unset): Human-readable version name Example: PostgreSQL 16.
            default (bool | Unset): Whether this is the default version (recommended)
            deprecated (bool | Unset): Whether this version is deprecated (approaching EOL)
     """

    version: str | Unset = UNSET
    name: str | Unset = UNSET
    default: bool | Unset = UNSET
    deprecated: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        version = self.version

        name = self.name

        default = self.default

        deprecated = self.deprecated


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if version is not UNSET:
            field_dict["version"] = version
        if name is not UNSET:
            field_dict["name"] = name
        if default is not UNSET:
            field_dict["default"] = default
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        version = d.pop("version", UNSET)

        name = d.pop("name", UNSET)

        default = d.pop("default", UNSET)

        deprecated = d.pop("deprecated", UNSET)

        list_postgres_versions_response_200_item = cls(
            version=version,
            name=name,
            default=default,
            deprecated=deprecated,
        )


        list_postgres_versions_response_200_item.additional_properties = d
        return list_postgres_versions_response_200_item

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
