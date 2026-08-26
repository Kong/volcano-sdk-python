from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field
import json
from .. import types

from ..types import UNSET, Unset

from ..types import File, FileTypes
from ..types import UNSET, Unset
from io import BytesIO






T = TypeVar("T", bound="CreateFunctionsBatchBody")



@_attrs_define
class CreateFunctionsBatchBody:
    """ 
        Attributes:
            functions (str): JSON array of functions with `name`, `runtime`, optional `handler`, and `file_field`. Each
                `file_field` must name a multipart file field containing that function's ZIP or tar.gz source bundle.
            code_0 (File | Unset): Function ZIP or tar.gz archive referenced by the first manifest entry's `file_field`;
                additional code_N file fields may be included. Each archive is subject to SOURCE_ARCHIVE_SIZE_LIMIT_MB.
     """

    functions: str
    code_0: File | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        functions = self.functions

        code_0: FileTypes | Unset = UNSET
        if not isinstance(self.code_0, Unset):
            code_0 = self.code_0.to_tuple()



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "functions": functions,
        })
        if code_0 is not UNSET:
            field_dict["code_0"] = code_0

        return field_dict


    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("functions", (None, str(self.functions).encode(), "text/plain")))



        if not isinstance(self.code_0, Unset):
            files.append(("code_0", self.code_0.to_tuple()))




        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))



        return files


    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        functions = d.pop("functions")

        _code_0 = d.pop("code_0", UNSET)
        code_0: File | Unset
        if isinstance(_code_0,  Unset):
            code_0 = UNSET
        else:
            code_0 = File(
             payload = BytesIO(_code_0)
        )




        create_functions_batch_body = cls(
            functions=functions,
            code_0=code_0,
        )


        create_functions_batch_body.additional_properties = d
        return create_functions_batch_body

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
