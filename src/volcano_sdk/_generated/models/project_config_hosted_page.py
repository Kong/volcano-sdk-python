from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ProjectConfigHostedPage")



@_attrs_define
class ProjectConfigHostedPage:
    """ 
        Attributes:
            html (str): Raw HTML markup for the page. Max 256 KiB.
            css (str | Unset): Optional CSS injected at render time. Max 256 KiB.
     """

    html: str
    css: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        html = self.html

        css = self.css


        field_dict: dict[str, Any] = {}

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

        project_config_hosted_page = cls(
            html=html,
            css=css,
        )

        return project_config_hosted_page

