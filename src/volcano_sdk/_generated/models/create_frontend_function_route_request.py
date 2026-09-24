from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="CreateFrontendFunctionRouteRequest")



@_attrs_define
class CreateFrontendFunctionRouteRequest:
    """ 
        Attributes:
            function_id (UUID):
            path_prefix (str):
            strip_prefix (bool | Unset):  Default: False.
     """

    function_id: UUID
    path_prefix: str
    strip_prefix: bool | Unset = False





    def to_dict(self) -> dict[str, Any]:
        function_id = str(self.function_id)

        path_prefix = self.path_prefix

        strip_prefix = self.strip_prefix


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "function_id": function_id,
            "path_prefix": path_prefix,
        })
        if strip_prefix is not UNSET:
            field_dict["strip_prefix"] = strip_prefix

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        function_id = UUID(d.pop("function_id"))




        path_prefix = d.pop("path_prefix")

        strip_prefix = d.pop("strip_prefix", UNSET)

        create_frontend_function_route_request = cls(
            function_id=function_id,
            path_prefix=path_prefix,
            strip_prefix=strip_prefix,
        )

        return create_frontend_function_route_request

