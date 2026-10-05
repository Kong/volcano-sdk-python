from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auth_page_layout import AuthPageLayout
from ..models.auth_page_layout import check_auth_page_layout
from typing import cast






T = TypeVar("T", bound="UpdateAuthPageLayoutRequest")



@_attrs_define
class UpdateAuthPageLayoutRequest:
    """ 
        Attributes:
            layout (AuthPageLayout):
     """

    layout: AuthPageLayout





    def to_dict(self) -> dict[str, Any]:
        layout: str = self.layout


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "layout": layout,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        layout = check_auth_page_layout(d.pop("layout"))




        update_auth_page_layout_request = cls(
            layout=layout,
        )

        return update_auth_page_layout_request

