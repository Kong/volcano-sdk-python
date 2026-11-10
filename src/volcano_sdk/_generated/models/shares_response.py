from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.share import Share





T = TypeVar("T", bound="SharesResponse")



@_attrs_define
class SharesResponse:
    """ 
        Attributes:
            shares (list[Share]):
     """

    shares: list[Share]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.share import Share # noqa: PLC0415
        shares = []
        for shares_item_data in self.shares:
            shares_item = shares_item_data.to_dict()
            shares.append(shares_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "shares": shares,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.share import Share # noqa: PLC0415
        d = dict(src_dict)
        shares = []
        _shares = d.pop("shares")
        for shares_item_data in (_shares):
            shares_item = Share.from_dict(shares_item_data)



            shares.append(shares_item)


        shares_response = cls(
            shares=shares,
        )


        shares_response.additional_properties = d
        return shares_response

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
