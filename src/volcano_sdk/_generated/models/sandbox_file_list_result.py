from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.sandbox_file_entry import SandboxFileEntry





T = TypeVar("T", bound="SandboxFileListResult")



@_attrs_define
class SandboxFileListResult:
    """
        Attributes:
            project_id (UUID): The project the session belongs to.
            session_id (UUID): The session listed.
            entries (list[SandboxFileEntry]): Entries sorted by path, compared one path element at a time by bytes, so a
                directory comes right before its contents.
            unsupported_names (int | Unset): How many names directly inside the listed directory no entry can carry: names
                that are not UTF-8, or whose path would pass 4096 bytes. The listing skips them and everything below them. Every
                page reports it. Absent when there are none.
            next_cursor (str | Unset): Present when more entries remain. Pass it as `cursor` to get the next page.
     """

    project_id: UUID
    session_id: UUID
    entries: list[SandboxFileEntry]
    unsupported_names: int | Unset = UNSET
    next_cursor: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.sandbox_file_entry import SandboxFileEntry # noqa: PLC0415
        project_id = str(self.project_id)

        session_id = str(self.session_id)

        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()
            entries.append(entries_item)



        unsupported_names = self.unsupported_names

        next_cursor = self.next_cursor


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "project_id": project_id,
            "session_id": session_id,
            "entries": entries,
        })
        if unsupported_names is not UNSET:
            field_dict["unsupported_names"] = unsupported_names
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_file_entry import SandboxFileEntry # noqa: PLC0415
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        session_id = UUID(d.pop("session_id"))




        entries = []
        _entries = d.pop("entries")
        for entries_item_data in (_entries):
            entries_item = SandboxFileEntry.from_dict(entries_item_data)



            entries.append(entries_item)


        unsupported_names = d.pop("unsupported_names", UNSET)

        next_cursor = d.pop("next_cursor", UNSET)

        sandbox_file_list_result = cls(
            project_id=project_id,
            session_id=session_id,
            entries=entries,
            unsupported_names=unsupported_names,
            next_cursor=next_cursor,
        )

        return sandbox_file_list_result
