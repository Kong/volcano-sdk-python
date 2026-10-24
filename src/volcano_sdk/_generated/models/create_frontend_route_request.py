from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="CreateFrontendRouteRequest")



@_attrs_define
class CreateFrontendRouteRequest:
    """ 
        Attributes:
            target_frontend_id (UUID): The Frontend to mount. It must be another Frontend in the Project.
            path_prefix (str):
     """

    target_frontend_id: UUID
    path_prefix: str





    def to_dict(self) -> dict[str, Any]:
        target_frontend_id = str(self.target_frontend_id)

        path_prefix = self.path_prefix


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "target_frontend_id": target_frontend_id,
            "path_prefix": path_prefix,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target_frontend_id = UUID(d.pop("target_frontend_id"))




        path_prefix = d.pop("path_prefix")

        create_frontend_route_request = cls(
            target_frontend_id=target_frontend_id,
            path_prefix=path_prefix,
        )

        return create_frontend_route_request

