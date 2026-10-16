from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.autofix_pull_request_state import AutofixPullRequestState
from ..models.autofix_pull_request_state import check_autofix_pull_request_state
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="AutofixPullRequest")



@_attrs_define
class AutofixPullRequest:
    """ The draft pull request the run opened on the connected repository.

        Attributes:
            number (int):
            url (str):
            branch (str): The branch the fix is on, `volcano/autofix/<run id>`.
            state (AutofixPullRequestState):
            closed_at (datetime.datetime | Unset): When the pull request was merged or closed.
            deployed_at (datetime.datetime | Unset): When a deployment that includes the merged fix went live. The issue
                resolves then, unless it occurred again since. When more than 20 deployments went live after the merge before
                Volcano checked, it is the merge time instead.
     """

    number: int
    url: str
    branch: str
    state: AutofixPullRequestState
    closed_at: datetime.datetime | Unset = UNSET
    deployed_at: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        number = self.number

        url = self.url

        branch = self.branch

        state: str = self.state

        closed_at: str | Unset = UNSET
        if not isinstance(self.closed_at, Unset):
            closed_at = self.closed_at.isoformat()

        deployed_at: str | Unset = UNSET
        if not isinstance(self.deployed_at, Unset):
            deployed_at = self.deployed_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "number": number,
            "url": url,
            "branch": branch,
            "state": state,
        })
        if closed_at is not UNSET:
            field_dict["closed_at"] = closed_at
        if deployed_at is not UNSET:
            field_dict["deployed_at"] = deployed_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        number = d.pop("number")

        url = d.pop("url")

        branch = d.pop("branch")

        state = check_autofix_pull_request_state(d.pop("state"))




        _closed_at = d.pop("closed_at", UNSET)
        closed_at: datetime.datetime | Unset
        if isinstance(_closed_at,  Unset):
            closed_at = UNSET
        else:
            closed_at = datetime.datetime.fromisoformat(_closed_at)




        _deployed_at = d.pop("deployed_at", UNSET)
        deployed_at: datetime.datetime | Unset
        if isinstance(_deployed_at,  Unset):
            deployed_at = UNSET
        else:
            deployed_at = datetime.datetime.fromisoformat(_deployed_at)




        autofix_pull_request = cls(
            number=number,
            url=url,
            branch=branch,
            state=state,
            closed_at=closed_at,
            deployed_at=deployed_at,
        )

        return autofix_pull_request

