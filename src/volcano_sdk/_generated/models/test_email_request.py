from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="TestEmailRequest")



@_attrs_define
class TestEmailRequest:
    """ When `html_body` or `text_body` is provided the backend renders
    those (plus optional `subject`) through html/text templates
    against the standard `Data` (ProjectName, Name, SiteURL)
    and sends the result — used by the template-editor "Send Test"
    affordance to preview an unsaved template. When both bodies are
    omitted a hardcoded diagnostic message is sent to verify SMTP
    credentials and `subject` is ignored. Sending `subject` alone
    (without a body) is rejected with 400.

        Attributes:
            to_email (str): Recipient address for the diagnostic email.
            subject (str | Unset): Optional subject override, rendered as a text/template. Only
                applied on the override path — requires `html_body` or
                `text_body` to also be set, otherwise the request is
                rejected with 400.
            html_body (str | Unset): Optional HTML body override. Rendered as an html/template. Max 256 KiB.
            text_body (str | Unset): Optional plain-text body override. Rendered as a text/template. Max 256 KiB.
     """

    to_email: str
    subject: str | Unset = UNSET
    html_body: str | Unset = UNSET
    text_body: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        to_email = self.to_email

        subject = self.subject

        html_body = self.html_body

        text_body = self.text_body


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "to_email": to_email,
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
        to_email = d.pop("to_email")

        subject = d.pop("subject", UNSET)

        html_body = d.pop("html_body", UNSET)

        text_body = d.pop("text_body", UNSET)

        test_email_request = cls(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
        )


        test_email_request.additional_properties = d
        return test_email_request

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
