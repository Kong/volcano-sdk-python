from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ProjectConfigAuthSessions")



@_attrs_define
class ProjectConfigAuthSessions:
    """ 
        Attributes:
            inactivity_timeout (int | Unset): Force re-login after inactivity (seconds, 0=never)
            max_session_duration (int | Unset): Force re-login after duration (seconds, 0=never)
     """

    inactivity_timeout: int | Unset = UNSET
    max_session_duration: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        inactivity_timeout = self.inactivity_timeout

        max_session_duration = self.max_session_duration


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if inactivity_timeout is not UNSET:
            field_dict["inactivity_timeout"] = inactivity_timeout
        if max_session_duration is not UNSET:
            field_dict["max_session_duration"] = max_session_duration

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        inactivity_timeout = d.pop("inactivity_timeout", UNSET)

        max_session_duration = d.pop("max_session_duration", UNSET)

        project_config_auth_sessions = cls(
            inactivity_timeout=inactivity_timeout,
            max_session_duration=max_session_duration,
        )

        return project_config_auth_sessions

