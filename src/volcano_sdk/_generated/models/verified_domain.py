from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="VerifiedDomain")



@_attrs_define
class VerifiedDomain:
    """ A domain the account owns, along with every name below it.

        Attributes:
            domain (str):  Example: example.com.
            verified_at (datetime.datetime): When the account last proved ownership.
     """

    domain: str
    verified_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        domain = self.domain

        verified_at = self.verified_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "domain": domain,
            "verified_at": verified_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        domain = d.pop("domain")

        verified_at = datetime.datetime.fromisoformat(d.pop("verified_at"))




        verified_domain = cls(
            domain=domain,
            verified_at=verified_at,
        )


        verified_domain.additional_properties = d
        return verified_domain

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
