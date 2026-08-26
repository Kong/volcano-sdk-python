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

if TYPE_CHECKING:
  from ..models.storage_object_metadata import StorageObjectMetadata





T = TypeVar("T", bound="StorageObject")



@_attrs_define
class StorageObject:
    """ 
        Attributes:
            id (UUID):
            bucket_id (UUID):
            name (str): Full path within bucket (e.g., "users/abc123/avatar.png")
            is_public (bool): If true, the file can be downloaded with just an anon key (no user authentication).
                Files are private by default. Only the owner or a service key can change visibility.
                 Default: False.
            size (int): File size in bytes
            mime_type (str): MIME type
            owner_id (None | Unset | UUID): Auth user who uploaded (null for anonymous/service)
            etag (str | Unset): Entity tag for cache validation
            metadata (StorageObjectMetadata | Unset): Custom user metadata (key-value pairs).
                Limits: Maximum 50 keys, maximum 10KB total serialized size.
            created_at (datetime.datetime | Unset):
            updated_at (datetime.datetime | Unset):
            public_url (str | Unset): Shareable public URL for this file (only set for public files with is_public=true).
                This URL requires NO authentication and can be embedded in HTML, shared via email, etc.
                The URL is properly URL-encoded by the server - use it as-is without additional encoding.
     """

    id: UUID
    bucket_id: UUID
    name: str
    size: int
    mime_type: str
    is_public: bool = False
    owner_id: None | Unset | UUID = UNSET
    etag: str | Unset = UNSET
    metadata: StorageObjectMetadata | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    public_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.storage_object_metadata import StorageObjectMetadata
        id = str(self.id)

        bucket_id = str(self.bucket_id)

        name = self.name

        is_public = self.is_public

        size = self.size

        mime_type = self.mime_type

        owner_id: None | str | Unset
        if isinstance(self.owner_id, Unset):
            owner_id = UNSET
        elif isinstance(self.owner_id, UUID):
            owner_id = str(self.owner_id)
        else:
            owner_id = self.owner_id

        etag = self.etag

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        public_url = self.public_url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "bucket_id": bucket_id,
            "name": name,
            "is_public": is_public,
            "size": size,
            "mime_type": mime_type,
        })
        if owner_id is not UNSET:
            field_dict["owner_id"] = owner_id
        if etag is not UNSET:
            field_dict["etag"] = etag
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if public_url is not UNSET:
            field_dict["public_url"] = public_url

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.storage_object_metadata import StorageObjectMetadata
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        bucket_id = UUID(d.pop("bucket_id"))




        name = d.pop("name")

        is_public = d.pop("is_public")

        size = d.pop("size")

        mime_type = d.pop("mime_type")

        def _parse_owner_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                owner_id_type_0 = UUID(data)



                return owner_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        owner_id = _parse_owner_id(d.pop("owner_id", UNSET))


        etag = d.pop("etag", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: StorageObjectMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = StorageObjectMetadata.from_dict(_metadata)




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




        public_url = d.pop("public_url", UNSET)

        storage_object = cls(
            id=id,
            bucket_id=bucket_id,
            name=name,
            is_public=is_public,
            size=size,
            mime_type=mime_type,
            owner_id=owner_id,
            etag=etag,
            metadata=metadata,
            created_at=created_at,
            updated_at=updated_at,
            public_url=public_url,
        )


        storage_object.additional_properties = d
        return storage_object

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
