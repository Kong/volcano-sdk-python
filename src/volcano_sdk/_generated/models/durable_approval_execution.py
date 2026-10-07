from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.durable_execution_status import check_durable_execution_status
from ..models.durable_execution_status import DurableExecutionStatus
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="DurableApprovalExecution")



@_attrs_define
class DurableApprovalExecution:
    """ The durable execution that requested the approval. `id` and `status`
    are null once the execution is no longer retained; `name` is kept.

        Attributes:
            id (None | UUID):
            name (str):
            status (DurableExecutionStatus | None):
     """

    id: None | UUID
    name: str
    status: DurableExecutionStatus | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id: None | str
        if isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        name = self.name

        status: None | str
        if isinstance(self.status, str):
            status = self.status
        else:
            status = self.status


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                id_type_0 = UUID(data)



                return id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        id = _parse_id(d.pop("id"))


        name = d.pop("name")

        def _parse_status(data: object) -> DurableExecutionStatus | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_1 = check_durable_execution_status(data)



                return status_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DurableExecutionStatus | None, data)

        status = _parse_status(d.pop("status"))


        durable_approval_execution = cls(
            id=id,
            name=name,
            status=status,
        )


        durable_approval_execution.additional_properties = d
        return durable_approval_execution

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
