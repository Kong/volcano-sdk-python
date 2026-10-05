from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auth_page_density import AuthPageDensity
from ..models.auth_page_density import check_auth_page_density
from ..models.auth_page_font import AuthPageFont
from ..models.auth_page_font import check_auth_page_font
from ..models.auth_page_radius import AuthPageRadius
from ..models.auth_page_radius import check_auth_page_radius
from ..models.auth_page_scale import AuthPageScale
from ..models.auth_page_scale import check_auth_page_scale
from ..models.auth_page_theme_version import AuthPageThemeVersion
from ..models.auth_page_theme_version import check_auth_page_theme_version
from typing import cast

if TYPE_CHECKING:
  from ..models.auth_page_theme_colors import AuthPageThemeColors





T = TypeVar("T", bound="AuthPageTheme")



@_attrs_define
class AuthPageTheme:
    """ 
        Attributes:
            version (AuthPageThemeVersion):
            colors (AuthPageThemeColors):
            font (AuthPageFont):
            scale (AuthPageScale):
            density (AuthPageDensity):
            radius (AuthPageRadius):
     """

    version: AuthPageThemeVersion
    colors: AuthPageThemeColors
    font: AuthPageFont
    scale: AuthPageScale
    density: AuthPageDensity
    radius: AuthPageRadius





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_page_theme_colors import AuthPageThemeColors
        version: int = self.version

        colors = self.colors.to_dict()

        font: str = self.font

        scale: str = self.scale

        density: str = self.density

        radius: str = self.radius


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "version": version,
            "colors": colors,
            "font": font,
            "scale": scale,
            "density": density,
            "radius": radius,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_page_theme_colors import AuthPageThemeColors
        d = dict(src_dict)
        version = check_auth_page_theme_version(d.pop("version"))




        colors = AuthPageThemeColors.from_dict(d.pop("colors"))




        font = check_auth_page_font(d.pop("font"))




        scale = check_auth_page_scale(d.pop("scale"))




        density = check_auth_page_density(d.pop("density"))




        radius = check_auth_page_radius(d.pop("radius"))




        auth_page_theme = cls(
            version=version,
            colors=colors,
            font=font,
            scale=scale,
            density=density,
            radius=radius,
        )

        return auth_page_theme

