from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.durable_callback_status import check_durable_callback_status
from ..models.durable_callback_status import DurableCallbackStatus
from typing import cast






T = TypeVar("T", bound="DurableCallbackOutcome")



@_attrs_define
class DurableCallbackOutcome:
    """ 
        Attributes:
            status (DurableCallbackStatus): `waiting` until the token is succeeded or failed. `delivering` while
                the outcome is on its way to the workflow; Volcano finishes the
                delivery on its own. `succeeded` or `failed` once the workflow has the
                outcome.
     """

    status: DurableCallbackStatus
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        status: str = self.status


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = check_durable_callback_status(d.pop("status"))




        durable_callback_outcome = cls(
            status=status,
        )


        durable_callback_outcome.additional_properties = d
        return durable_callback_outcome

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
