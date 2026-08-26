from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_frontend_custom_domain import ProjectFrontendCustomDomain





T = TypeVar("T", bound="PaginatedProjectCustomDomains")



@_attrs_define
class PaginatedProjectCustomDomains:
    """ 
        Attributes:
            data (list[ProjectFrontendCustomDomain]):
            page (int): Current page number (1-indexed)
            limit (int): Number of items per page
            total (int): Total number of items across all pages
            has_more (bool): Whether there are more pages available
            next_ (str | Unset): URL path to next page (only present if has_more is true)
     """

    data: list[ProjectFrontendCustomDomain]
    page: int
    limit: int
    total: int
    has_more: bool
    next_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_frontend_custom_domain import ProjectFrontendCustomDomain
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)



        page = self.page

        limit = self.limit

        total = self.total

        has_more = self.has_more

        next_ = self.next_


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "data": data,
            "page": page,
            "limit": limit,
            "total": total,
            "has_more": has_more,
        })
        if next_ is not UNSET:
            field_dict["next"] = next_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_frontend_custom_domain import ProjectFrontendCustomDomain
        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in (_data):
            data_item = ProjectFrontendCustomDomain.from_dict(data_item_data)



            data.append(data_item)


        page = d.pop("page")

        limit = d.pop("limit")

        total = d.pop("total")

        has_more = d.pop("has_more")

        next_ = d.pop("next", UNSET)

        paginated_project_custom_domains = cls(
            data=data,
            page=page,
            limit=limit,
            total=total,
            has_more=has_more,
            next_=next_,
        )


        paginated_project_custom_domains.additional_properties = d
        return paginated_project_custom_domains

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
