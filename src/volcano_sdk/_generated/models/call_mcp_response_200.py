from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.call_mcp_response_200_jsonrpc import CallMCPResponse200Jsonrpc
from ..models.call_mcp_response_200_jsonrpc import check_call_mcp_response_200_jsonrpc
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.call_mcp_response_200_error import CallMCPResponse200Error
  from ..models.call_mcp_response_200_result import CallMCPResponse200Result





T = TypeVar("T", bound="CallMCPResponse200")



@_attrs_define
class CallMCPResponse200:
    """ 
        Attributes:
            jsonrpc (CallMCPResponse200Jsonrpc):
            id (int | None | str): Echoes the request's id. Null when the request could not be read well enough to determine
                one.
            result (CallMCPResponse200Result | Unset):
            error (CallMCPResponse200Error | Unset):
     """

    jsonrpc: CallMCPResponse200Jsonrpc
    id: int | None | str
    result: CallMCPResponse200Result | Unset = UNSET
    error: CallMCPResponse200Error | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.call_mcp_response_200_error import CallMCPResponse200Error
        from ..models.call_mcp_response_200_result import CallMCPResponse200Result
        jsonrpc: str = self.jsonrpc

        id: int | None | str
        id = self.id

        result: dict[str, Any] | Unset = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.to_dict()

        error: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "jsonrpc": jsonrpc,
            "id": id,
        })
        if result is not UNSET:
            field_dict["result"] = result
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_mcp_response_200_error import CallMCPResponse200Error
        from ..models.call_mcp_response_200_result import CallMCPResponse200Result
        d = dict(src_dict)
        jsonrpc = check_call_mcp_response_200_jsonrpc(d.pop("jsonrpc"))




        def _parse_id(data: object) -> int | None | str:
            if data is None:
                return data
            return cast(int | None | str, data)

        id = _parse_id(d.pop("id"))


        _result = d.pop("result", UNSET)
        result: CallMCPResponse200Result | Unset
        if isinstance(_result,  Unset):
            result = UNSET
        else:
            result = CallMCPResponse200Result.from_dict(_result)




        _error = d.pop("error", UNSET)
        error: CallMCPResponse200Error | Unset
        if isinstance(_error,  Unset):
            error = UNSET
        else:
            error = CallMCPResponse200Error.from_dict(_error)




        call_mcp_response_200 = cls(
            jsonrpc=jsonrpc,
            id=id,
            result=result,
            error=error,
        )


        call_mcp_response_200.additional_properties = d
        return call_mcp_response_200

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
