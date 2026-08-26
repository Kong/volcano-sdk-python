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
     """

    name: str
    code: File
    runtime: CreateFunctionBodyRuntime
    handler: str | Unset = 'handler'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        code = self.code.to_tuple()


        runtime: str = self.runtime

        handler = self.handler


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "code": code,
            "runtime": runtime,
        })
        if handler is not UNSET:
            field_dict["handler"] = handler

        return field_dict


    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("name", (None, str(self.name).encode(), "text/plain")))



        files.append(("code", self.code.to_tuple()))



        files.append(("runtime", (None, str(self.runtime).encode(), "text/plain")))



        if not isinstance(self.handler, Unset):
            files.append(("handler", (None, str(self.handler).encode(), "text/plain")))




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

        create_function_body = cls(
            name=name,
            code=code,
            runtime=runtime,
            handler=handler,
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
