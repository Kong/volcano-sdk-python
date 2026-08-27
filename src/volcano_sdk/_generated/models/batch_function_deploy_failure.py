from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.batch_function_deploy_failure_operation import BatchFunctionDeployFailureOperation
from ..models.batch_function_deploy_failure_operation import check_batch_function_deploy_failure_operation
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="BatchFunctionDeployFailure")



@_attrs_define
class BatchFunctionDeployFailure:
    """ 
        Attributes:
            name (str):
            error (str):
            function_id (UUID | Unset):
            operation (BatchFunctionDeployFailureOperation | Unset):
     """

    name: str
    error: str
    function_id: UUID | Unset = UNSET
    operation: BatchFunctionDeployFailureOperation | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        error = self.error

        function_id: str | Unset = UNSET
        if not isinstance(self.function_id, Unset):
            function_id = str(self.function_id)

        operation: str | Unset = UNSET
        if not isinstance(self.operation, Unset):
            operation = self.operation



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "error": error,
        })
        if function_id is not UNSET:
            field_dict["function_id"] = function_id
        if operation is not UNSET:
            field_dict["operation"] = operation

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        error = d.pop("error")

        _function_id = d.pop("function_id", UNSET)
        function_id: UUID | Unset
        if isinstance(_function_id,  Unset):
            function_id = UNSET
        else:
            function_id = UUID(_function_id)




        _operation = d.pop("operation", UNSET)
        operation: BatchFunctionDeployFailureOperation | Unset
        if isinstance(_operation,  Unset):
            operation = UNSET
        else:
            operation = check_batch_function_deploy_failure_operation(_operation)




        batch_function_deploy_failure = cls(
            name=name,
            error=error,
            function_id=function_id,
            operation=operation,
        )


        batch_function_deploy_failure.additional_properties = d
        return batch_function_deploy_failure

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
