from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_config_apply_result_entry import ProjectConfigApplyResultEntry
  from ..models.project_config_apply_summary import ProjectConfigApplySummary
  from ..models.project_config_missing_resource import ProjectConfigMissingResource
  from ..models.project_config_skipped_resource import ProjectConfigSkippedResource





T = TypeVar("T", bound="ProjectConfigApplyResult")



@_attrs_define
class ProjectConfigApplyResult:
    """ Per-resource report for a project config apply (or dry run).

        Attributes:
            results (list[ProjectConfigApplyResultEntry]):
            skipped (list[ProjectConfigSkippedResource]): Manifest entries referencing functions, frontends, databases, or
                buckets that do not exist. Their configuration was not applied;
                deploy/create the resource first, then re-apply.
            missing (list[ProjectConfigMissingResource]): Existing functions, frontends, databases, or buckets that have no
                entry in the corresponding declared manifest section.
            summary (ProjectConfigApplySummary):
            dry_run (bool | Unset): True when the request was a dry run and no changes were made.
     """

    results: list[ProjectConfigApplyResultEntry]
    skipped: list[ProjectConfigSkippedResource]
    missing: list[ProjectConfigMissingResource]
    summary: ProjectConfigApplySummary
    dry_run: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_apply_result_entry import ProjectConfigApplyResultEntry
        from ..models.project_config_apply_summary import ProjectConfigApplySummary
        from ..models.project_config_missing_resource import ProjectConfigMissingResource
        from ..models.project_config_skipped_resource import ProjectConfigSkippedResource
        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)



        skipped = []
        for skipped_item_data in self.skipped:
            skipped_item = skipped_item_data.to_dict()
            skipped.append(skipped_item)



        missing = []
        for missing_item_data in self.missing:
            missing_item = missing_item_data.to_dict()
            missing.append(missing_item)



        summary = self.summary.to_dict()

        dry_run = self.dry_run


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "results": results,
            "skipped": skipped,
            "missing": missing,
            "summary": summary,
        })
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_apply_result_entry import ProjectConfigApplyResultEntry
        from ..models.project_config_apply_summary import ProjectConfigApplySummary
        from ..models.project_config_missing_resource import ProjectConfigMissingResource
        from ..models.project_config_skipped_resource import ProjectConfigSkippedResource
        d = dict(src_dict)
        results = []
        _results = d.pop("results")
        for results_item_data in (_results):
            results_item = ProjectConfigApplyResultEntry.from_dict(results_item_data)



            results.append(results_item)


        skipped = []
        _skipped = d.pop("skipped")
        for skipped_item_data in (_skipped):
            skipped_item = ProjectConfigSkippedResource.from_dict(skipped_item_data)



            skipped.append(skipped_item)


        missing = []
        _missing = d.pop("missing")
        for missing_item_data in (_missing):
            missing_item = ProjectConfigMissingResource.from_dict(missing_item_data)



            missing.append(missing_item)


        summary = ProjectConfigApplySummary.from_dict(d.pop("summary"))




        dry_run = d.pop("dry_run", UNSET)

        project_config_apply_result = cls(
            results=results,
            skipped=skipped,
            missing=missing,
            summary=summary,
            dry_run=dry_run,
        )


        project_config_apply_result.additional_properties = d
        return project_config_apply_result

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
