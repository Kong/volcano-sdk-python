from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.auth_session import AuthSession





T = TypeVar("T", bound="ListUserSessionsResponse200")



@_attrs_define
class ListUserSessionsResponse200:
    """ 
        Attributes:
            sessions (list[AuthSession] | Unset):
            total (int | Unset): Total number of sessions
            page (int | Unset): Current page number
            limit (int | Unset): Number of sessions per page
            total_pages (int | Unset): Total number of pages
            data (list[AuthSession] | Unset): Sessions for this page (cursor pagination only)
            has_more (bool | Unset): Whether a further page exists (cursor pagination only)
            next_cursor (str | Unset): Opaque cursor for the next page (cursor pagination only)
            prev_cursor (str | Unset): Opaque cursor for the previous page (cursor pagination only). Send as
                `ending_before`.
     """

    sessions: list[AuthSession] | Unset = UNSET
    total: int | Unset = UNSET
    page: int | Unset = UNSET
    limit: int | Unset = UNSET
    total_pages: int | Unset = UNSET
    data: list[AuthSession] | Unset = UNSET
    has_more: bool | Unset = UNSET
    next_cursor: str | Unset = UNSET
    prev_cursor: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_session import AuthSession
        sessions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.sessions, Unset):
            sessions = []
            for sessions_item_data in self.sessions:
                sessions_item = sessions_item_data.to_dict()
                sessions.append(sessions_item)



        total = self.total

        page = self.page

        limit = self.limit

        total_pages = self.total_pages

        data: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)



        has_more = self.has_more

        next_cursor = self.next_cursor

        prev_cursor = self.prev_cursor


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if sessions is not UNSET:
            field_dict["sessions"] = sessions
        if total is not UNSET:
            field_dict["total"] = total
        if page is not UNSET:
            field_dict["page"] = page
        if limit is not UNSET:
            field_dict["limit"] = limit
        if total_pages is not UNSET:
            field_dict["total_pages"] = total_pages
        if data is not UNSET:
            field_dict["data"] = data
        if has_more is not UNSET:
            field_dict["has_more"] = has_more
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor
        if prev_cursor is not UNSET:
            field_dict["prev_cursor"] = prev_cursor

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_session import AuthSession
        d = dict(src_dict)
        _sessions = d.pop("sessions", UNSET)
        sessions: list[AuthSession] | Unset = UNSET
        if _sessions is not UNSET:
            sessions = []
            for sessions_item_data in _sessions:
                sessions_item = AuthSession.from_dict(sessions_item_data)



                sessions.append(sessions_item)


        total = d.pop("total", UNSET)

        page = d.pop("page", UNSET)

        limit = d.pop("limit", UNSET)

        total_pages = d.pop("total_pages", UNSET)

        _data = d.pop("data", UNSET)
        data: list[AuthSession] | Unset = UNSET
        if _data is not UNSET:
            data = []
            for data_item_data in _data:
                data_item = AuthSession.from_dict(data_item_data)



                data.append(data_item)


        has_more = d.pop("has_more", UNSET)

        next_cursor = d.pop("next_cursor", UNSET)

        prev_cursor = d.pop("prev_cursor", UNSET)

        list_user_sessions_response_200 = cls(
            sessions=sessions,
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
            data=data,
            has_more=has_more,
            next_cursor=next_cursor,
            prev_cursor=prev_cursor,
        )


        list_user_sessions_response_200.additional_properties = d
        return list_user_sessions_response_200

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
