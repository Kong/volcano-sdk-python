from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_draft_reason import check_lavaflow_draft_reason
from ..models.lavaflow_draft_reason import LavaflowDraftReason
from ..models.lavaflow_pull_request_state import check_lavaflow_pull_request_state
from ..models.lavaflow_pull_request_state import LavaflowPullRequestState
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="LavaflowPullRequest")



@_attrs_define
class LavaflowPullRequest:
    """ 
        Attributes:
            number (int):
            url (str):
            state (LavaflowPullRequestState):
            opened_at (datetime.datetime | None): When the run opened the pull request, null for one opened before LavaFlow
                recorded the time.
            merged_at (datetime.datetime | None): When the pull request merged; null unless `state` is `merged`.
            deployed_at (datetime.datetime | None): When the merged fix went live: the first live deployment of the issue's
                resource that includes it finished. When more than 20 deployments went live between the merge and the one
                LavaFlow found the fix in, LavaFlow can't tell which first included it, and this is the merge time. Null until
                LavaFlow finds the fix live, and for a pull request that didn't merge. LavaFlow watches the resource's
                deployments for a week after the merge.
            draft (bool | None): Whether the pull request is a draft, as GitHub last reported it to LavaFlow. Null for one
                opened before LavaFlow recorded it.
            draft_reason (LavaflowDraftReason | None): Why the pull request is a draft, null unless `draft` is true.
            branch (str | Unset): The recorded pull request branch. Omitted when it was not recorded, the run's fix is
                withheld because it may add a credential, or the full branch name cannot be served under the project's text
                privacy checks. It is never shortened.
     """

    number: int
    url: str
    state: LavaflowPullRequestState
    opened_at: datetime.datetime | None
    merged_at: datetime.datetime | None
    deployed_at: datetime.datetime | None
    draft: bool | None
    draft_reason: LavaflowDraftReason | None
    branch: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        number = self.number

        url = self.url

        state: str = self.state

        opened_at: None | str
        if isinstance(self.opened_at, datetime.datetime):
            opened_at = self.opened_at.isoformat()
        else:
            opened_at = self.opened_at

        merged_at: None | str
        if isinstance(self.merged_at, datetime.datetime):
            merged_at = self.merged_at.isoformat()
        else:
            merged_at = self.merged_at

        deployed_at: None | str
        if isinstance(self.deployed_at, datetime.datetime):
            deployed_at = self.deployed_at.isoformat()
        else:
            deployed_at = self.deployed_at

        draft: bool | None
        draft = self.draft

        draft_reason: None | str
        if isinstance(self.draft_reason, str):
            draft_reason = self.draft_reason
        else:
            draft_reason = self.draft_reason

        branch = self.branch


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "number": number,
            "url": url,
            "state": state,
            "opened_at": opened_at,
            "merged_at": merged_at,
            "deployed_at": deployed_at,
            "draft": draft,
            "draft_reason": draft_reason,
        })
        if branch is not UNSET:
            field_dict["branch"] = branch

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        number = d.pop("number")

        url = d.pop("url")

        state = check_lavaflow_pull_request_state(d.pop("state"))




        def _parse_opened_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                opened_at_type_0 = datetime.datetime.fromisoformat(data)



                return opened_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        opened_at = _parse_opened_at(d.pop("opened_at"))


        def _parse_merged_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                merged_at_type_0 = datetime.datetime.fromisoformat(data)



                return merged_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        merged_at = _parse_merged_at(d.pop("merged_at"))


        def _parse_deployed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deployed_at_type_0 = datetime.datetime.fromisoformat(data)



                return deployed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        deployed_at = _parse_deployed_at(d.pop("deployed_at"))


        def _parse_draft(data: object) -> bool | None:
            if data is None:
                return data
            return cast(bool | None, data)

        draft = _parse_draft(d.pop("draft"))


        def _parse_draft_reason(data: object) -> LavaflowDraftReason | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                draft_reason_type_1 = check_lavaflow_draft_reason(data)



                return draft_reason_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LavaflowDraftReason | None, data)

        draft_reason = _parse_draft_reason(d.pop("draft_reason"))


        branch = d.pop("branch", UNSET)

        lavaflow_pull_request = cls(
            number=number,
            url=url,
            state=state,
            opened_at=opened_at,
            merged_at=merged_at,
            deployed_at=deployed_at,
            draft=draft,
            draft_reason=draft_reason,
            branch=branch,
        )


        lavaflow_pull_request.additional_properties = d
        return lavaflow_pull_request

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
