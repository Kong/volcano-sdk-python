from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ProjectConfigEmailTemplate")



@_attrs_define
class ProjectConfigEmailTemplate:
    """ 
        Attributes:
            subject (str | Unset):
            html_body (str | Unset): HTML body. Max 256 KiB. PRO plan required for custom bodies.
            text_body (str | Unset): Plain-text body. Max 256 KiB. PRO plan required for custom bodies.
     """

    subject: str | Unset = UNSET
    html_body: str | Unset = UNSET
    text_body: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        subject = self.subject

        html_body = self.html_body

        text_body = self.text_body


        field_dict: dict[str, Any] = {}

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

        project_config_email_template = cls(
            subject=subject,
            html_body=html_body,
            text_body=text_body,
        )

        return project_config_email_template

