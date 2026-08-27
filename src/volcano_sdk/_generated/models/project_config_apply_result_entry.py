from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_config_apply_result_entry_action import check_project_config_apply_result_entry_action
from ..models.project_config_apply_result_entry_action import ProjectConfigApplyResultEntryAction
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProjectConfigApplyResultEntry")



@_attrs_define
class ProjectConfigApplyResultEntry:
    """ 
        Attributes:
            section (str): Manifest section the entry belongs to (e.g. variables, buckets, auth.providers.oauth).
            action (ProjectConfigApplyResultEntryAction):
            name (str | Unset): Resource name or key within the section. Empty for singleton sections.
            error (str | Unset): Error detail when action is `error`.
            notice (str | Unset): Optional operational note (e.g. disabling realtime drops active connections).
     """

    section: str
    action: ProjectConfigApplyResultEntryAction
    name: str | Unset = UNSET
    error: str | Unset = UNSET
    notice: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        section = self.section

        action: str = self.action

        name = self.name

        error = self.error

        notice = self.notice


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "section": section,
            "action": action,
        })
        if name is not UNSET:
            field_dict["name"] = name
        if error is not UNSET:
            field_dict["error"] = error
        if notice is not UNSET:
            field_dict["notice"] = notice

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        section = d.pop("section")

        action = check_project_config_apply_result_entry_action(d.pop("action"))




        name = d.pop("name", UNSET)

        error = d.pop("error", UNSET)

        notice = d.pop("notice", UNSET)

        project_config_apply_result_entry = cls(
            section=section,
            action=action,
            name=name,
            error=error,
            notice=notice,
        )


        project_config_apply_result_entry.additional_properties = d
        return project_config_apply_result_entry

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
