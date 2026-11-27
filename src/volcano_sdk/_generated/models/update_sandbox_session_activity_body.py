from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.update_sandbox_session_activity_body_activity import UpdateSandboxSessionActivityBodyActivity





T = TypeVar("T", bound="UpdateSandboxSessionActivityBody")



@_attrs_define
class UpdateSandboxSessionActivityBody:
    """
        Attributes:
            activity (UpdateSandboxSessionActivityBodyActivity):
     """

    activity: UpdateSandboxSessionActivityBodyActivity





    def to_dict(self) -> dict[str, Any]:
        from ..models.update_sandbox_session_activity_body_activity import UpdateSandboxSessionActivityBodyActivity # noqa: PLC0415
        activity = self.activity.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "activity": activity,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_sandbox_session_activity_body_activity import UpdateSandboxSessionActivityBodyActivity # noqa: PLC0415
        d = dict(src_dict)
        activity = UpdateSandboxSessionActivityBodyActivity.from_dict(d.pop("activity"))




        update_sandbox_session_activity_body = cls(
            activity=activity,
        )

        return update_sandbox_session_activity_body
