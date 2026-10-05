from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.function_http_auth_mode import check_function_http_auth_mode
from ..models.function_http_auth_mode import FunctionHTTPAuthMode
from ..models.function_invocation_mode import check_function_invocation_mode
from ..models.function_invocation_mode import FunctionInvocationMode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.update_function_request_openapi_spec_type_0 import UpdateFunctionRequestOpenapiSpecType0





T = TypeVar("T", bound="UpdateFunctionRequest")



@_attrs_define
class UpdateFunctionRequest:
    """ 
        Attributes:
            is_public (bool | Unset): Function visibility for anon-key invocation.
                - `false` (default): private function
                - `true`: public function (anon keys with `functions.invoke` can invoke)
            invocation_mode (FunctionInvocationMode | Unset): Invocation contract. `rpc` preserves the existing POST
                `{payload: ...}` contract;
                `http` forwards HTTP request semantics to the function runtime.
            http_auth_mode (FunctionHTTPAuthMode | Unset): Authentication applied by the HTTP ingress. `none` is valid only
                for public
                HTTP-mode functions and is intended for externally signed webhooks.
            openapi_spec (None | Unset | UpdateFunctionRequestOpenapiSpecType0): OpenAPI 3.0 or 3.1 metadata for HTTP mode.
                Send null to clear it.
     """

    is_public: bool | Unset = UNSET
    invocation_mode: FunctionInvocationMode | Unset = UNSET
    http_auth_mode: FunctionHTTPAuthMode | Unset = UNSET
    openapi_spec: None | Unset | UpdateFunctionRequestOpenapiSpecType0 = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.update_function_request_openapi_spec_type_0 import UpdateFunctionRequestOpenapiSpecType0
        is_public = self.is_public

        invocation_mode: str | Unset = UNSET
        if not isinstance(self.invocation_mode, Unset):
            invocation_mode = self.invocation_mode


        http_auth_mode: str | Unset = UNSET
        if not isinstance(self.http_auth_mode, Unset):
            http_auth_mode = self.http_auth_mode


        openapi_spec: dict[str, Any] | None | Unset
        if isinstance(self.openapi_spec, Unset):
            openapi_spec = UNSET
        elif isinstance(self.openapi_spec, UpdateFunctionRequestOpenapiSpecType0):
            openapi_spec = self.openapi_spec.to_dict()
        else:
            openapi_spec = self.openapi_spec


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if is_public is not UNSET:
            field_dict["is_public"] = is_public
        if invocation_mode is not UNSET:
            field_dict["invocation_mode"] = invocation_mode
        if http_auth_mode is not UNSET:
            field_dict["http_auth_mode"] = http_auth_mode
        if openapi_spec is not UNSET:
            field_dict["openapi_spec"] = openapi_spec

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_function_request_openapi_spec_type_0 import UpdateFunctionRequestOpenapiSpecType0
        d = dict(src_dict)
        is_public = d.pop("is_public", UNSET)

        _invocation_mode = d.pop("invocation_mode", UNSET)
        invocation_mode: FunctionInvocationMode | Unset
        if isinstance(_invocation_mode,  Unset):
            invocation_mode = UNSET
        else:
            invocation_mode = check_function_invocation_mode(_invocation_mode)




        _http_auth_mode = d.pop("http_auth_mode", UNSET)
        http_auth_mode: FunctionHTTPAuthMode | Unset
        if isinstance(_http_auth_mode,  Unset):
            http_auth_mode = UNSET
        else:
            http_auth_mode = check_function_http_auth_mode(_http_auth_mode)




        def _parse_openapi_spec(data: object) -> None | Unset | UpdateFunctionRequestOpenapiSpecType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                openapi_spec_type_0 = UpdateFunctionRequestOpenapiSpecType0.from_dict(data)



                return openapi_spec_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UpdateFunctionRequestOpenapiSpecType0, data)

        openapi_spec = _parse_openapi_spec(d.pop("openapi_spec", UNSET))


        update_function_request = cls(
            is_public=is_public,
            invocation_mode=invocation_mode,
            http_auth_mode=http_auth_mode,
            openapi_spec=openapi_spec,
        )

        return update_function_request

