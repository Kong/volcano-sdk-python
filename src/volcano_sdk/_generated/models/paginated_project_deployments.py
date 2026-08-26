from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_deployment import ProjectDeployment





T = TypeVar("T", bound="PaginatedProjectDeployments")



@_attrs_define
class PaginatedProjectDeployments:
    """ 
        Attributes:
            data (list[ProjectDeployment]):
            limit (int): Number of items per page
            total (int): Total number of items across all pages
            has_more (bool): Whether there are more pages available
            page (int | Unset): Current page number (1-indexed). Offset pagination only — omitted in
                cursor mode, where position comes from the cursor and there is no page
                number to report. Required-and-1-indexed would otherwise force a `0`
                onto every cursor response.
            next_ (str | Unset): URL path to next page (offset pagination only; present if has_more is true)
            next_cursor (str | Unset): Opaque cursor for the next page (cursor pagination only; present if has_more is true)
            prev_cursor (str | Unset): Opaque cursor for the previous page (cursor pagination only; present when a previous
                page exists). Send as `ending_before`.
     """

    data: list[ProjectDeployment]
    limit: int
    total: int
    has_more: bool
    page: int | Unset = UNSET
    next_: str | Unset = UNSET
    next_cursor: str | Unset = UNSET
    prev_cursor: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_deployment import ProjectDeployment
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)



        limit = self.limit

        total = self.total

        has_more = self.has_more

        page = self.page

        next_ = self.next_

        next_cursor = self.next_cursor

        prev_cursor = self.prev_cursor


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "data": data,
            "limit": limit,
            "total": total,
            "has_more": has_more,
        })
        if page is not UNSET:
            field_dict["page"] = page
        if next_ is not UNSET:
            field_dict["next"] = next_
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor
        if prev_cursor is not UNSET:
            field_dict["prev_cursor"] = prev_cursor

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_deployment import ProjectDeployment
        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in (_data):
            data_item = ProjectDeployment.from_dict(data_item_data)



            data.append(data_item)


        limit = d.pop("limit")

        total = d.pop("total")

        has_more = d.pop("has_more")

        page = d.pop("page", UNSET)

        next_ = d.pop("next", UNSET)

        next_cursor = d.pop("next_cursor", UNSET)

        prev_cursor = d.pop("prev_cursor", UNSET)

        paginated_project_deployments = cls(
            data=data,
            limit=limit,
            total=total,
            has_more=has_more,
            page=page,
            next_=next_,
            next_cursor=next_cursor,
            prev_cursor=prev_cursor,
        )


        paginated_project_deployments.additional_properties = d
        return paginated_project_deployments

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
