from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="HeartbeatDurableCallbackRequest")



@_attrs_define
class HeartbeatDurableCallbackRequest:
    """ 
        Attributes:
            token (str): The `vcb_` token the workflow handed out. It is the only credential
                the callback operations take, so treat it as a secret.
     """

    token: str





    def to_dict(self) -> dict[str, Any]:
        token = self.token


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "token": token,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        token = d.pop("token")

        heartbeat_durable_callback_request = cls(
            token=token,
        )

        return heartbeat_durable_callback_request

