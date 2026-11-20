from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.aikido_severity import AikidoSeverity
from ..models.aikido_severity import check_aikido_severity
from typing import cast






T = TypeVar("T", bound="LavaflowAikidoBinding")



@_attrs_define
class LavaflowAikidoBinding:
    """ The Aikido workspace a binding reports issues from. Present when `connector_type` is `aikido`.

        Attributes:
            workspace_name (str):
            min_severity (AikidoSeverity): An Aikido issue severity, lowest first.
     """

    workspace_name: str
    min_severity: AikidoSeverity
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        workspace_name = self.workspace_name

        min_severity: str = self.min_severity


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "workspace_name": workspace_name,
            "min_severity": min_severity,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        workspace_name = d.pop("workspace_name")

        min_severity = check_aikido_severity(d.pop("min_severity"))




        lavaflow_aikido_binding = cls(
            workspace_name=workspace_name,
            min_severity=min_severity,
        )


        lavaflow_aikido_binding.additional_properties = d
        return lavaflow_aikido_binding

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
