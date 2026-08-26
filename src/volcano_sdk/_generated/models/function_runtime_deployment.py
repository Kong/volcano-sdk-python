from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="FunctionRuntimeDeployment")



@_attrs_define
class FunctionRuntimeDeployment:
    """ 
        Attributes:
            file_extensions (list[str]): Source file extensions the CLI can use to detect this runtime. Example: ['.js',
                '.mjs'].
            entrypoint (str): Archive path the CLI should use for a single-file function source. Example: index.js.
            handler (str): Handler symbol the CLI should submit when deploying this runtime. Example: handler.
            dependency_manifests (list[str]): Dependency manifest files the CLI should include for hosted builds. Example:
                ['package.json', 'package-lock.json'].
     """

    file_extensions: list[str]
    entrypoint: str
    handler: str
    dependency_manifests: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        file_extensions = self.file_extensions



        entrypoint = self.entrypoint

        handler = self.handler

        dependency_manifests = self.dependency_manifests




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "file_extensions": file_extensions,
            "entrypoint": entrypoint,
            "handler": handler,
            "dependency_manifests": dependency_manifests,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_extensions = cast(list[str], d.pop("file_extensions"))


        entrypoint = d.pop("entrypoint")

        handler = d.pop("handler")

        dependency_manifests = cast(list[str], d.pop("dependency_manifests"))


        function_runtime_deployment = cls(
            file_extensions=file_extensions,
            entrypoint=entrypoint,
            handler=handler,
            dependency_manifests=dependency_manifests,
        )


        function_runtime_deployment.additional_properties = d
        return function_runtime_deployment

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
