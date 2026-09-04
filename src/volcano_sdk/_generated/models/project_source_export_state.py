from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_source_export_state_mode import check_project_source_export_state_mode
from ..models.project_source_export_state_mode import ProjectSourceExportStateMode
from typing import cast
import datetime






T = TypeVar("T", bound="ProjectSourceExportState")



@_attrs_define
class ProjectSourceExportState:
    """ The project's source of truth and any pending Git transition.

        Attributes:
            mode (ProjectSourceExportStateMode):
            transition_started_at (datetime.datetime | None): When source export started, cleared if an incomplete
                transition is canceled.
            exported_at (datetime.datetime | None): When the initial export push entered deployment, or when a transition
                was canceled after its commit was reserved. Once set, the one-time export is consumed.
            handed_over_at (datetime.datetime | None): When a complete production-branch deployment first proved the
                repository could drive the project, null until then. Once set, the repository is the project's source of truth.
     """

    mode: ProjectSourceExportStateMode
    transition_started_at: datetime.datetime | None
    exported_at: datetime.datetime | None
    handed_over_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        mode: str = self.mode

        transition_started_at: None | str
        if isinstance(self.transition_started_at, datetime.datetime):
            transition_started_at = self.transition_started_at.isoformat()
        else:
            transition_started_at = self.transition_started_at

        exported_at: None | str
        if isinstance(self.exported_at, datetime.datetime):
            exported_at = self.exported_at.isoformat()
        else:
            exported_at = self.exported_at

        handed_over_at: None | str
        if isinstance(self.handed_over_at, datetime.datetime):
            handed_over_at = self.handed_over_at.isoformat()
        else:
            handed_over_at = self.handed_over_at


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "mode": mode,
            "transition_started_at": transition_started_at,
            "exported_at": exported_at,
            "handed_over_at": handed_over_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = check_project_source_export_state_mode(d.pop("mode"))




        def _parse_transition_started_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                transition_started_at_type_0 = datetime.datetime.fromisoformat(data)



                return transition_started_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        transition_started_at = _parse_transition_started_at(d.pop("transition_started_at"))


        def _parse_exported_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                exported_at_type_0 = datetime.datetime.fromisoformat(data)



                return exported_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        exported_at = _parse_exported_at(d.pop("exported_at"))


        def _parse_handed_over_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                handed_over_at_type_0 = datetime.datetime.fromisoformat(data)



                return handed_over_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        handed_over_at = _parse_handed_over_at(d.pop("handed_over_at"))


        project_source_export_state = cls(
            mode=mode,
            transition_started_at=transition_started_at,
            exported_at=exported_at,
            handed_over_at=handed_over_at,
        )


        project_source_export_state.additional_properties = d
        return project_source_export_state

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
