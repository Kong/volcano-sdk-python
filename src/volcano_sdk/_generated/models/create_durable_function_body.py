from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field
import json
from .. import types

from ..types import UNSET, Unset

from ..models.create_durable_function_body_runtime import check_create_durable_function_body_runtime
from ..models.create_durable_function_body_runtime import CreateDurableFunctionBodyRuntime
from ..models.create_durable_function_body_variable_scope import check_create_durable_function_body_variable_scope
from ..models.create_durable_function_body_variable_scope import CreateDurableFunctionBodyVariableScope
from ..types import File, FileTypes
from ..types import UNSET, Unset
from io import BytesIO
from typing import cast






T = TypeVar("T", bound="CreateDurableFunctionBody")



@_attrs_define
class CreateDurableFunctionBody:
    """ 
        Attributes:
            name (str): DNS-safe function name (lowercase letters, numbers, hyphens; cannot start or end with hyphen)
                Example: order-pipeline.
            code (File): ZIP or tar.gz archive containing function source code plus dependency manifests/lockfiles.
            runtime (CreateDurableFunctionBodyRuntime): Runtime environment. Required. Durable execution needs the
                durable authoring API, which ships for the Node runtimes;
                any other runtime is rejected with 400 and the response
                names the ones that work.
                 Example: nodejs24.x.
            handler (str | Unset): The name of the function to invoke. Defaults to "handler" if not specified. Default:
                'handler'. Example: handler.
            is_public (bool | Unset): Whether anon keys with `functions.invoke` may start an
                execution. Redeploying is the only way to change it, since
                the collection has no update endpoint; omit it to keep the
                current visibility, and a new function starts private.

                The standard collection's synchronous invocation fields —
                `invocation_mode`, `http_auth_mode`, `openapi_spec` —
                configure a request path no durable route serves, and are
                rejected with 400 rather than ignored.
            variable_scope (CreateDurableFunctionBodyVariableScope | Unset): Which project variables this function receives.
                `all` (the default) gives it every project variable; `scoped` gives it only the variables it selects. Omitting
                this leaves an existing function's scope unchanged.
            variables (str | Unset): JSON-encoded array of project variable names this function requires, on top of the ones
                detected in its source. A declared name the project does not define is rejected with 400; a detected name it
                does not define is ignored. Only used when `variable_scope` is `scoped`. Omitting this leaves an existing
                function's declared names unchanged.
     """

    name: str
    code: File
    runtime: CreateDurableFunctionBodyRuntime
    handler: str | Unset = 'handler'
    is_public: bool | Unset = UNSET
    variable_scope: CreateDurableFunctionBodyVariableScope | Unset = UNSET
    variables: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        code = self.code.to_tuple()


        runtime: str = self.runtime

        handler = self.handler

        is_public = self.is_public

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




        runtime = check_create_durable_function_body_runtime(d.pop("runtime"))




        handler = d.pop("handler", UNSET)

        is_public = d.pop("is_public", UNSET)

        _variable_scope = d.pop("variable_scope", UNSET)
        variable_scope: CreateDurableFunctionBodyVariableScope | Unset
        if isinstance(_variable_scope,  Unset):
            variable_scope = UNSET
        else:
            variable_scope = check_create_durable_function_body_variable_scope(_variable_scope)




        variables = d.pop("variables", UNSET)

        create_durable_function_body = cls(
            name=name,
            code=code,
            runtime=runtime,
            handler=handler,
            is_public=is_public,
            variable_scope=variable_scope,
            variables=variables,
        )


        create_durable_function_body.additional_properties = d
        return create_durable_function_body

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
