from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="PlatformExchangeResponse")



@_attrs_define
class PlatformExchangeResponse:
    """ 
        Attributes:
            token (str):
            user_id (str):
            token_id (UUID):
            expires_at (datetime.datetime):
     """

    token: str
    user_id: str
    token_id: UUID
    expires_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        token = self.token

        user_id = self.user_id

        token_id = str(self.token_id)

        expires_at = self.expires_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "token": token,
            "user_id": user_id,
            "token_id": token_id,
            "expires_at": expires_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        token = d.pop("token")

        user_id = d.pop("user_id")

        token_id = UUID(d.pop("token_id"))




        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))




        platform_exchange_response = cls(
            token=token,
            user_id=user_id,
            token_id=token_id,
            expires_at=expires_at,
        )


        platform_exchange_response.additional_properties = d
        return platform_exchange_response

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
