from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.function_runtime_deployment import FunctionRuntimeDeployment





T = TypeVar("T", bound="FunctionRuntimeOption")



@_attrs_define
class FunctionRuntimeOption:
    """ 
        Attributes:
            name (str): Runtime identifier accepted by function APIs. Example: nodejs24.x.
            language (str): Runtime language family used by the CLI to choose defaults from source files. Example: nodejs.
            default (bool): Whether this runtime is the CLI default for its language.
            deployment (FunctionRuntimeDeployment):
     """

    name: str
    language: str
    default: bool
    deployment: FunctionRuntimeDeployment
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.function_runtime_deployment import FunctionRuntimeDeployment
        name = self.name

        language = self.language

        default = self.default

        deployment = self.deployment.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "language": language,
            "default": default,
            "deployment": deployment,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.function_runtime_deployment import FunctionRuntimeDeployment
        d = dict(src_dict)
        name = d.pop("name")

        language = d.pop("language")

        default = d.pop("default")

        deployment = FunctionRuntimeDeployment.from_dict(d.pop("deployment"))




        function_runtime_option = cls(
            name=name,
            language=language,
            default=default,
            deployment=deployment,
        )


        function_runtime_option.additional_properties = d
        return function_runtime_option

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
