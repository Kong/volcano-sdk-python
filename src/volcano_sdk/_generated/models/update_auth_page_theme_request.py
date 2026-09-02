from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.auth_page_theme import AuthPageTheme





T = TypeVar("T", bound="UpdateAuthPageThemeRequest")



@_attrs_define
class UpdateAuthPageThemeRequest:
    """ 
        Attributes:
            theme (AuthPageTheme):
     """

    theme: AuthPageTheme





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_page_theme import AuthPageTheme
        theme = self.theme.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "theme": theme,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_page_theme import AuthPageTheme
        d = dict(src_dict)
        theme = AuthPageTheme.from_dict(d.pop("theme"))




        update_auth_page_theme_request = cls(
            theme=theme,
        )

        return update_auth_page_theme_request

