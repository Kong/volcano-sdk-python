from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="SandboxBuildLogPageDataItem")



@_attrs_define
class SandboxBuildLogPageDataItem:
    """
        Attributes:
            timestamp (datetime.datetime):
            message (str):
     """

    timestamp: datetime.datetime
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp.isoformat()

        message = self.message


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "timestamp": timestamp,
            "message": message,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        timestamp = datetime.datetime.fromisoformat(d.pop("timestamp"))




        message = d.pop("message")

        sandbox_build_log_page_data_item = cls(
            timestamp=timestamp,
            message=message,
        )


        sandbox_build_log_page_data_item.additional_properties = d
        return sandbox_build_log_page_data_item

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
