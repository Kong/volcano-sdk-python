from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="SandboxFilePartRequest")



@_attrs_define
class SandboxFilePartRequest:
    """
        Attributes:
            project_id (UUID):
            session_id (UUID):
            path (str): Workspace file to write, relative to `/workspace`.
            offset (int): Byte offset of this part's data in the file.
            size (int): Size of the whole file in bytes, at most 1 GiB.
            sha256 (str): Lowercase hex SHA-256 of the whole file.
            data (str): This part's bytes, at most 8 MiB.
     """

    project_id: UUID
    session_id: UUID
    path: str
    offset: int
    size: int
    sha256: str
    data: str





    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        session_id = str(self.session_id)

        path = self.path

        offset = self.offset

        size = self.size

        sha256 = self.sha256

        data = self.data


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "project_id": project_id,
            "session_id": session_id,
            "path": path,
            "offset": offset,
            "size": size,
            "sha256": sha256,
            "data": data,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        session_id = UUID(d.pop("session_id"))




        path = d.pop("path")

        offset = d.pop("offset")

        size = d.pop("size")

        sha256 = d.pop("sha256")

        data = d.pop("data")

        sandbox_file_part_request = cls(
            project_id=project_id,
            session_id=session_id,
            path=path,
            offset=offset,
            size=size,
            sha256=sha256,
            data=data,
        )

        return sandbox_file_part_request
