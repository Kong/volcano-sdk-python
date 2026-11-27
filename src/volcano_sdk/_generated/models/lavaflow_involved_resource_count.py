from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.lavaflow_resource_reference import LavaflowResourceReference





T = TypeVar("T", bound="LavaflowInvolvedResourceCount")



@_attrs_define
class LavaflowInvolvedResourceCount:
    """ A resource and how many matching runs involve it.

        Attributes:
            resource (LavaflowResourceReference): A function, durable function or frontend in the project, or the project of
                a user-reported problem.
            runs (int):
     """

    resource: LavaflowResourceReference
    runs: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_resource_reference import LavaflowResourceReference # noqa: PLC0415
        resource = self.resource.to_dict()

        runs = self.runs


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "resource": resource,
            "runs": runs,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_resource_reference import LavaflowResourceReference # noqa: PLC0415
        d = dict(src_dict)
        resource = LavaflowResourceReference.from_dict(d.pop("resource"))




        runs = d.pop("runs")

        lavaflow_involved_resource_count = cls(
            resource=resource,
            runs=runs,
        )


        lavaflow_involved_resource_count.additional_properties = d
        return lavaflow_involved_resource_count

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
