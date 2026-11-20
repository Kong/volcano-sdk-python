from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_skill_retired_reason import check_lavaflow_skill_retired_reason
from ..models.lavaflow_skill_retired_reason import LavaflowSkillRetiredReason
from ..models.lavaflow_skill_scope import check_lavaflow_skill_scope
from ..models.lavaflow_skill_scope import LavaflowSkillScope
from ..models.lavaflow_skill_status import check_lavaflow_skill_status
from ..models.lavaflow_skill_status import LavaflowSkillStatus
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.lavaflow_skill_applies_to import LavaflowSkillAppliesTo
  from ..models.lavaflow_skill_citation import LavaflowSkillCitation
  from ..models.lavaflow_skill_counts import LavaflowSkillCounts
  from ..models.lavaflow_skill_source import LavaflowSkillSource





T = TypeVar("T", bound="LavaflowSkill")



@_attrs_define
class LavaflowSkill:
    """ A project skill with its active version.

        Attributes:
            id (UUID):
            project_id (UUID):
            scope (LavaflowSkillScope): `project` skills belong to this project and never leave it. `volcano` skills are
                written by Volcano for every project.
            name (str): Unique in the project.
            status (LavaflowSkillStatus): `proposed` waits for the owner to activate it. `active` is in force. `retired` is
                set aside and can be restored.
            retired_reason (LavaflowSkillRetiredReason | None): Why it retired, null unless `status` is `retired`.
            version (int): The active version.
            description (str): When the skill applies.
            body (str): Markdown, at most 2 KiB.
            applies_to (LavaflowSkillAppliesTo): Where a skill applies. Empty lists apply it to the whole project.
            citations (list[LavaflowSkillCitation]):
            content_sha256 (str): The hash of the active version's text, as a run records it.
            source (LavaflowSkillSource): Where a version came from: a writer's act on a fix's pull request, or the owner's
                edit.
            counts (LavaflowSkillCounts):
            last_used_at (datetime.datetime | None):
            last_renewed_at (datetime.datetime): When the skill was created, or last renewed by the owner's edit, activation
                or restore.
            retired_at (datetime.datetime | None):
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
     """

    id: UUID
    project_id: UUID
    scope: LavaflowSkillScope
    name: str
    status: LavaflowSkillStatus
    retired_reason: LavaflowSkillRetiredReason | None
    version: int
    description: str
    body: str
    applies_to: LavaflowSkillAppliesTo
    citations: list[LavaflowSkillCitation]
    content_sha256: str
    source: LavaflowSkillSource
    counts: LavaflowSkillCounts
    last_used_at: datetime.datetime | None
    last_renewed_at: datetime.datetime
    retired_at: datetime.datetime | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_skill_applies_to import LavaflowSkillAppliesTo # noqa: PLC0415
        from ..models.lavaflow_skill_citation import LavaflowSkillCitation # noqa: PLC0415
        from ..models.lavaflow_skill_counts import LavaflowSkillCounts # noqa: PLC0415
        from ..models.lavaflow_skill_source import LavaflowSkillSource # noqa: PLC0415
        id = str(self.id)

        project_id = str(self.project_id)

        scope: str = self.scope

        name = self.name

        status: str = self.status

        retired_reason: None | str
        if isinstance(self.retired_reason, str):
            retired_reason = self.retired_reason
        else:
            retired_reason = self.retired_reason

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

        counts = self.counts.to_dict()

        last_used_at: None | str
        if isinstance(self.last_used_at, datetime.datetime):
            last_used_at = self.last_used_at.isoformat()
        else:
            last_used_at = self.last_used_at

        last_renewed_at = self.last_renewed_at.isoformat()

        retired_at: None | str
        if isinstance(self.retired_at, datetime.datetime):
            retired_at = self.retired_at.isoformat()
        else:
            retired_at = self.retired_at

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "project_id": project_id,
            "scope": scope,
            "name": name,
            "status": status,
            "retired_reason": retired_reason,
            "version": version,
            "description": description,
            "body": body,
            "applies_to": applies_to,
            "citations": citations,
            "content_sha256": content_sha256,
            "source": source,
            "counts": counts,
            "last_used_at": last_used_at,
            "last_renewed_at": last_renewed_at,
            "retired_at": retired_at,
            "created_at": created_at,
            "updated_at": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_skill_applies_to import LavaflowSkillAppliesTo # noqa: PLC0415
        from ..models.lavaflow_skill_citation import LavaflowSkillCitation # noqa: PLC0415
        from ..models.lavaflow_skill_counts import LavaflowSkillCounts # noqa: PLC0415
        from ..models.lavaflow_skill_source import LavaflowSkillSource # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        scope = check_lavaflow_skill_scope(d.pop("scope"))




        name = d.pop("name")

        status = check_lavaflow_skill_status(d.pop("status"))




        def _parse_retired_reason(data: object) -> LavaflowSkillRetiredReason | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                retired_reason_type_1 = check_lavaflow_skill_retired_reason(data)



                return retired_reason_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowSkillRetiredReason | None, data)

        retired_reason = _parse_retired_reason(d.pop("retired_reason"))


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




        counts = LavaflowSkillCounts.from_dict(d.pop("counts"))




        def _parse_last_used_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_used_at_type_0 = datetime.datetime.fromisoformat(data)



                return last_used_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_used_at = _parse_last_used_at(d.pop("last_used_at"))


        last_renewed_at = datetime.datetime.fromisoformat(d.pop("last_renewed_at"))




        def _parse_retired_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                retired_at_type_0 = datetime.datetime.fromisoformat(data)



                return retired_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        retired_at = _parse_retired_at(d.pop("retired_at"))


        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        lavaflow_skill = cls(
            id=id,
            project_id=project_id,
            scope=scope,
            name=name,
            status=status,
            retired_reason=retired_reason,
            version=version,
            description=description,
            body=body,
            applies_to=applies_to,
            citations=citations,
            content_sha256=content_sha256,
            source=source,
            counts=counts,
            last_used_at=last_used_at,
            last_renewed_at=last_renewed_at,
            retired_at=retired_at,
            created_at=created_at,
            updated_at=updated_at,
        )


        lavaflow_skill.additional_properties = d
        return lavaflow_skill

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
