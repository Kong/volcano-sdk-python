from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.durable_callback_error import DurableCallbackError





T = TypeVar("T", bound="FailDurableCallbackRequest")



@_attrs_define
class FailDurableCallbackRequest:
    """ 
        Attributes:
            token (str): The `vcb_` token the workflow handed out. It is the only credential
                the callback operations take, so treat it as a secret.
            error (DurableCallbackError): The error the waiting step raises.
     """

    token: str
    error: DurableCallbackError





    def to_dict(self) -> dict[str, Any]:
        from ..models.durable_callback_error import DurableCallbackError # noqa: PLC0415
        token = self.token

        error = self.error.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "token": token,
            "error": error,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.durable_callback_error import DurableCallbackError # noqa: PLC0415
        d = dict(src_dict)
        token = d.pop("token")

        error = DurableCallbackError.from_dict(d.pop("error"))




        fail_durable_callback_request = cls(
            token=token,
            error=error,
        )

        return fail_durable_callback_request

