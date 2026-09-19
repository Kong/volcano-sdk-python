from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.call_mcp_body_jsonrpc import CallMCPBodyJsonrpc
from ..models.call_mcp_body_jsonrpc import check_call_mcp_body_jsonrpc
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.call_mcp_body_params import CallMCPBodyParams





T = TypeVar("T", bound="CallMCPBody")



@_attrs_define
class CallMCPBody:
    """ A JSON-RPC 2.0 request object.

        Attributes:
            jsonrpc (CallMCPBodyJsonrpc):
            method (str): The MCP method to call.
            id (int | str | Unset): Request identifier, echoed verbatim. Omit it to send a
                notification, which is answered with `202` and no body.
            params (CallMCPBodyParams | Unset):
     """

    jsonrpc: CallMCPBodyJsonrpc
    method: str
    id: int | str | Unset = UNSET
    params: CallMCPBodyParams | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.call_mcp_body_params import CallMCPBodyParams
        jsonrpc: str = self.jsonrpc

        method = self.method

        id: int | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        params: dict[str, Any] | Unset = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "jsonrpc": jsonrpc,
            "method": method,
        })
        if id is not UNSET:
            field_dict["id"] = id
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_mcp_body_params import CallMCPBodyParams
        d = dict(src_dict)
        jsonrpc = check_call_mcp_body_jsonrpc(d.pop("jsonrpc"))




        method = d.pop("method")

        def _parse_id(data: object) -> int | str | Unset:
            if isinstance(data, Unset):
                return data
            return cast(int | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))


        _params = d.pop("params", UNSET)
        params: CallMCPBodyParams | Unset
        if isinstance(_params,  Unset):
            params = UNSET
        else:
            params = CallMCPBodyParams.from_dict(_params)




        call_mcp_body = cls(
            jsonrpc=jsonrpc,
            method=method,
            id=id,
            params=params,
        )


        call_mcp_body.additional_properties = d
        return call_mcp_body

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
