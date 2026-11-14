from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.lavaflow_connector_binding import LavaflowConnectorBinding





T = TypeVar("T", bound="LavaflowConnectorBindingsResponse")



@_attrs_define
class LavaflowConnectorBindingsResponse:
    """ 
        Attributes:
            bindings (list[LavaflowConnectorBinding]):
     """

    bindings: list[LavaflowConnectorBinding]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_connector_binding import LavaflowConnectorBinding # noqa: PLC0415
        bindings = []
        for bindings_item_data in self.bindings:
            bindings_item = bindings_item_data.to_dict()
            bindings.append(bindings_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "bindings": bindings,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_connector_binding import LavaflowConnectorBinding # noqa: PLC0415
        d = dict(src_dict)
        bindings = []
        _bindings = d.pop("bindings")
        for bindings_item_data in (_bindings):
            bindings_item = LavaflowConnectorBinding.from_dict(bindings_item_data)



            bindings.append(bindings_item)


        lavaflow_connector_bindings_response = cls(
            bindings=bindings,
        )


        lavaflow_connector_bindings_response.additional_properties = d
        return lavaflow_connector_bindings_response

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
