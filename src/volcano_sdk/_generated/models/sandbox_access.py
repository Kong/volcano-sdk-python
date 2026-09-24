from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="SandboxAccess")



@_attrs_define
class SandboxAccess:
    """ 
        Attributes:
            url (str):
            token (str):
            expires_at (datetime.datetime):
     """

    url: str
    token: str
    expires_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        url = self.url

        token = self.token

        expires_at = self.expires_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "url": url,
            "token": token,
            "expires_at": expires_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        token = d.pop("token")

        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))




        sandbox_access = cls(
            url=url,
            token=token,
            expires_at=expires_at,
        )

        return sandbox_access

