from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.storage_object import StorageObject





T = TypeVar("T", bound="StorageListResponse")



@_attrs_define
class StorageListResponse:
    """ 
        Attributes:
            objects (list[StorageObject] | Unset):
            next_cursor (str | Unset): Cursor for next page (empty if no more results)
     """

    objects: list[StorageObject] | Unset = UNSET
    next_cursor: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.storage_object import StorageObject
        objects: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.objects, Unset):
            objects = []
            for objects_item_data in self.objects:
                objects_item = objects_item_data.to_dict()
                objects.append(objects_item)



        next_cursor = self.next_cursor


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if objects is not UNSET:
            field_dict["objects"] = objects
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.storage_object import StorageObject
        d = dict(src_dict)
        _objects = d.pop("objects", UNSET)
        objects: list[StorageObject] | Unset = UNSET
        if _objects is not UNSET:
            objects = []
            for objects_item_data in _objects:
                objects_item = StorageObject.from_dict(objects_item_data)



                objects.append(objects_item)


        next_cursor = d.pop("next_cursor", UNSET)

        storage_list_response = cls(
            objects=objects,
            next_cursor=next_cursor,
        )


        storage_list_response.additional_properties = d
        return storage_list_response

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
