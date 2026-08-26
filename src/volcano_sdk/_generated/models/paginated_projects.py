from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.paginated_projects_status import check_paginated_projects_status
from ..models.paginated_projects_status import PaginatedProjectsStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.project import Project





T = TypeVar("T", bound="PaginatedProjects")



@_attrs_define
class PaginatedProjects:
    """ 
        Attributes:
            data (list[Project]):
            page (int): Current page number (1-indexed)
            limit (int): Number of items per page
            total (int): Total number of items across all pages
            has_more (bool): Whether there are more pages available
            next_ (str | Unset): URL path to next page (offset pagination only; present if has_more is true)
            next_cursor (str | Unset): Opaque cursor for the next page (cursor pagination only; present if has_more is true)
            prev_cursor (str | Unset): Opaque cursor for the previous page (cursor pagination only; present when a previous
                page exists). Send as `ending_before`.
            status (PaginatedProjectsStatus | Unset): Latest project variable propagation status.
            current_sync_id (UUID | Unset): Identifier of the latest variable propagation sync.
            provisioning_started_at (datetime.datetime | Unset): Timestamp when the current variable propagation phase
                started.
     """

    data: list[Project]
    page: int
    limit: int
    total: int
    has_more: bool
    next_: str | Unset = UNSET
    next_cursor: str | Unset = UNSET
    prev_cursor: str | Unset = UNSET
    status: PaginatedProjectsStatus | Unset = UNSET
    current_sync_id: UUID | Unset = UNSET
    provisioning_started_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.project import Project
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)



        page = self.page

        limit = self.limit

        total = self.total

        has_more = self.has_more

        next_ = self.next_

        next_cursor = self.next_cursor

        prev_cursor = self.prev_cursor

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status


        current_sync_id: str | Unset = UNSET
        if not isinstance(self.current_sync_id, Unset):
            current_sync_id = str(self.current_sync_id)

        provisioning_started_at: str | Unset = UNSET
        if not isinstance(self.provisioning_started_at, Unset):
            provisioning_started_at = self.provisioning_started_at.isoformat()


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
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor
        if prev_cursor is not UNSET:
            field_dict["prev_cursor"] = prev_cursor
        if status is not UNSET:
            field_dict["status"] = status
        if current_sync_id is not UNSET:
            field_dict["current_sync_id"] = current_sync_id
        if provisioning_started_at is not UNSET:
            field_dict["provisioning_started_at"] = provisioning_started_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project import Project
        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in (_data):
            data_item = Project.from_dict(data_item_data)



            data.append(data_item)


        page = d.pop("page")

        limit = d.pop("limit")

        total = d.pop("total")

        has_more = d.pop("has_more")

        next_ = d.pop("next", UNSET)

        next_cursor = d.pop("next_cursor", UNSET)

        prev_cursor = d.pop("prev_cursor", UNSET)

        _status = d.pop("status", UNSET)
        status: PaginatedProjectsStatus | Unset
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = check_paginated_projects_status(_status)




        _current_sync_id = d.pop("current_sync_id", UNSET)
        current_sync_id: UUID | Unset
        if isinstance(_current_sync_id,  Unset):
            current_sync_id = UNSET
        else:
            current_sync_id = UUID(_current_sync_id)




        _provisioning_started_at = d.pop("provisioning_started_at", UNSET)
        provisioning_started_at: datetime.datetime | Unset
        if isinstance(_provisioning_started_at,  Unset):
            provisioning_started_at = UNSET
        else:
            provisioning_started_at = datetime.datetime.fromisoformat(_provisioning_started_at)




        paginated_projects = cls(
            data=data,
            page=page,
            limit=limit,
            total=total,
            has_more=has_more,
            next_=next_,
            next_cursor=next_cursor,
            prev_cursor=prev_cursor,
            status=status,
            current_sync_id=current_sync_id,
            provisioning_started_at=provisioning_started_at,
        )


        paginated_projects.additional_properties = d
        return paginated_projects

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
