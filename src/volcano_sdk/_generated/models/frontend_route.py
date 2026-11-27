from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="FrontendRoute")



@_attrs_define
class FrontendRoute:
    """ A path prefix on this Frontend's hostnames served by another Frontend in the Project, the
    mounted Frontend. Paths are forwarded unchanged, so the mounted Frontend serves its prefix
    as real pages (page directories or a matching `basePath`).

        Attributes:
            id (UUID):
            project_id (UUID):
            frontend_id (UUID): The Frontend whose hostnames serve the route
            target_frontend_id (UUID): The mounted Frontend
            path_prefix (str):
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
     """

    id: UUID
    project_id: UUID
    frontend_id: UUID
    target_frontend_id: UUID
    path_prefix: str
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id = str(self.project_id)

        frontend_id = str(self.frontend_id)

        target_frontend_id = str(self.target_frontend_id)

        path_prefix = self.path_prefix

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "project_id": project_id,
            "frontend_id": frontend_id,
            "target_frontend_id": target_frontend_id,
            "path_prefix": path_prefix,
            "created_at": created_at,
            "updated_at": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        frontend_id = UUID(d.pop("frontend_id"))




        target_frontend_id = UUID(d.pop("target_frontend_id"))




        path_prefix = d.pop("path_prefix")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        frontend_route = cls(
            id=id,
            project_id=project_id,
            frontend_id=frontend_id,
            target_frontend_id=target_frontend_id,
            path_prefix=path_prefix,
            created_at=created_at,
            updated_at=updated_at,
        )

        return frontend_route

