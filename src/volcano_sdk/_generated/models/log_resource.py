from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.log_resource_type import check_log_resource_type
from ..models.log_resource_type import LogResourceType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="LogResource")



@_attrs_define
class LogResource:
    """ Resource that owns a historical log event.

        Attributes:
            type_ (LogResourceType): Resource type that owns the log event.
            id (UUID): Resource ID that owns the log event.
            name (str | Unset): Resource name associated with the log event, when available.
     """

    type_: LogResourceType
    id: UUID
    name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        id = str(self.id)

        name = self.name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "id": id,
        })
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_log_resource_type(d.pop("type"))




        id = UUID(d.pop("id"))




        name = d.pop("name", UNSET)

        log_resource = cls(
            type_=type_,
            id=id,
            name=name,
        )


        log_resource.additional_properties = d
        return log_resource

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
