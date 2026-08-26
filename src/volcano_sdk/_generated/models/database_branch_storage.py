from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="DatabaseBranchStorage")



@_attrs_define
class DatabaseBranchStorage:
    """ One branch's contribution to its parent database's storage.

        Attributes:
            id (UUID):
            name (str): Branch name
            storage_bytes (int): Bytes this branch has diverged from its parent. Pages the branch
                still shares with the parent are not counted, so this is what the
                branch actually adds to the total rather than its apparent size.
     """

    id: UUID
    name: str
    storage_bytes: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        storage_bytes = self.storage_bytes


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
            "storage_bytes": storage_bytes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        name = d.pop("name")

        storage_bytes = d.pop("storage_bytes")

        database_branch_storage = cls(
            id=id,
            name=name,
            storage_bytes=storage_bytes,
        )


        database_branch_storage.additional_properties = d
        return database_branch_storage

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
