from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AuthPageThemeColors")



@_attrs_define
class AuthPageThemeColors:
    """ 
        Attributes:
            background (str):
            surface (str):
            text (str):
            accent (str):
            accent_text (str):
     """

    background: str
    surface: str
    text: str
    accent: str
    accent_text: str





    def to_dict(self) -> dict[str, Any]:
        background = self.background

        surface = self.surface

        text = self.text

        accent = self.accent

        accent_text = self.accent_text


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "background": background,
            "surface": surface,
            "text": text,
            "accent": accent,
            "accent_text": accent_text,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        background = d.pop("background")

        surface = d.pop("surface")

        text = d.pop("text")

        accent = d.pop("accent")

        accent_text = d.pop("accent_text")

        auth_page_theme_colors = cls(
            background=background,
            surface=surface,
            text=text,
            accent=accent,
            accent_text=accent_text,
        )

        return auth_page_theme_colors

