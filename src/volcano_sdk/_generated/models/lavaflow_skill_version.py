from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.lavaflow_skill_applies_to import LavaflowSkillAppliesTo
  from ..models.lavaflow_skill_citation import LavaflowSkillCitation
  from ..models.lavaflow_skill_source import LavaflowSkillSource





T = TypeVar("T", bound="LavaflowSkillVersion")



@_attrs_define
class LavaflowSkillVersion:
    """ 
        Attributes:
            skill_id (UUID):
            project_id (UUID):
            version (int):
            description (str):
            body (str):
            applies_to (LavaflowSkillAppliesTo): Where a skill applies. Empty lists apply it to the whole project.
            citations (list[LavaflowSkillCitation]):
            content_sha256 (str):
            source (LavaflowSkillSource): Where a version came from: a writer's act on a fix's pull request, or the owner's
                edit.
            created_at (datetime.datetime):
     """

    skill_id: UUID
    project_id: UUID
    version: int
    description: str
    body: str
    applies_to: LavaflowSkillAppliesTo
    citations: list[LavaflowSkillCitation]
    content_sha256: str
    source: LavaflowSkillSource
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_skill_applies_to import LavaflowSkillAppliesTo # noqa: PLC0415
        from ..models.lavaflow_skill_citation import LavaflowSkillCitation # noqa: PLC0415
        from ..models.lavaflow_skill_source import LavaflowSkillSource # noqa: PLC0415
        skill_id = str(self.skill_id)

        project_id = str(self.project_id)

        version = self.version

        description = self.description

        body = self.body

        applies_to = self.applies_to.to_dict()

        citations = []
        for citations_item_data in self.citations:
            citations_item = citations_item_data.to_dict()
            citations.append(citations_item)



        content_sha256 = self.content_sha256

        source = self.source.to_dict()

        created_at = self.created_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "skill_id": skill_id,
            "project_id": project_id,
            "version": version,
            "description": description,
            "body": body,
            "applies_to": applies_to,
            "citations": citations,
            "content_sha256": content_sha256,
            "source": source,
            "created_at": created_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_skill_applies_to import LavaflowSkillAppliesTo # noqa: PLC0415
        from ..models.lavaflow_skill_citation import LavaflowSkillCitation # noqa: PLC0415
        from ..models.lavaflow_skill_source import LavaflowSkillSource # noqa: PLC0415
        d = dict(src_dict)
        skill_id = UUID(d.pop("skill_id"))




        project_id = UUID(d.pop("project_id"))




        version = d.pop("version")

        description = d.pop("description")

        body = d.pop("body")

        applies_to = LavaflowSkillAppliesTo.from_dict(d.pop("applies_to"))




        citations = []
        _citations = d.pop("citations")
        for citations_item_data in (_citations):
            citations_item = LavaflowSkillCitation.from_dict(citations_item_data)



            citations.append(citations_item)


        content_sha256 = d.pop("content_sha256")

        source = LavaflowSkillSource.from_dict(d.pop("source"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        lavaflow_skill_version = cls(
            skill_id=skill_id,
            project_id=project_id,
            version=version,
            description=description,
            body=body,
            applies_to=applies_to,
            citations=citations,
            content_sha256=content_sha256,
            source=source,
            created_at=created_at,
        )


        lavaflow_skill_version.additional_properties = d
        return lavaflow_skill_version

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
