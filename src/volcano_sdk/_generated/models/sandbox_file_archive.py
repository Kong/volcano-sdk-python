from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="SandboxFileArchive")



@_attrs_define
class SandboxFileArchive:
    """
        Attributes:
            project_id (UUID):
            session_id (UUID):
            path (str):
            files (int): Regular files written.
            bytes_ (int): Bytes of file content written.
     """

    project_id: UUID
    session_id: UUID
    path: str
    files: int
    bytes_: int





    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        session_id = str(self.session_id)

        path = self.path

        files = self.files

        bytes_ = self.bytes_


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "project_id": project_id,
            "session_id": session_id,
            "path": path,
            "files": files,
            "bytes": bytes_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        session_id = UUID(d.pop("session_id"))




        path = d.pop("path")

        files = d.pop("files")

        bytes_ = d.pop("bytes")

        sandbox_file_archive = cls(
            project_id=project_id,
            session_id=session_id,
            path=path,
            files=files,
            bytes_=bytes_,
        )

        return sandbox_file_archive
