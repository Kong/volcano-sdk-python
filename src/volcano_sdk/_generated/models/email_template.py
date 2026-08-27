from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.email_template_template_type import check_email_template_template_type
from ..models.email_template_template_type import EmailTemplateTemplateType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="EmailTemplate")



@_attrs_define
class EmailTemplate:
    """ Custom email template

        Attributes:
            template_type (EmailTemplateTemplateType):
            subject (str):  Example: Confirm your email address.
            html_body (str): HTML template with placeholders
            text_body (str): Plain text template with placeholders
            id (UUID | Unset):
            project_id (UUID | Unset):
            created_at (datetime.datetime | Unset):
            updated_at (datetime.datetime | Unset):
     """

    template_type: EmailTemplateTemplateType
    subject: str
    html_body: str
    text_body: str
    id: UUID | Unset = UNSET
    project_id: UUID | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        template_type: str = self.template_type

        subject = self.subject

        html_body = self.html_body

        text_body = self.text_body

        id: str | Unset = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        project_id: str | Unset = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "template_type": template_type,
            "subject": subject,
            "html_body": html_body,
            "text_body": text_body,
        })
        if id is not UNSET:
            field_dict["id"] = id
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        template_type = check_email_template_template_type(d.pop("template_type"))




        subject = d.pop("subject")

        html_body = d.pop("html_body")

        text_body = d.pop("text_body")

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




        email_template = cls(
            template_type=template_type,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
            id=id,
            project_id=project_id,
            created_at=created_at,
            updated_at=updated_at,
        )


        email_template.additional_properties = d
        return email_template

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
