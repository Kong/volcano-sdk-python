from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_email_template_request_template_type import check_create_email_template_request_template_type
from ..models.create_email_template_request_template_type import CreateEmailTemplateRequestTemplateType
from typing import cast






T = TypeVar("T", bound="CreateEmailTemplateRequest")



@_attrs_define
class CreateEmailTemplateRequest:
    """ 
        Attributes:
            template_type (CreateEmailTemplateRequestTemplateType): Type of email template
            subject (str): Email subject line Example: Confirm your email.
            html_body (str): HTML template body. Available placeholders:
                - {{.Token}} - The confirmation/reset token
                - {{.ProjectName}} - The project name
                - {{.Email}} - User's email address
            text_body (str): Plain text template body (same placeholders as HTML)
     """

    template_type: CreateEmailTemplateRequestTemplateType
    subject: str
    html_body: str
    text_body: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        template_type: str = self.template_type

        subject = self.subject

        html_body = self.html_body

        text_body = self.text_body


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "template_type": template_type,
            "subject": subject,
            "html_body": html_body,
            "text_body": text_body,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        template_type = check_create_email_template_request_template_type(d.pop("template_type"))




        subject = d.pop("subject")

        html_body = d.pop("html_body")

        text_body = d.pop("text_body")

        create_email_template_request = cls(
            template_type=template_type,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
        )


        create_email_template_request.additional_properties = d
        return create_email_template_request

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
