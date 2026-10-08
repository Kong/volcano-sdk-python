from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.durable_approval_counts import DurableApprovalCounts
  from ..models.durable_approval_function import DurableApprovalFunction





T = TypeVar("T", bound="DurableApprovalFunctionCounts")



@_attrs_define
class DurableApprovalFunctionCounts:
    """ 
        Attributes:
            function (DurableApprovalFunction): The durable function that requested the approval. `id` is null once the
                function has been deleted; `name` is kept.
            counts (DurableApprovalCounts): Approvals by status. `requested` is every approval, whatever its status.
     """

    function: DurableApprovalFunction
    counts: DurableApprovalCounts
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.durable_approval_counts import DurableApprovalCounts # noqa: PLC0415
        from ..models.durable_approval_function import DurableApprovalFunction # noqa: PLC0415
        function = self.function.to_dict()

        counts = self.counts.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "function": function,
            "counts": counts,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.durable_approval_counts import DurableApprovalCounts # noqa: PLC0415
        from ..models.durable_approval_function import DurableApprovalFunction # noqa: PLC0415
        d = dict(src_dict)
        function = DurableApprovalFunction.from_dict(d.pop("function"))




        counts = DurableApprovalCounts.from_dict(d.pop("counts"))




        durable_approval_function_counts = cls(
            function=function,
            counts=counts,
        )


        durable_approval_function_counts.additional_properties = d
        return durable_approval_function_counts

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
