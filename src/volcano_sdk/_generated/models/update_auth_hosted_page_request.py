from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateAuthHostedPageRequest")



@_attrs_define
class UpdateAuthHostedPageRequest:
    """ 
        Attributes:
            html (str): Raw HTML markup for the page. Max 256 KiB.
            css (str | Unset): Optional CSS injected at render time. Max 256 KiB.
     """

    html: str
    css: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        html = self.html

        css = self.css


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "html": html,
        })
        if css is not UNSET:
            field_dict["css"] = css

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        html = d.pop("html")

        css = d.pop("css", UNSET)

        update_auth_hosted_page_request = cls(
            html=html,
            css=css,
        )


        update_auth_hosted_page_request.additional_properties = d
        return update_auth_hosted_page_request

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
