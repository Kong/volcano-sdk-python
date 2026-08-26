from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.schedule_request_kind import check_schedule_request_kind
from ..models.schedule_request_kind import ScheduleRequestKind
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ScheduleRequest")



@_attrs_define
class ScheduleRequest:
    """ 
        Attributes:
            cron_expression (str): Standard 5-field cron expression evaluated in UTC. Seconds fields, descriptors, and
                Quartz syntax are not supported. Example: */5 * * * *.
            kind (ScheduleRequestKind | Unset):  Default: 'cron'.
     """

    cron_expression: str
    kind: ScheduleRequestKind | Unset = 'cron'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        cron_expression = self.cron_expression

        kind: str | Unset = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "cron_expression": cron_expression,
        })
        if kind is not UNSET:
            field_dict["kind"] = kind

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cron_expression = d.pop("cron_expression")

        _kind = d.pop("kind", UNSET)
        kind: ScheduleRequestKind | Unset
        if isinstance(_kind,  Unset):
            kind = UNSET
        else:
            kind = check_schedule_request_kind(_kind)




        schedule_request = cls(
            cron_expression=cron_expression,
            kind=kind,
        )


        schedule_request.additional_properties = d
        return schedule_request

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
