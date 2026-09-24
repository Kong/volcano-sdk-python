from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="SandboxAccessRequest")



@_attrs_define
class SandboxAccessRequest:
    """ 
        Attributes:
            port (int):
            expires_in_seconds (int | Unset):  Default: 300.
     """

    port: int
    expires_in_seconds: int | Unset = 300





    def to_dict(self) -> dict[str, Any]:
        port = self.port

        expires_in_seconds = self.expires_in_seconds


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "port": port,
        })
        if expires_in_seconds is not UNSET:
            field_dict["expires_in_seconds"] = expires_in_seconds

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        port = d.pop("port")

        expires_in_seconds = d.pop("expires_in_seconds", UNSET)

        sandbox_access_request = cls(
            port=port,
            expires_in_seconds=expires_in_seconds,
        )

        return sandbox_access_request

