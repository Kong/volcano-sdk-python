from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateEmailTemplateRequest")



@_attrs_define
class UpdateEmailTemplateRequest:
    """ 
        Attributes:
            subject (str | Unset):
            html_body (str | Unset):
            text_body (str | Unset):
     """

    subject: str | Unset = UNSET
    html_body: str | Unset = UNSET
    text_body: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        subject = self.subject

        html_body = self.html_body

        text_body = self.text_body


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if subject is not UNSET:
            field_dict["subject"] = subject
        if html_body is not UNSET:
            field_dict["html_body"] = html_body
        if text_body is not UNSET:
            field_dict["text_body"] = text_body

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        subject = d.pop("subject", UNSET)

        html_body = d.pop("html_body", UNSET)

        text_body = d.pop("text_body", UNSET)

        update_email_template_request = cls(
            subject=subject,
            html_body=html_body,
            text_body=text_body,
        )


        update_email_template_request.additional_properties = d
        return update_email_template_request

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
