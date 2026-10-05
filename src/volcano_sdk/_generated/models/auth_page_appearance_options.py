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
from ..models.auth_page_layout import AuthPageLayout
from ..models.auth_page_layout import check_auth_page_layout
from ..models.auth_page_radius import AuthPageRadius
from ..models.auth_page_radius import check_auth_page_radius
from ..models.auth_page_scale import AuthPageScale
from ..models.auth_page_scale import check_auth_page_scale
from ..models.hosted_auth_page_type import check_hosted_auth_page_type
from ..models.hosted_auth_page_type import HostedAuthPageType
from typing import cast






T = TypeVar("T", bound="AuthPageAppearanceOptions")



@_attrs_define
class AuthPageAppearanceOptions:
    """ 
        Attributes:
            pages (list[HostedAuthPageType]):
            fonts (list[AuthPageFont]):
            scales (list[AuthPageScale]):
            densities (list[AuthPageDensity]):
            radii (list[AuthPageRadius]):
            layouts (list[AuthPageLayout]):
     """

    pages: list[HostedAuthPageType]
    fonts: list[AuthPageFont]
    scales: list[AuthPageScale]
    densities: list[AuthPageDensity]
    radii: list[AuthPageRadius]
    layouts: list[AuthPageLayout]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        pages = []
        for pages_item_data in self.pages:
            pages_item: str = pages_item_data
            pages.append(pages_item)



        fonts = []
        for fonts_item_data in self.fonts:
            fonts_item: str = fonts_item_data
            fonts.append(fonts_item)



        scales = []
        for scales_item_data in self.scales:
            scales_item: str = scales_item_data
            scales.append(scales_item)



        densities = []
        for densities_item_data in self.densities:
            densities_item: str = densities_item_data
            densities.append(densities_item)



        radii = []
        for radii_item_data in self.radii:
            radii_item: str = radii_item_data
            radii.append(radii_item)



        layouts = []
        for layouts_item_data in self.layouts:
            layouts_item: str = layouts_item_data
            layouts.append(layouts_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "pages": pages,
            "fonts": fonts,
            "scales": scales,
            "densities": densities,
            "radii": radii,
            "layouts": layouts,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pages = []
        _pages = d.pop("pages")
        for pages_item_data in (_pages):
            pages_item = check_hosted_auth_page_type(pages_item_data)



            pages.append(pages_item)


        fonts = []
        _fonts = d.pop("fonts")
        for fonts_item_data in (_fonts):
            fonts_item = check_auth_page_font(fonts_item_data)



            fonts.append(fonts_item)


        scales = []
        _scales = d.pop("scales")
        for scales_item_data in (_scales):
            scales_item = check_auth_page_scale(scales_item_data)



            scales.append(scales_item)


        densities = []
        _densities = d.pop("densities")
        for densities_item_data in (_densities):
            densities_item = check_auth_page_density(densities_item_data)



            densities.append(densities_item)


        radii = []
        _radii = d.pop("radii")
        for radii_item_data in (_radii):
            radii_item = check_auth_page_radius(radii_item_data)



            radii.append(radii_item)


        layouts = []
        _layouts = d.pop("layouts")
        for layouts_item_data in (_layouts):
            layouts_item = check_auth_page_layout(layouts_item_data)



            layouts.append(layouts_item)


        auth_page_appearance_options = cls(
            pages=pages,
            fonts=fonts,
            scales=scales,
            densities=densities,
            radii=radii,
            layouts=layouts,
        )


        auth_page_appearance_options.additional_properties = d
        return auth_page_appearance_options

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
