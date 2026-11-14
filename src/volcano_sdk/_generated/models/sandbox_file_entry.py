from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.sandbox_file_entry_sha_256_skipped import check_sandbox_file_entry_sha_256_skipped
from ..models.sandbox_file_entry_sha_256_skipped import SandboxFileEntrySha256Skipped
from ..models.sandbox_file_entry_type import check_sandbox_file_entry_type
from ..models.sandbox_file_entry_type import SandboxFileEntryType
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="SandboxFileEntry")



@_attrs_define
class SandboxFileEntry:
    """
        Attributes:
            path (str): Path relative to the workspace root, usable with the read and write file routes.
            type_ (SandboxFileEntryType): Entry type from the entry itself. A symlink is reported, never followed.
            size (int): Size in bytes of a regular file; 0 for every other type.
            mode (int): Permission bits, including setuid, setgid and sticky (`st_mode & 07777`). For example, 420 is `0644`
                and 493 is `0755`.
            sha256 (str | Unset): Lowercase hex SHA-256 of a regular file's content, present only when `include_sha256` is
                true and the file could be hashed.
            sha256_skipped (SandboxFileEntrySha256Skipped | Unset): Why a regular file has no `sha256` when `include_sha256`
                is true. `budget` is a file over 256 MiB. `changing` is a file that changed while it was hashed or kept
                changing; list it again later. `unreadable` is a file the session user doesn't own, whose owner-read bit
                (`0400`) is clear, or that has more than one hard link. Treat such a file as unverified.
            unreadable (bool | Unset): True on a directory the session user can't list; the listing doesn't enter it. The
                user's permission bits on the directory lack read or execute: the owner bits when the user owns it, the group
                bits when it belongs to the user's group, and the other bits otherwise. Absent on every other entry.
            unsupported_names (int | Unset): In a recursive listing, how many names directly inside this directory no entry
                can carry: names that are not UTF-8, or whose path would pass 4096 bytes. The listing skips them and everything
                below them. Absent when there are none.
     """

    path: str
    type_: SandboxFileEntryType
    size: int
    mode: int
    sha256: str | Unset = UNSET
    sha256_skipped: SandboxFileEntrySha256Skipped | Unset = UNSET
    unreadable: bool | Unset = UNSET
    unsupported_names: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        path = self.path

        type_: str = self.type_

        size = self.size

        mode = self.mode

        sha256 = self.sha256

        sha256_skipped: str | Unset = UNSET
        if not isinstance(self.sha256_skipped, Unset):
            sha256_skipped = self.sha256_skipped


        unreadable = self.unreadable

        unsupported_names = self.unsupported_names


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "path": path,
            "type": type_,
            "size": size,
            "mode": mode,
        })
        if sha256 is not UNSET:
            field_dict["sha256"] = sha256
        if sha256_skipped is not UNSET:
            field_dict["sha256_skipped"] = sha256_skipped
        if unreadable is not UNSET:
            field_dict["unreadable"] = unreadable
        if unsupported_names is not UNSET:
            field_dict["unsupported_names"] = unsupported_names

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        type_ = check_sandbox_file_entry_type(d.pop("type"))




        size = d.pop("size")

        mode = d.pop("mode")

        sha256 = d.pop("sha256", UNSET)

        _sha256_skipped = d.pop("sha256_skipped", UNSET)
        sha256_skipped: SandboxFileEntrySha256Skipped | Unset
        if isinstance(_sha256_skipped,  Unset):
            sha256_skipped = UNSET
        else:
            sha256_skipped = check_sandbox_file_entry_sha_256_skipped(_sha256_skipped)




        unreadable = d.pop("unreadable", UNSET)

        unsupported_names = d.pop("unsupported_names", UNSET)

        sandbox_file_entry = cls(
            path=path,
            type_=type_,
            size=size,
            mode=mode,
            sha256=sha256,
            sha256_skipped=sha256_skipped,
            unreadable=unreadable,
            unsupported_names=unsupported_names,
        )

        return sandbox_file_entry
