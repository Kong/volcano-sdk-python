from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="FunctionRollbackRequest")



@_attrs_define
class FunctionRollbackRequest:
    """ 
        Attributes:
            expected_revision (int): The `revision` the caller read from `serving`. Refuses the rollback with
                `stale_revision` unless what the function runs is still at this revision, so a retried rollback cannot undo
                itself.
            to_production (bool | Unset): Return to the function's own build whatever it ran before. Default: False.
     """

    expected_revision: int
    to_production: bool | Unset = False





    def to_dict(self) -> dict[str, Any]:
        expected_revision = self.expected_revision

        to_production = self.to_production


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "expected_revision": expected_revision,
        })
        if to_production is not UNSET:
            field_dict["to_production"] = to_production

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        expected_revision = d.pop("expected_revision")

        to_production = d.pop("to_production", UNSET)

        function_rollback_request = cls(
            expected_revision=expected_revision,
            to_production=to_production,
        )

        return function_rollback_request

