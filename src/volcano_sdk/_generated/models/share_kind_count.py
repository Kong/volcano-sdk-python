from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.share_kind_count_kind import check_share_kind_count_kind
from ..models.share_kind_count_kind import ShareKindCountKind
from typing import cast






T = TypeVar("T", bound="ShareKindCount")



@_attrs_define
class ShareKindCount:
    """ 
        Attributes:
            kind (ShareKindCountKind):
            events (int):
            visitors (int): Unique daily visitors among the events that carried one. A visitor is pseudonymised per day, so
                one who returns on another day counts again.
     """

    kind: ShareKindCountKind
    events: int
    visitors: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        events = self.events

        visitors = self.visitors


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "kind": kind,
            "events": events,
            "visitors": visitors,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_share_kind_count_kind(d.pop("kind"))




        events = d.pop("events")

        visitors = d.pop("visitors")

        share_kind_count = cls(
            kind=kind,
            events=events,
            visitors=visitors,
        )


        share_kind_count.additional_properties = d
        return share_kind_count

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
