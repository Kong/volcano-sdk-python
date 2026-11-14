from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ProjectConfigFrontendRoute")



@_attrs_define
class ProjectConfigFrontendRoute:
    """ 
        Attributes:
            frontend (str): Name of another existing frontend in the project to mount. Paths are forwarded unchanged.
            path_prefix (str):
     """

    frontend: str
    path_prefix: str





    def to_dict(self) -> dict[str, Any]:
        frontend = self.frontend

        path_prefix = self.path_prefix


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "frontend": frontend,
            "path_prefix": path_prefix,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        frontend = d.pop("frontend")

        path_prefix = d.pop("path_prefix")

        project_config_frontend_route = cls(
            frontend=frontend,
            path_prefix=path_prefix,
        )

        return project_config_frontend_route

