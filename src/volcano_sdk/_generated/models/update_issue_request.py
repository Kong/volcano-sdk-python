from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.issue_status import check_issue_status
from ..models.issue_status import IssueStatus
from typing import cast






T = TypeVar("T", bound="UpdateIssueRequest")



@_attrs_define
class UpdateIssueRequest:
    """ 
        Attributes:
            status (IssueStatus): `open` until someone resolves or ignores the issue. A resolved issue
                seen again reopens.
     """

    status: IssueStatus





    def to_dict(self) -> dict[str, Any]:
        status: str = self.status


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = check_issue_status(d.pop("status"))




        update_issue_request = cls(
            status=status,
        )

        return update_issue_request

