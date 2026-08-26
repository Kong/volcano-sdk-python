from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProjectConfigAuthCORS")



@_attrs_define
class ProjectConfigAuthCORS:
    """ 
        Attributes:
            enabled (bool | Unset):
            allowed_origins (list[str] | Unset):
            allow_credentials (bool | Unset):
            max_age (int | Unset):
     """

    enabled: bool | Unset = UNSET
    allowed_origins: list[str] | Unset = UNSET
    allow_credentials: bool | Unset = UNSET
    max_age: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        allowed_origins: list[str] | Unset = UNSET
        if not isinstance(self.allowed_origins, Unset):
            allowed_origins = self.allowed_origins



        allow_credentials = self.allow_credentials

        max_age = self.max_age


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if allowed_origins is not UNSET:
            field_dict["allowed_origins"] = allowed_origins
        if allow_credentials is not UNSET:
            field_dict["allow_credentials"] = allow_credentials
        if max_age is not UNSET:
            field_dict["max_age"] = max_age

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        allowed_origins = cast(list[str], d.pop("allowed_origins", UNSET))


        allow_credentials = d.pop("allow_credentials", UNSET)

        max_age = d.pop("max_age", UNSET)

        project_config_auth_cors = cls(
            enabled=enabled,
            allowed_origins=allowed_origins,
            allow_credentials=allow_credentials,
            max_age=max_age,
        )

        return project_config_auth_cors

