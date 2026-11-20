from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="CreateIssueRequest")



@_attrs_define
class CreateIssueRequest:
    """ The project, and an issue a person writes on it, describing what to fix.

        Attributes:
            project_id (UUID): The project to write the issue on.
            description (str): What to fix, in your words, up to 4,000 characters. It can span lines. Leading and trailing
                whitespace is trimmed, and a description of only whitespace is refused.
            title (str | Unset): A title, on one line, up to 200 characters; whitespace, line breaks included, collapses to
                single spaces. Omitted, the title is the description's first line, cut to 80 characters with an ellipsis.
     """

    project_id: UUID
    description: str
    title: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        description = self.description

        title = self.title


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "project_id": project_id,
            "description": description,
        })
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        description = d.pop("description")

        title = d.pop("title", UNSET)

        create_issue_request = cls(
            project_id=project_id,
            description=description,
            title=title,
        )

        return create_issue_request

