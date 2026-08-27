from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.function_invocation_request_payload import FunctionInvocationRequestPayload





T = TypeVar("T", bound="FunctionInvocationRequest")



@_attrs_define
class FunctionInvocationRequest:
    """ 
        Attributes:
            payload (FunctionInvocationRequestPayload | Unset): Payload to send to the function.

                If invoked with auth user token, Volcano automatically injects `__volcano_auth` context:
                ```javascript
                {
                  ...yourPayload,
                  __volcano_auth: {
                    user_id: "uuid",
                    email: "user@example.com",
                    project_id: "uuid",
                    role: "authenticated" | "anonymous"
                  }
                }
                ```
     """

    payload: FunctionInvocationRequestPayload | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.function_invocation_request_payload import FunctionInvocationRequestPayload
        payload: dict[str, Any] | Unset = UNSET
        if not isinstance(self.payload, Unset):
            payload = self.payload.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if payload is not UNSET:
            field_dict["payload"] = payload

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.function_invocation_request_payload import FunctionInvocationRequestPayload
        d = dict(src_dict)
        _payload = d.pop("payload", UNSET)
        payload: FunctionInvocationRequestPayload | Unset
        if isinstance(_payload,  Unset):
            payload = UNSET
        else:
            payload = FunctionInvocationRequestPayload.from_dict(_payload)




        function_invocation_request = cls(
            payload=payload,
        )


        function_invocation_request.additional_properties = d
        return function_invocation_request

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
