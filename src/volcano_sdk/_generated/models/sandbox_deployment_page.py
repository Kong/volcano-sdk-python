from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.sandbox_deployment import SandboxDeployment
  from ..models.sandbox_pagination import SandboxPagination





T = TypeVar("T", bound="SandboxDeploymentPage")



@_attrs_define
class SandboxDeploymentPage:
    """ 
        Attributes:
            data (list[SandboxDeployment]):
            pagination (SandboxPagination):
     """

    data: list[SandboxDeployment]
    pagination: SandboxPagination





    def to_dict(self) -> dict[str, Any]:
        from ..models.sandbox_deployment import SandboxDeployment
        from ..models.sandbox_pagination import SandboxPagination
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)



        pagination = self.pagination.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "data": data,
            "pagination": pagination,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_deployment import SandboxDeployment
        from ..models.sandbox_pagination import SandboxPagination
        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in (_data):
            data_item = SandboxDeployment.from_dict(data_item_data)



            data.append(data_item)


        pagination = SandboxPagination.from_dict(d.pop("pagination"))




        sandbox_deployment_page = cls(
            data=data,
            pagination=pagination,
        )

        return sandbox_deployment_page

