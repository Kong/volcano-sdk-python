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
  from ..models.batch_function_deploy_failure import BatchFunctionDeployFailure
  from ..models.function import Function





T = TypeVar("T", bound="BatchFunctionDeployResponse")



@_attrs_define
class BatchFunctionDeployResponse:
    """ 
        Attributes:
            batch_id (UUID):
            data (list[Function]): Functions whose deployment workflows were started successfully
            failed (list[BatchFunctionDeployFailure] | Unset): Functions that failed before their workflow started.
                Successful functions are left running; failed new functions are deleted and failed updates are rolled back where
                possible.
     """

    batch_id: UUID
    data: list[Function]
    failed: list[BatchFunctionDeployFailure] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.batch_function_deploy_failure import BatchFunctionDeployFailure
        from ..models.function import Function
        batch_id = str(self.batch_id)

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)



        failed: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.failed, Unset):
            failed = []
            for failed_item_data in self.failed:
                failed_item = failed_item_data.to_dict()
                failed.append(failed_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "batch_id": batch_id,
            "data": data,
        })
        if failed is not UNSET:
            field_dict["failed"] = failed

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_function_deploy_failure import BatchFunctionDeployFailure
        from ..models.function import Function
        d = dict(src_dict)
        batch_id = UUID(d.pop("batch_id"))




        data = []
        _data = d.pop("data")
        for data_item_data in (_data):
            data_item = Function.from_dict(data_item_data)



            data.append(data_item)


        _failed = d.pop("failed", UNSET)
        failed: list[BatchFunctionDeployFailure] | Unset = UNSET
        if _failed is not UNSET:
            failed = []
            for failed_item_data in _failed:
                failed_item = BatchFunctionDeployFailure.from_dict(failed_item_data)



                failed.append(failed_item)


        batch_function_deploy_response = cls(
            batch_id=batch_id,
            data=data,
            failed=failed,
        )


        batch_function_deploy_response.additional_properties = d
        return batch_function_deploy_response

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
