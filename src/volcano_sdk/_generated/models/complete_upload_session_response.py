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





T = TypeVar("T", bound="CompleteUploadSessionResponse")



@_attrs_define
class CompleteUploadSessionResponse:
    """ Response when completing an upload

        Attributes:
            object_ (StorageObject | Unset):
     """

    object_: StorageObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.storage_object import StorageObject
        object_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.object_, Unset):
            object_ = self.object_.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if object_ is not UNSET:
            field_dict["object"] = object_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.storage_object import StorageObject
        d = dict(src_dict)
        _object_ = d.pop("object", UNSET)
        object_: StorageObject | Unset
        if isinstance(_object_,  Unset):
            object_ = UNSET
        else:
            object_ = StorageObject.from_dict(_object_)




        complete_upload_session_response = cls(
            object_=object_,
        )


        complete_upload_session_response.additional_properties = d
        return complete_upload_session_response

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
