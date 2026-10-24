from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.default_email_template_type import check_default_email_template_type
from ..models.default_email_template_type import DefaultEmailTemplateType
from typing import cast






T = TypeVar("T", bound="DefaultEmailTemplate")



@_attrs_define
class DefaultEmailTemplate:
    """ Built-in email template used when no custom template applies.

        Attributes:
            type_ (DefaultEmailTemplateType):
            subject (str):
            html_body (str): HTML template with placeholders
            text_body (str): Plain text template with placeholders
     """

    type_: DefaultEmailTemplateType
    subject: str
    html_body: str
    text_body: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        subject = self.subject

        html_body = self.html_body

        text_body = self.text_body


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "subject": subject,
            "html_body": html_body,
            "text_body": text_body,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_default_email_template_type(d.pop("type"))




        subject = d.pop("subject")

        html_body = d.pop("html_body")

        text_body = d.pop("text_body")

        default_email_template = cls(
            type_=type_,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
        )


        default_email_template.additional_properties = d
        return default_email_template

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
