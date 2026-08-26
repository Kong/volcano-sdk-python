from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.storage_policy_operation import check_storage_policy_operation
from ..models.storage_policy_operation import StoragePolicyOperation
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="StoragePolicy")



@_attrs_define
class StoragePolicy:
    """ 
        Attributes:
            id (UUID):
            bucket_id (UUID):
            name (str): Policy name (unique within bucket)
            operation (StoragePolicyOperation): Operation this policy applies to
            definition (str): Policy expression evaluated at request time.
                Examples:
                - "true" - Allow all
                - "auth.uid() = owner_id" - Owner only
                - "auth.role() = 'authenticated'" - Authenticated users
                - "(storage.foldername(name))[1] = auth.uid()::text" - User's folder
            created_at (datetime.datetime | Unset):
            updated_at (datetime.datetime | Unset):
     """

    id: UUID
    bucket_id: UUID
    name: str
    operation: StoragePolicyOperation
    definition: str
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        bucket_id = str(self.bucket_id)

        name = self.name

        operation: str = self.operation

        definition = self.definition

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
            "bucket_id": bucket_id,
            "name": name,
            "operation": operation,
            "definition": definition,
        })
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        bucket_id = UUID(d.pop("bucket_id"))




        name = d.pop("name")

        operation = check_storage_policy_operation(d.pop("operation"))




        definition = d.pop("definition")

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




        storage_policy = cls(
            id=id,
            bucket_id=bucket_id,
            name=name,
            operation=operation,
            definition=definition,
            created_at=created_at,
            updated_at=updated_at,
        )


        storage_policy.additional_properties = d
        return storage_policy

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
