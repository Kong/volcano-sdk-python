from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.function_runtime_option import FunctionRuntimeOption





T = TypeVar("T", bound="FunctionRuntimesResponse")



@_attrs_define
class FunctionRuntimesResponse:
    """ 
        Attributes:
            runtimes (list[FunctionRuntimeOption]):
     """

    runtimes: list[FunctionRuntimeOption]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.function_runtime_option import FunctionRuntimeOption
        runtimes = []
        for runtimes_item_data in self.runtimes:
            runtimes_item = runtimes_item_data.to_dict()
            runtimes.append(runtimes_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "runtimes": runtimes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.function_runtime_option import FunctionRuntimeOption
        d = dict(src_dict)
        runtimes = []
        _runtimes = d.pop("runtimes")
        for runtimes_item_data in (_runtimes):
            runtimes_item = FunctionRuntimeOption.from_dict(runtimes_item_data)



            runtimes.append(runtimes_item)


        function_runtimes_response = cls(
            runtimes=runtimes,
        )


        function_runtimes_response.additional_properties = d
        return function_runtimes_response

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
