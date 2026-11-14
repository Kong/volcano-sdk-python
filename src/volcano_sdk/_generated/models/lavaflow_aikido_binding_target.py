from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.aikido_severity import AikidoSeverity
from ..models.aikido_severity import check_aikido_severity
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="LavaflowAikidoBindingTarget")



@_attrs_define
class LavaflowAikidoBindingTarget:
    """ What an `aikido` connector reports for the project. Send `aikido`, not `slack`, for an `aikido` connector.

        Attributes:
            min_severity (AikidoSeverity | Unset): An Aikido issue severity, lowest first.
     """

    min_severity: AikidoSeverity | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        min_severity: str | Unset = UNSET
        if not isinstance(self.min_severity, Unset):
            min_severity = self.min_severity



        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if min_severity is not UNSET:
            field_dict["min_severity"] = min_severity

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _min_severity = d.pop("min_severity", UNSET)
        min_severity: AikidoSeverity | Unset
        if isinstance(_min_severity,  Unset):
            min_severity = UNSET
        else:
            min_severity = check_aikido_severity(_min_severity)




        lavaflow_aikido_binding_target = cls(
            min_severity=min_severity,
        )

        return lavaflow_aikido_binding_target

