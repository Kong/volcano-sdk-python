from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ShareVariable")



@_attrs_define
class ShareVariable:
    """ A project variable a deploy link's release declares. A project created from the link always gets it.

        Attributes:
            name (str): The variable's name.
            required (bool): Always true: a project created from the link always gets this variable,
                created empty when the visitor gives no value. It never means a value must
                be given.
            secret (bool): Whether to treat the value as a secret: take it masked and never show it back. Only a
                `NEXT_PUBLIC_` name, which a Next.js build copies into the browser, is not secret.
            unshared (bool | Unset): True when the source project gives the variable only to the scoped
                functions that declare it, not to every function, and so does a project
                made from the release. Omitted when false.
     """

    name: str
    required: bool
    secret: bool
    unshared: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        required = self.required

        secret = self.secret

        unshared = self.unshared


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "required": required,
            "secret": secret,
        })
        if unshared is not UNSET:
            field_dict["unshared"] = unshared

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        required = d.pop("required")

        secret = d.pop("secret")

        unshared = d.pop("unshared", UNSET)

        share_variable = cls(
            name=name,
            required=required,
            secret=secret,
            unshared=unshared,
        )


        share_variable.additional_properties = d
        return share_variable

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
