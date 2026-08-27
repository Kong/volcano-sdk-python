from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ProjectConfigAuthPasswordReset")



@_attrs_define
class ProjectConfigAuthPasswordReset:
    """ 
        Attributes:
            allow (bool | Unset):
            timeout (int | Unset): Password reset token expiry in seconds
            max_history (int | Unset): Number of previous passwords to disallow (0=disabled)
     """

    allow: bool | Unset = UNSET
    timeout: int | Unset = UNSET
    max_history: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        allow = self.allow

        timeout = self.timeout

        max_history = self.max_history


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if allow is not UNSET:
            field_dict["allow"] = allow
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if max_history is not UNSET:
            field_dict["max_history"] = max_history

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        allow = d.pop("allow", UNSET)

        timeout = d.pop("timeout", UNSET)

        max_history = d.pop("max_history", UNSET)

        project_config_auth_password_reset = cls(
            allow=allow,
            timeout=timeout,
            max_history=max_history,
        )

        return project_config_auth_password_reset

