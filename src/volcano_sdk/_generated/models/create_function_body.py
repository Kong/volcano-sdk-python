from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field
import json
from .. import types

from ..types import UNSET, Unset

from ..models.create_function_body_runtime import check_create_function_body_runtime
from ..models.create_function_body_runtime import CreateFunctionBodyRuntime
from ..models.create_function_body_variable_scope import check_create_function_body_variable_scope
from ..models.create_function_body_variable_scope import CreateFunctionBodyVariableScope
from ..models.function_http_auth_mode import check_function_http_auth_mode
from ..models.function_http_auth_mode import FunctionHTTPAuthMode
from ..models.function_invocation_mode import check_function_invocation_mode
from ..models.function_invocation_mode import FunctionInvocationMode
from ..types import File, FileTypes
from ..types import UNSET, Unset
from io import BytesIO
from typing import cast






T = TypeVar("T", bound="CreateFunctionBody")



@_attrs_define
class CreateFunctionBody:
    """ 
        Attributes:
            name (str): DNS-safe function name (lowercase letters, numbers, hyphens; cannot start or end with hyphen)
                Example: my-api-function.
            code (File): ZIP or tar.gz archive containing function source code plus dependency manifests/lockfiles. The API
                enforces SOURCE_ARCHIVE_SIZE_LIMIT_MB and stores a normalized tar.gz source archive.
            runtime (CreateFunctionBodyRuntime): Runtime environment. Required.
                - Node.js: nodejs22.x, nodejs24.x
                - Python: python3.10, python3.11, python3.12, python3.13, python3.14
                - Ruby: ruby3.3, ruby3.4, ruby4.0
                 Example: nodejs24.x.
            handler (str | Unset): The name of the function to invoke. Defaults to "handler" if not specified.
                Your code must export/define a function with this name:
                - Node.js: exports.handler (in index.js)
                - Python: def handler() (in main.py)
                - Ruby: def handler() (in main.rb)
                 Default: 'handler'. Example: handler.
            is_public (bool | Unset): Whether the function can be reached through public invocation ingress. Default: False.
            invocation_mode (FunctionInvocationMode | Unset): Invocation contract. `rpc` preserves the existing POST
                `{payload: ...}` contract;
                `http` forwards HTTP request semantics to the function runtime.
            http_auth_mode (FunctionHTTPAuthMode | Unset): Authentication applied by the HTTP ingress. `none` is valid only
                for public
                HTTP-mode functions and is intended for externally signed webhooks.
            openapi_spec (str | Unset): JSON-encoded OpenAPI 3.0 or 3.1 metadata for an HTTP-mode function.
            variable_scope (CreateFunctionBodyVariableScope | Unset): Which project variables this function receives. `all`
                (the default) gives it only project variables marked `shared: true`; `scoped` gives it only the variables it
                selects. Omitting this leaves an existing function's scope unchanged.
            variables (str | Unset): JSON-encoded array of project variable names this function requires, on top of the ones
                detected in its source. A declared name the project does not define is rejected with 400; a detected name it
                does not define is ignored. Only used when `variable_scope` is `scoped`. Omitting this leaves an existing
                function's declared names unchanged.
     """

    name: str
    code: File
    runtime: CreateFunctionBodyRuntime
    handler: str | Unset = 'handler'
    is_public: bool | Unset = False
    invocation_mode: FunctionInvocationMode | Unset = UNSET
    http_auth_mode: FunctionHTTPAuthMode | Unset = UNSET
    openapi_spec: str | Unset = UNSET
    variable_scope: CreateFunctionBodyVariableScope | Unset = UNSET
    variables: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        code = self.code.to_tuple()


        runtime: str = self.runtime

        handler = self.handler

        is_public = self.is_public

        invocation_mode: str | Unset = UNSET
        if not isinstance(self.invocation_mode, Unset):
            invocation_mode = self.invocation_mode


        http_auth_mode: str | Unset = UNSET
        if not isinstance(self.http_auth_mode, Unset):
            http_auth_mode = self.http_auth_mode


        openapi_spec = self.openapi_spec

        variable_scope: str | Unset = UNSET
        if not isinstance(self.variable_scope, Unset):
            variable_scope = self.variable_scope


        variables = self.variables


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "code": code,
            "runtime": runtime,
        })
        if handler is not UNSET:
            field_dict["handler"] = handler
        if is_public is not UNSET:
            field_dict["is_public"] = is_public
        if invocation_mode is not UNSET:
            field_dict["invocation_mode"] = invocation_mode
        if http_auth_mode is not UNSET:
            field_dict["http_auth_mode"] = http_auth_mode
        if openapi_spec is not UNSET:
            field_dict["openapi_spec"] = openapi_spec
        if variable_scope is not UNSET:
            field_dict["variable_scope"] = variable_scope
        if variables is not UNSET:
            field_dict["variables"] = variables

        return field_dict


    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("name", (None, str(self.name).encode(), "text/plain")))



        files.append(("code", self.code.to_tuple()))



        files.append(("runtime", (None, str(self.runtime).encode(), "text/plain")))



        if not isinstance(self.handler, Unset):
            files.append(("handler", (None, str(self.handler).encode(), "text/plain")))



        if not isinstance(self.is_public, Unset):
            files.append(("is_public", (None, str(self.is_public).encode(), "text/plain")))



        if not isinstance(self.invocation_mode, Unset):
            files.append(("invocation_mode", (None, str(self.invocation_mode).encode(), "text/plain")))



        if not isinstance(self.http_auth_mode, Unset):
            files.append(("http_auth_mode", (None, str(self.http_auth_mode).encode(), "text/plain")))



        if not isinstance(self.openapi_spec, Unset):
            files.append(("openapi_spec", (None, str(self.openapi_spec).encode(), "text/plain")))



        if not isinstance(self.variable_scope, Unset):
            files.append(("variable_scope", (None, str(self.variable_scope).encode(), "text/plain")))



        if not isinstance(self.variables, Unset):
            files.append(("variables", (None, str(self.variables).encode(), "text/plain")))




        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))



        return files


    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        code = File(
             payload = BytesIO(d.pop("code"))
        )




        runtime = check_create_function_body_runtime(d.pop("runtime"))




        handler = d.pop("handler", UNSET)

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




        openapi_spec = d.pop("openapi_spec", UNSET)

        _variable_scope = d.pop("variable_scope", UNSET)
        variable_scope: CreateFunctionBodyVariableScope | Unset
        if isinstance(_variable_scope,  Unset):
            variable_scope = UNSET
        else:
            variable_scope = check_create_function_body_variable_scope(_variable_scope)




        variables = d.pop("variables", UNSET)

        create_function_body = cls(
            name=name,
            code=code,
            runtime=runtime,
            handler=handler,
            is_public=is_public,
            invocation_mode=invocation_mode,
            http_auth_mode=http_auth_mode,
            openapi_spec=openapi_spec,
            variable_scope=variable_scope,
            variables=variables,
        )


        create_function_body.additional_properties = d
        return create_function_body

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
