from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_storage_policy_request_operation import check_create_storage_policy_request_operation
from ..models.create_storage_policy_request_operation import CreateStoragePolicyRequestOperation
from typing import cast






T = TypeVar("T", bound="CreateStoragePolicyRequest")



@_attrs_define
class CreateStoragePolicyRequest:
    """ 
        Attributes:
            name (str): Policy name
            operation (CreateStoragePolicyRequestOperation): Operation this policy applies to
            definition (str): Policy expression
     """

    name: str
    operation: CreateStoragePolicyRequestOperation
    definition: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        operation: str = self.operation

        definition = self.definition


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "operation": operation,
            "definition": definition,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        operation = check_create_storage_policy_request_operation(d.pop("operation"))




        definition = d.pop("definition")

        create_storage_policy_request = cls(
            name=name,
            operation=operation,
            definition=definition,
        )


        create_storage_policy_request.additional_properties = d
        return create_storage_policy_request

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
