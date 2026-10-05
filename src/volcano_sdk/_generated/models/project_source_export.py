from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.project_source_export_omission import ProjectSourceExportOmission
  from ..models.project_source_export_skip import ProjectSourceExportSkip





T = TypeVar("T", bound="ProjectSourceExport")



@_attrs_define
class ProjectSourceExport:
    """ The initial production-branch commit, and everything export could not carry.

        Attributes:
            repo_full_name (str):
            branch (str): The production branch that was created.
            commit_sha (str):
            file_count (int):
            skipped (list[ProjectSourceExportSkip]): Resources whose source could not be taken, with the reason. Most often
                a resource that has never deployed successfully.
            omitted (list[ProjectSourceExportOmission]): Things deliberately left out of the branch.
     """

    repo_full_name: str
    branch: str
    commit_sha: str
    file_count: int
    skipped: list[ProjectSourceExportSkip]
    omitted: list[ProjectSourceExportOmission]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_source_export_omission import ProjectSourceExportOmission
        from ..models.project_source_export_skip import ProjectSourceExportSkip
        repo_full_name = self.repo_full_name

        branch = self.branch

        commit_sha = self.commit_sha

        file_count = self.file_count

        skipped = []
        for skipped_item_data in self.skipped:
            skipped_item = skipped_item_data.to_dict()
            skipped.append(skipped_item)



        omitted = []
        for omitted_item_data in self.omitted:
            omitted_item = omitted_item_data.to_dict()
            omitted.append(omitted_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "repo_full_name": repo_full_name,
            "branch": branch,
            "commit_sha": commit_sha,
            "file_count": file_count,
            "skipped": skipped,
            "omitted": omitted,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_source_export_omission import ProjectSourceExportOmission
        from ..models.project_source_export_skip import ProjectSourceExportSkip
        d = dict(src_dict)
        repo_full_name = d.pop("repo_full_name")

        branch = d.pop("branch")

        commit_sha = d.pop("commit_sha")

        file_count = d.pop("file_count")

        skipped = []
        _skipped = d.pop("skipped")
        for skipped_item_data in (_skipped):
            skipped_item = ProjectSourceExportSkip.from_dict(skipped_item_data)



            skipped.append(skipped_item)


        omitted = []
        _omitted = d.pop("omitted")
        for omitted_item_data in (_omitted):
            omitted_item = ProjectSourceExportOmission.from_dict(omitted_item_data)



            omitted.append(omitted_item)


        project_source_export = cls(
            repo_full_name=repo_full_name,
            branch=branch,
            commit_sha=commit_sha,
            file_count=file_count,
            skipped=skipped,
            omitted=omitted,
        )


        project_source_export.additional_properties = d
        return project_source_export

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
