from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.import_provider import check_import_provider
from ..models.import_provider import ImportProvider
from ..models.project_import_readiness import check_project_import_readiness
from ..models.project_import_readiness import ProjectImportReadiness
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.import_source import ImportSource
  from ..models.project_import_action import ProjectImportAction
  from ..models.project_import_destination import ProjectImportDestination
  from ..models.project_import_finding import ProjectImportFinding
  from ..models.project_import_summary import ProjectImportSummary





T = TypeVar("T", bound="ProjectImportReport")



@_attrs_define
class ProjectImportReport:
    """ 
        Attributes:
            schema_version (str):
            provider (ImportProvider):
            source (ImportSource):
            destination (ProjectImportDestination):
            actions (list[ProjectImportAction]):
            findings (list[ProjectImportFinding]):
            summary (ProjectImportSummary):
            readiness (ProjectImportReadiness):
            source_fingerprint (str):
            capability_fingerprint (str):
            fingerprint (str):
            generated_at (datetime.datetime):
     """

    schema_version: str
    provider: ImportProvider
    source: ImportSource
    destination: ProjectImportDestination
    actions: list[ProjectImportAction]
    findings: list[ProjectImportFinding]
    summary: ProjectImportSummary
    readiness: ProjectImportReadiness
    source_fingerprint: str
    capability_fingerprint: str
    fingerprint: str
    generated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.import_source import ImportSource
        from ..models.project_import_action import ProjectImportAction
        from ..models.project_import_destination import ProjectImportDestination
        from ..models.project_import_finding import ProjectImportFinding
        from ..models.project_import_summary import ProjectImportSummary
        schema_version = self.schema_version

        provider: str = self.provider

        source = self.source.to_dict()

        destination = self.destination.to_dict()

        actions = []
        for actions_item_data in self.actions:
            actions_item = actions_item_data.to_dict()
            actions.append(actions_item)



        findings = []
        for findings_item_data in self.findings:
            findings_item = findings_item_data.to_dict()
            findings.append(findings_item)



        summary = self.summary.to_dict()

        readiness: str = self.readiness

        source_fingerprint = self.source_fingerprint

        capability_fingerprint = self.capability_fingerprint

        fingerprint = self.fingerprint

        generated_at = self.generated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "schema_version": schema_version,
            "provider": provider,
            "source": source,
            "destination": destination,
            "actions": actions,
            "findings": findings,
            "summary": summary,
            "readiness": readiness,
            "source_fingerprint": source_fingerprint,
            "capability_fingerprint": capability_fingerprint,
            "fingerprint": fingerprint,
            "generated_at": generated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.import_source import ImportSource
        from ..models.project_import_action import ProjectImportAction
        from ..models.project_import_destination import ProjectImportDestination
        from ..models.project_import_finding import ProjectImportFinding
        from ..models.project_import_summary import ProjectImportSummary
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        provider = check_import_provider(d.pop("provider"))




        source = ImportSource.from_dict(d.pop("source"))




        destination = ProjectImportDestination.from_dict(d.pop("destination"))




        actions = []
        _actions = d.pop("actions")
        for actions_item_data in (_actions):
            actions_item = ProjectImportAction.from_dict(actions_item_data)



            actions.append(actions_item)


        findings = []
        _findings = d.pop("findings")
        for findings_item_data in (_findings):
            findings_item = ProjectImportFinding.from_dict(findings_item_data)



            findings.append(findings_item)


        summary = ProjectImportSummary.from_dict(d.pop("summary"))




        readiness = check_project_import_readiness(d.pop("readiness"))




        source_fingerprint = d.pop("source_fingerprint")

        capability_fingerprint = d.pop("capability_fingerprint")

        fingerprint = d.pop("fingerprint")

        generated_at = datetime.datetime.fromisoformat(d.pop("generated_at"))




        project_import_report = cls(
            schema_version=schema_version,
            provider=provider,
            source=source,
            destination=destination,
            actions=actions,
            findings=findings,
            summary=summary,
            readiness=readiness,
            source_fingerprint=source_fingerprint,
            capability_fingerprint=capability_fingerprint,
            fingerprint=fingerprint,
            generated_at=generated_at,
        )


        project_import_report.additional_properties = d
        return project_import_report

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
