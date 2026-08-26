from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.import_source import ImportSource





T = TypeVar("T", bound="ImportSourcesResponse")



@_attrs_define
class ImportSourcesResponse:
    """ 
        Attributes:
            sources (list[ImportSource]):
     """

    sources: list[ImportSource]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.import_source import ImportSource
        sources = []
        for sources_item_data in self.sources:
            sources_item = sources_item_data.to_dict()
            sources.append(sources_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "sources": sources,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.import_source import ImportSource
        d = dict(src_dict)
        sources = []
        _sources = d.pop("sources")
        for sources_item_data in (_sources):
            sources_item = ImportSource.from_dict(sources_item_data)



            sources.append(sources_item)


        import_sources_response = cls(
            sources=sources,
        )


        import_sources_response.additional_properties = d
        return import_sources_response

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
