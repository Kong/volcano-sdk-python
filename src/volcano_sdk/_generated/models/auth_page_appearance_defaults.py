from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auth_page_layout import AuthPageLayout
from ..models.auth_page_layout import check_auth_page_layout
from typing import cast

if TYPE_CHECKING:
  from ..models.auth_page_theme import AuthPageTheme





T = TypeVar("T", bound="AuthPageAppearanceDefaults")



@_attrs_define
class AuthPageAppearanceDefaults:
    """ 
        Attributes:
            theme (AuthPageTheme):
            layout (AuthPageLayout):
     """

    theme: AuthPageTheme
    layout: AuthPageLayout
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_page_theme import AuthPageTheme
        theme = self.theme.to_dict()

        layout: str = self.layout


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "theme": theme,
            "layout": layout,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_page_theme import AuthPageTheme
        d = dict(src_dict)
        theme = AuthPageTheme.from_dict(d.pop("theme"))




        layout = check_auth_page_layout(d.pop("layout"))




        auth_page_appearance_defaults = cls(
            theme=theme,
            layout=layout,
        )


        auth_page_appearance_defaults.additional_properties = d
        return auth_page_appearance_defaults

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
