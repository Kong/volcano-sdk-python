from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field
import json
from .. import types

from ..types import UNSET, Unset

from ..types import File, FileTypes
from io import BytesIO
from uuid import UUID






T = TypeVar("T", bound="SandboxFileArchiveForm")



@_attrs_define
class SandboxFileArchiveForm:
    """ Send `project_id`, `session_id` and `path`, in any order, then the `archive` part.

        Attributes:
            project_id (UUID):
            session_id (UUID):
            path (str): Workspace directory to extract into, relative to `/workspace`. It must name a directory below the
                workspace root; a path that resolves to the root or to `/`, such as `.`, `./`, `/`, `/workspace` or
                `/workspace/.`, is refused.
            archive (File): A tar archive, optionally gzip-compressed.
     """

    project_id: UUID
    session_id: UUID
    path: str
    archive: File
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        session_id = str(self.session_id)

        path = self.path

        archive = self.archive.to_tuple()



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "project_id": project_id,
            "session_id": session_id,
            "path": path,
            "archive": archive,
        })

        return field_dict


    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("project_id", (None, str(self.project_id), "text/plain")))



        files.append(("session_id", (None, str(self.session_id), "text/plain")))



        files.append(("path", (None, str(self.path).encode(), "text/plain")))



        files.append(("archive", self.archive.to_tuple()))




        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))



        return files


    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        session_id = UUID(d.pop("session_id"))




        path = d.pop("path")

        archive = File(
             payload = BytesIO(d.pop("archive"))
        )




        sandbox_file_archive_form = cls(
            project_id=project_id,
            session_id=session_id,
            path=path,
            archive=archive,
        )


        sandbox_file_archive_form.additional_properties = d
        return sandbox_file_archive_form

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
