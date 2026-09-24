from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="SandboxSubjectGrantRequest")



@_attrs_define
class SandboxSubjectGrantRequest:
    """ 
        Attributes:
            expires_at (datetime.datetime):
     """

    expires_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        expires_at = self.expires_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "expires_at": expires_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))




        sandbox_subject_grant_request = cls(
            expires_at=expires_at,
        )

        return sandbox_subject_grant_request

