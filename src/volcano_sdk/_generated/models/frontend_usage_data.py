from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="FrontendUsageData")



@_attrs_define
class FrontendUsageData:
    """ Monthly frontend request totals grouped by frontend.

        Attributes:
            frontend_id (UUID): Frontend ID
            requests (int): Total requests for this frontend in the current usage month
            frontend_name (None | str | Unset): Frontend name at the time usage was fetched
     """

    frontend_id: UUID
    requests: int
    frontend_name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        frontend_id = str(self.frontend_id)

        requests = self.requests

        frontend_name: None | str | Unset
        if isinstance(self.frontend_name, Unset):
            frontend_name = UNSET
        else:
            frontend_name = self.frontend_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "frontend_id": frontend_id,
            "requests": requests,
        })
        if frontend_name is not UNSET:
            field_dict["frontend_name"] = frontend_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        frontend_id = UUID(d.pop("frontend_id"))




        requests = d.pop("requests")

        def _parse_frontend_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        frontend_name = _parse_frontend_name(d.pop("frontend_name", UNSET))


        frontend_usage_data = cls(
            frontend_id=frontend_id,
            requests=requests,
            frontend_name=frontend_name,
        )


        frontend_usage_data.additional_properties = d
        return frontend_usage_data

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
