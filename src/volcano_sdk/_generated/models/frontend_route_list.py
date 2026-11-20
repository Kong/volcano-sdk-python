from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.frontend_route import FrontendRoute





T = TypeVar("T", bound="FrontendRouteList")



@_attrs_define
class FrontendRouteList:
    """ 
        Attributes:
            data (list[FrontendRoute]):
     """

    data: list[FrontendRoute]





    def to_dict(self) -> dict[str, Any]:
        from ..models.frontend_route import FrontendRoute # noqa: PLC0415
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "data": data,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.frontend_route import FrontendRoute # noqa: PLC0415
        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in (_data):
            data_item = FrontendRoute.from_dict(data_item_data)



            data.append(data_item)


        frontend_route_list = cls(
            data=data,
        )

        return frontend_route_list

