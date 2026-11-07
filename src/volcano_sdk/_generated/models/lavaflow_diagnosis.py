from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.lavaflow_log_line import LavaflowLogLine





T = TypeVar("T", bound="LavaflowDiagnosis")



@_attrs_define
class LavaflowDiagnosis:
    """ 
        Attributes:
            summary (str):
            root_cause (str):
            evidence (list[str]):
            log_lines (list[LavaflowLogLine]): Empty for now. `evidence` cites the log lines the diagnosis relies on.
     """

    summary: str
    root_cause: str
    evidence: list[str]
    log_lines: list[LavaflowLogLine]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_log_line import LavaflowLogLine # noqa: PLC0415
        summary = self.summary

        root_cause = self.root_cause

        evidence = self.evidence



        log_lines = []
        for log_lines_item_data in self.log_lines:
            log_lines_item = log_lines_item_data.to_dict()
            log_lines.append(log_lines_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "summary": summary,
            "root_cause": root_cause,
            "evidence": evidence,
            "log_lines": log_lines,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_log_line import LavaflowLogLine # noqa: PLC0415
        d = dict(src_dict)
        summary = d.pop("summary")

        root_cause = d.pop("root_cause")

        evidence = cast(list[str], d.pop("evidence"))


        log_lines = []
        _log_lines = d.pop("log_lines")
        for log_lines_item_data in (_log_lines):
            log_lines_item = LavaflowLogLine.from_dict(log_lines_item_data)



            log_lines.append(log_lines_item)


        lavaflow_diagnosis = cls(
            summary=summary,
            root_cause=root_cause,
            evidence=evidence,
            log_lines=log_lines,
        )


        lavaflow_diagnosis.additional_properties = d
        return lavaflow_diagnosis

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
