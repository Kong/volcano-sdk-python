from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_skill_update_status import check_lavaflow_skill_update_status
from ..models.lavaflow_skill_update_status import LavaflowSkillUpdateStatus
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.lavaflow_skill_applies_to_update import LavaflowSkillAppliesToUpdate





T = TypeVar("T", bound="LavaflowSkillUpdate")



@_attrs_define
class LavaflowSkillUpdate:
    """ The fields to change. An omitted field keeps its value.

        Attributes:
            description (str | Unset):
            body (str | Unset):
            applies_to (LavaflowSkillAppliesToUpdate | Unset): The members of `applies_to` to change. An omitted member
                keeps its value, and a list you send replaces it, so `[]` clears it.
            status (LavaflowSkillUpdateStatus | Unset): `active` activates a proposed skill or restores a retired one.
                `retired` retires it.
     """

    description: str | Unset = UNSET
    body: str | Unset = UNSET
    applies_to: LavaflowSkillAppliesToUpdate | Unset = UNSET
    status: LavaflowSkillUpdateStatus | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_skill_applies_to_update import LavaflowSkillAppliesToUpdate # noqa: PLC0415
        description = self.description

        body = self.body

        applies_to: dict[str, Any] | Unset = UNSET
        if not isinstance(self.applies_to, Unset):
            applies_to = self.applies_to.to_dict()

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status



        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if description is not UNSET:
            field_dict["description"] = description
        if body is not UNSET:
            field_dict["body"] = body
        if applies_to is not UNSET:
            field_dict["applies_to"] = applies_to
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_skill_applies_to_update import LavaflowSkillAppliesToUpdate # noqa: PLC0415
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        body = d.pop("body", UNSET)

        _applies_to = d.pop("applies_to", UNSET)
        applies_to: LavaflowSkillAppliesToUpdate | Unset
        if isinstance(_applies_to,  Unset):
            applies_to = UNSET
        else:
            applies_to = LavaflowSkillAppliesToUpdate.from_dict(_applies_to)




        _status = d.pop("status", UNSET)
        status: LavaflowSkillUpdateStatus | Unset
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = check_lavaflow_skill_update_status(_status)




        lavaflow_skill_update = cls(
            description=description,
            body=body,
            applies_to=applies_to,
            status=status,
        )

        return lavaflow_skill_update

