from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="StorageBucket")



@_attrs_define
class StorageBucket:
    """ A named container for files within a project.
    Public access is controlled at the file level via is_public on StorageObject.

        Attributes:
            id (UUID):
            name (str): Bucket name (unique within project)
            project_id (UUID | Unset):
            file_size_limit (int | None | Unset): Maximum file size in bytes (null for no limit)
            allowed_mime_types (list[str] | None | Unset): Allowed MIME types (null for all types)
            last_invoked_at (datetime.datetime | Unset): Most recent bucket operation timestamp
            created_at (datetime.datetime | Unset):
            updated_at (datetime.datetime | Unset):
     """

    id: UUID
    name: str
    project_id: UUID | Unset = UNSET
    file_size_limit: int | None | Unset = UNSET
    allowed_mime_types: list[str] | None | Unset = UNSET
    last_invoked_at: datetime.datetime | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        project_id: str | Unset = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        file_size_limit: int | None | Unset
        if isinstance(self.file_size_limit, Unset):
            file_size_limit = UNSET
        else:
            file_size_limit = self.file_size_limit

        allowed_mime_types: list[str] | None | Unset
        if isinstance(self.allowed_mime_types, Unset):
            allowed_mime_types = UNSET
        elif isinstance(self.allowed_mime_types, list):
            allowed_mime_types = self.allowed_mime_types


        else:
            allowed_mime_types = self.allowed_mime_types

        last_invoked_at: str | Unset = UNSET
        if not isinstance(self.last_invoked_at, Unset):
            last_invoked_at = self.last_invoked_at.isoformat()

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
        })
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if file_size_limit is not UNSET:
            field_dict["file_size_limit"] = file_size_limit
        if allowed_mime_types is not UNSET:
            field_dict["allowed_mime_types"] = allowed_mime_types
        if last_invoked_at is not UNSET:
            field_dict["last_invoked_at"] = last_invoked_at
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        name = d.pop("name")

        _project_id = d.pop("project_id", UNSET)
        project_id: UUID | Unset
        if isinstance(_project_id,  Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)




        def _parse_file_size_limit(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        file_size_limit = _parse_file_size_limit(d.pop("file_size_limit", UNSET))


        def _parse_allowed_mime_types(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allowed_mime_types_type_0 = cast(list[str], data)

                return allowed_mime_types_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        allowed_mime_types = _parse_allowed_mime_types(d.pop("allowed_mime_types", UNSET))


        _last_invoked_at = d.pop("last_invoked_at", UNSET)
        last_invoked_at: datetime.datetime | Unset
        if isinstance(_last_invoked_at,  Unset):
            last_invoked_at = UNSET
        else:
            last_invoked_at = datetime.datetime.fromisoformat(_last_invoked_at)




        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)




        _updated_at = d.pop("updated_at", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at,  Unset):
            updated_at = UNSET
        else:
            updated_at = datetime.datetime.fromisoformat(_updated_at)




        storage_bucket = cls(
            id=id,
            name=name,
            project_id=project_id,
            file_size_limit=file_size_limit,
            allowed_mime_types=allowed_mime_types,
            last_invoked_at=last_invoked_at,
            created_at=created_at,
            updated_at=updated_at,
        )


        storage_bucket.additional_properties = d
        return storage_bucket

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
