from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.update_database_type_request_database_type import check_update_database_type_request_database_type
from ..models.update_database_type_request_database_type import UpdateDatabaseTypeRequestDatabaseType
from typing import cast






T = TypeVar("T", bound="UpdateDatabaseTypeRequest")



@_attrs_define
class UpdateDatabaseTypeRequest:
    """ Update database compute size tier

        Attributes:
            database_type (UpdateDatabaseTypeRequestDatabaseType): New compute size tier Example: volcano-db-m.
     """

    database_type: UpdateDatabaseTypeRequestDatabaseType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        database_type: str = self.database_type


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "database_type": database_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        database_type = check_update_database_type_request_database_type(d.pop("database_type"))




        update_database_type_request = cls(
            database_type=database_type,
        )


        update_database_type_request.additional_properties = d
        return update_database_type_request

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
