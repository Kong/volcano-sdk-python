from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.auth_page_theme import AuthPageTheme
  from ..models.project_config_auth_page_layouts import ProjectConfigAuthPageLayouts





T = TypeVar("T", bound="ProjectConfigAuthPageAppearance")



@_attrs_define
class ProjectConfigAuthPageAppearance:
    """ 
        Attributes:
            theme (AuthPageTheme | Unset):
            layouts (ProjectConfigAuthPageLayouts | Unset):
     """

    theme: AuthPageTheme | Unset = UNSET
    layouts: ProjectConfigAuthPageLayouts | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_page_theme import AuthPageTheme
        from ..models.project_config_auth_page_layouts import ProjectConfigAuthPageLayouts
        theme: dict[str, Any] | Unset = UNSET
        if not isinstance(self.theme, Unset):
            theme = self.theme.to_dict()

        layouts: dict[str, Any] | Unset = UNSET
        if not isinstance(self.layouts, Unset):
            layouts = self.layouts.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if theme is not UNSET:
            field_dict["theme"] = theme
        if layouts is not UNSET:
            field_dict["layouts"] = layouts

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_page_theme import AuthPageTheme
        from ..models.project_config_auth_page_layouts import ProjectConfigAuthPageLayouts
        d = dict(src_dict)
        _theme = d.pop("theme", UNSET)
        theme: AuthPageTheme | Unset
        if isinstance(_theme,  Unset):
            theme = UNSET
        else:
            theme = AuthPageTheme.from_dict(_theme)




        _layouts = d.pop("layouts", UNSET)
        layouts: ProjectConfigAuthPageLayouts | Unset
        if isinstance(_layouts,  Unset):
            layouts = UNSET
        else:
            layouts = ProjectConfigAuthPageLayouts.from_dict(_layouts)




        project_config_auth_page_appearance = cls(
            theme=theme,
            layouts=layouts,
        )

        return project_config_auth_page_appearance

