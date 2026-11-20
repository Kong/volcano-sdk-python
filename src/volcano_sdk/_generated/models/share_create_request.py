from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="ShareCreateRequest")



@_attrs_define
class ShareCreateRequest:
    """ 
        Attributes:
            project_id (UUID): The project to share. A project the caller can't share answers like one that doesn't exist.
            suggested_name (str | Unset): A project name for clients to offer visitors as the default; the create request
                still carries its own `name`. It may contain only letters, numbers, underscores and hyphens.
            description (str | Unset): What the project does, shown to visitors before they deploy. One line of plain text
                with no control characters; surrounding spaces are trimmed.
            allow_reshare (bool | Unset): Lets the projects made from this link be shared again by their owners. Defaults to
                false.
     """

    project_id: UUID
    suggested_name: str | Unset = UNSET
    description: str | Unset = UNSET
    allow_reshare: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        suggested_name = self.suggested_name

        description = self.description

        allow_reshare = self.allow_reshare


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "project_id": project_id,
        })
        if suggested_name is not UNSET:
            field_dict["suggested_name"] = suggested_name
        if description is not UNSET:
            field_dict["description"] = description
        if allow_reshare is not UNSET:
            field_dict["allow_reshare"] = allow_reshare

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        suggested_name = d.pop("suggested_name", UNSET)

        description = d.pop("description", UNSET)

        allow_reshare = d.pop("allow_reshare", UNSET)

        share_create_request = cls(
            project_id=project_id,
            suggested_name=suggested_name,
            description=description,
            allow_reshare=allow_reshare,
        )

        return share_create_request

