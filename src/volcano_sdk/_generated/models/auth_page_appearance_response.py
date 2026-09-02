from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.auth_page_appearance_defaults import AuthPageAppearanceDefaults
  from ..models.auth_page_appearance_options import AuthPageAppearanceOptions
  from ..models.auth_page_appearance_response_layouts import AuthPageAppearanceResponseLayouts
  from ..models.auth_page_appearance_response_parked import AuthPageAppearanceResponseParked
  from ..models.auth_page_theme import AuthPageTheme





T = TypeVar("T", bound="AuthPageAppearanceResponse")



@_attrs_define
class AuthPageAppearanceResponse:
    """ 
        Attributes:
            theme (AuthPageTheme):
            layouts (AuthPageAppearanceResponseLayouts):
            customisation_allowed (bool):
            parked (AuthPageAppearanceResponseParked): Per-page saved-but-not-live state.
            defaults (AuthPageAppearanceDefaults):
            options (AuthPageAppearanceOptions):
     """

    theme: AuthPageTheme
    layouts: AuthPageAppearanceResponseLayouts
    customisation_allowed: bool
    parked: AuthPageAppearanceResponseParked
    defaults: AuthPageAppearanceDefaults
    options: AuthPageAppearanceOptions
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_page_appearance_defaults import AuthPageAppearanceDefaults
        from ..models.auth_page_appearance_options import AuthPageAppearanceOptions
        from ..models.auth_page_appearance_response_layouts import AuthPageAppearanceResponseLayouts
        from ..models.auth_page_appearance_response_parked import AuthPageAppearanceResponseParked
        from ..models.auth_page_theme import AuthPageTheme
        theme = self.theme.to_dict()

        layouts = self.layouts.to_dict()

        customisation_allowed = self.customisation_allowed

        parked = self.parked.to_dict()

        defaults = self.defaults.to_dict()

        options = self.options.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "theme": theme,
            "layouts": layouts,
            "customisation_allowed": customisation_allowed,
            "parked": parked,
            "defaults": defaults,
            "options": options,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_page_appearance_defaults import AuthPageAppearanceDefaults
        from ..models.auth_page_appearance_options import AuthPageAppearanceOptions
        from ..models.auth_page_appearance_response_layouts import AuthPageAppearanceResponseLayouts
        from ..models.auth_page_appearance_response_parked import AuthPageAppearanceResponseParked
        from ..models.auth_page_theme import AuthPageTheme
        d = dict(src_dict)
        theme = AuthPageTheme.from_dict(d.pop("theme"))




        layouts = AuthPageAppearanceResponseLayouts.from_dict(d.pop("layouts"))




        customisation_allowed = d.pop("customisation_allowed")

        parked = AuthPageAppearanceResponseParked.from_dict(d.pop("parked"))




        defaults = AuthPageAppearanceDefaults.from_dict(d.pop("defaults"))




        options = AuthPageAppearanceOptions.from_dict(d.pop("options"))




        auth_page_appearance_response = cls(
            theme=theme,
            layouts=layouts,
            customisation_allowed=customisation_allowed,
            parked=parked,
            defaults=defaults,
            options=options,
        )


        auth_page_appearance_response.additional_properties = d
        return auth_page_appearance_response

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
