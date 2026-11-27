from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="SandboxFilePart")



@_attrs_define
class SandboxFilePart:
    """
        Attributes:
            project_id (UUID):
            session_id (UUID):
            path (str):
            offset (int):
            size (int):
            received (int): Bytes of the file received through the end of this part.
            complete (bool): True when this part finished the file and it is now at `path`.
     """

    project_id: UUID
    session_id: UUID
    path: str
    offset: int
    size: int
    received: int
    complete: bool





    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        session_id = str(self.session_id)

        path = self.path

        offset = self.offset

        size = self.size

        received = self.received

        complete = self.complete


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "project_id": project_id,
            "session_id": session_id,
            "path": path,
            "offset": offset,
            "size": size,
            "received": received,
            "complete": complete,
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

        received = d.pop("received")

        complete = d.pop("complete")

        sandbox_file_part = cls(
            project_id=project_id,
            session_id=session_id,
            path=path,
            offset=offset,
            size=size,
            received=received,
            complete=complete,
        )

        return sandbox_file_part
