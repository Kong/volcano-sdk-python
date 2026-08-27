from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.hosted_auth_page_type import check_hosted_auth_page_type
from ..models.hosted_auth_page_type import HostedAuthPageType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="AuthHostedPage")



@_attrs_define
class AuthHostedPage:
    """ 
        Attributes:
            id (UUID | Unset):
            project_id (UUID | Unset):
            page_type (HostedAuthPageType | Unset):
            html (str | Unset): HTML content for this page type.
            css (str | Unset): CSS content for this page type.
            created_at (datetime.datetime | Unset):
            updated_at (datetime.datetime | Unset):
     """

    id: UUID | Unset = UNSET
    project_id: UUID | Unset = UNSET
    page_type: HostedAuthPageType | Unset = UNSET
    html: str | Unset = UNSET
    css: str | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id: str | Unset = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        project_id: str | Unset = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        page_type: str | Unset = UNSET
        if not isinstance(self.page_type, Unset):
            page_type = self.page_type


        html = self.html

        css = self.css

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if page_type is not UNSET:
            field_dict["page_type"] = page_type
        if html is not UNSET:
            field_dict["html"] = html
        if css is not UNSET:
            field_dict["css"] = css
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _id = d.pop("id", UNSET)
        id: UUID | Unset
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        _project_id = d.pop("project_id", UNSET)
        project_id: UUID | Unset
        if isinstance(_project_id,  Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)




        _page_type = d.pop("page_type", UNSET)
        page_type: HostedAuthPageType | Unset
        if isinstance(_page_type,  Unset):
            page_type = UNSET
        else:
            page_type = check_hosted_auth_page_type(_page_type)




        html = d.pop("html", UNSET)

        css = d.pop("css", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)




        _updated_at = d.pop("updated_at", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at,  Unset):
            updated_at = UNSET
        else:
            updated_at = datetime.datetime.fromisoformat(_updated_at)




        auth_hosted_page = cls(
            id=id,
            project_id=project_id,
            page_type=page_type,
            html=html,
            css=css,
            created_at=created_at,
            updated_at=updated_at,
        )


        auth_hosted_page.additional_properties = d
        return auth_hosted_page

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
