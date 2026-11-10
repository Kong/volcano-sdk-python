from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_skill_scope import check_lavaflow_skill_scope
from ..models.lavaflow_skill_scope import LavaflowSkillScope
from typing import cast

if TYPE_CHECKING:
  from ..models.lavaflow_global_skill_applies_to import LavaflowGlobalSkillAppliesTo





T = TypeVar("T", bound="LavaflowGlobalSkill")



@_attrs_define
class LavaflowGlobalSkill:
    """ A skill Volcano wrote for every project. It holds no customer content.

        Attributes:
            scope (LavaflowSkillScope): `project` skills belong to this project and never leave it. `volcano` skills are
                written by Volcano for every project.
            name (str): Runs list it as `volcano:<name>`.
            description (str):
            body (str):
            applies_to (LavaflowGlobalSkillAppliesTo): Where a global skill applies. Empty lists apply it to every project.
            content_sha256 (str): The hash of the skill's file, which identifies its version.
     """

    scope: LavaflowSkillScope
    name: str
    description: str
    body: str
    applies_to: LavaflowGlobalSkillAppliesTo
    content_sha256: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_global_skill_applies_to import LavaflowGlobalSkillAppliesTo # noqa: PLC0415
        scope: str = self.scope

        name = self.name

        description = self.description

        body = self.body

        applies_to = self.applies_to.to_dict()

        content_sha256 = self.content_sha256


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "scope": scope,
            "name": name,
            "description": description,
            "body": body,
            "applies_to": applies_to,
            "content_sha256": content_sha256,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_global_skill_applies_to import LavaflowGlobalSkillAppliesTo # noqa: PLC0415
        d = dict(src_dict)
        scope = check_lavaflow_skill_scope(d.pop("scope"))




        name = d.pop("name")

        description = d.pop("description")

        body = d.pop("body")

        applies_to = LavaflowGlobalSkillAppliesTo.from_dict(d.pop("applies_to"))




        content_sha256 = d.pop("content_sha256")

        lavaflow_global_skill = cls(
            scope=scope,
            name=name,
            description=description,
            body=body,
            applies_to=applies_to,
            content_sha256=content_sha256,
        )


        lavaflow_global_skill.additional_properties = d
        return lavaflow_global_skill

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
