from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="FrontendDomainVerificationRecord")



@_attrs_define
class FrontendDomainVerificationRecord:
    """ 
        Attributes:
            name (str):
            type_ (str):
            value (str):
     """

    name: str
    type_: str
    value: str





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_

        value = self.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
            "type": type_,
            "value": value,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        type_ = d.pop("type")

        value = d.pop("value")

        frontend_domain_verification_record = cls(
            name=name,
            type_=type_,
            value=value,
        )

        return frontend_domain_verification_record

