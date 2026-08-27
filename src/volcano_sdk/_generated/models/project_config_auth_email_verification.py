from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ProjectConfigAuthEmailVerification")



@_attrs_define
class ProjectConfigAuthEmailVerification:
    """ 
        Attributes:
            require_confirmation (bool | Unset): Require users to confirm email before sign-in. Requires email sending to be
                enabled.
            confirmation_timeout (int | Unset): Email confirmation token expiry in seconds
     """

    require_confirmation: bool | Unset = UNSET
    confirmation_timeout: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        require_confirmation = self.require_confirmation

        confirmation_timeout = self.confirmation_timeout


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if require_confirmation is not UNSET:
            field_dict["require_confirmation"] = require_confirmation
        if confirmation_timeout is not UNSET:
            field_dict["confirmation_timeout"] = confirmation_timeout

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        require_confirmation = d.pop("require_confirmation", UNSET)

        confirmation_timeout = d.pop("confirmation_timeout", UNSET)

        project_config_auth_email_verification = cls(
            require_confirmation=require_confirmation,
            confirmation_timeout=confirmation_timeout,
        )

        return project_config_auth_email_verification

