from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SucceedDurableCallbackRequest")



@_attrs_define
class SucceedDurableCallbackRequest:
    """ 
        Attributes:
            token (str): The `vcb_` token the workflow handed out. It is the only credential
                the callback operations take, so treat it as a secret.
            result (Any): Any JSON value other than null, up to 64 KiB. The waiting step
                resolves with it. Null is refused because a timeout resolves the
                step with null.
     """

    token: str
    result: Any





    def to_dict(self) -> dict[str, Any]:
        token = self.token

        result = self.result


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "token": token,
            "result": result,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        token = d.pop("token")

        result = d.pop("result")

        succeed_durable_callback_request = cls(
            token=token,
            result=result,
        )

        return succeed_durable_callback_request

