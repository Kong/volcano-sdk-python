from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.import_connection import ImportConnection





T = TypeVar("T", bound="ImportConnectionsResponse")



@_attrs_define
class ImportConnectionsResponse:
    """ 
        Attributes:
            connections (list[ImportConnection]):
     """

    connections: list[ImportConnection]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.import_connection import ImportConnection
        connections = []
        for connections_item_data in self.connections:
            connections_item = connections_item_data.to_dict()
            connections.append(connections_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "connections": connections,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.import_connection import ImportConnection
        d = dict(src_dict)
        connections = []
        _connections = d.pop("connections")
        for connections_item_data in (_connections):
            connections_item = ImportConnection.from_dict(connections_item_data)



            connections.append(connections_item)


        import_connections_response = cls(
            connections=connections,
        )


        import_connections_response.additional_properties = d
        return import_connections_response

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
