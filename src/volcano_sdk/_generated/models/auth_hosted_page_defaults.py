from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AuthHostedPageDefaults")



@_attrs_define
class AuthHostedPageDefaults:
    """ The starting point for an unsaved page: the theme shell we render for the
    built-in page plus its stylesheet. Valid input to the update endpoint —
    it carries no script, meta, or link tags.

        Attributes:
            html (str): Body shell markup containing the runtime render root.
            css (str): The built-in stylesheet, themed by the customer.
     """

    html: str
    css: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        html = self.html

        css = self.css


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "html": html,
            "css": css,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        html = d.pop("html")

        css = d.pop("css")

        auth_hosted_page_defaults = cls(
            html=html,
            css=css,
        )


        auth_hosted_page_defaults.additional_properties = d
        return auth_hosted_page_defaults

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
