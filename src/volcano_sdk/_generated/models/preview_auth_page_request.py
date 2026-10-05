from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auth_page_layout import AuthPageLayout
from ..models.auth_page_layout import check_auth_page_layout
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.auth_page_theme import AuthPageTheme





T = TypeVar("T", bound="PreviewAuthPageRequest")



@_attrs_define
class PreviewAuthPageRequest:
    """ 
        Attributes:
            theme (AuthPageTheme):
            layout (AuthPageLayout):
            action (str | Unset):
     """

    theme: AuthPageTheme
    layout: AuthPageLayout
    action: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_page_theme import AuthPageTheme
        theme = self.theme.to_dict()

        layout: str = self.layout

        action = self.action


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "theme": theme,
            "layout": layout,
        })
        if action is not UNSET:
            field_dict["action"] = action

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_page_theme import AuthPageTheme
        d = dict(src_dict)
        theme = AuthPageTheme.from_dict(d.pop("theme"))




        layout = check_auth_page_layout(d.pop("layout"))




        action = d.pop("action", UNSET)

        preview_auth_page_request = cls(
            theme=theme,
            layout=layout,
            action=action,
        )

        return preview_auth_page_request

