from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ProjectConfigFrontendFunctionRoute")



@_attrs_define
class ProjectConfigFrontendFunctionRoute:
    """ 
        Attributes:
            function (str): Name of an existing standard Function configured for HTTP invocation.
            path_prefix (str):
            strip_prefix (bool | Unset):  Default: False.
     """

    function: str
    path_prefix: str
    strip_prefix: bool | Unset = False





    def to_dict(self) -> dict[str, Any]:
        function = self.function

        path_prefix = self.path_prefix

        strip_prefix = self.strip_prefix


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "function": function,
            "path_prefix": path_prefix,
        })
        if strip_prefix is not UNSET:
            field_dict["strip_prefix"] = strip_prefix

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        function = d.pop("function")

        path_prefix = d.pop("path_prefix")

        strip_prefix = d.pop("strip_prefix", UNSET)

        project_config_frontend_function_route = cls(
            function=function,
            path_prefix=path_prefix,
            strip_prefix=strip_prefix,
        )

        return project_config_frontend_function_route

