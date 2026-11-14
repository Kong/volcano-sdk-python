from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_source_unavailable_reason import check_lavaflow_source_unavailable_reason
from ..models.lavaflow_source_unavailable_reason import LavaflowSourceUnavailableReason
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="LavaflowSourceUnavailable")



@_attrs_define
class LavaflowSourceUnavailable:
    """ Why LavaFlow couldn't read, or open a fix on, the code that served a run's error, so the run opened no pull request.

        Attributes:
            reason (LavaflowSourceUnavailableReason): Why LavaFlow couldn't read, or open a fix on, the code that served the
                error, with what you can do. LavaFlow reads the deployment that served the error, so once you deploy code it can
                read, it starts a new run when the error happens again. `no_repository`: LavaFlow is on for no repository; link
                one. `no_commit`: the deployment recorded no commit, nor did the build a redeploy serves, or no deployment was
                serving; deploy by pushing to the linked repository's production branch, or with the CLI from a clean checkout
                of a commit on that branch. `uncommitted_changes`: the deployment's files differ from its commit (`dirty:
                true`), as when the checkout had uncommitted changes; commit and push them, then deploy from the clean checkout.
                `unverified_commit`: Volcano couldn't verify the deployment's commit against the linked repository
                (`verification: none`), for example because the commit isn't on the production branch, or the deployment is a
                function redeploy, which doesn't carry its upload's `verification: repository` commit; push the commit to the
                production branch and deploy it again. `other_repository`: the commit LavaFlow would read is from a repository
                other than the one LavaFlow is on for, Volcano checked it under an earlier repository link, or the project no
                longer links that repository. For a deployment, deploy again from the linked repository; for a reported problem
                or a Code Quality finding, start a new run while the project links the repository LavaFlow is on for.
                `repository_unreadable`: LavaFlow couldn't read the repository at the commit, for example because the Volcano
                GitHub App lost access to it; check the project's repository link and the App's access.
                `commit_not_on_production_branch`: the production branch no longer holds the commit the fix is on, so LavaFlow
                opened no pull request; deploy from the production branch. `deployment_unattributed`: a newer deployment that
                may have changed the code was going live when the error happened, so LavaFlow couldn't tell which one threw it;
                if the error happens again, LavaFlow starts a new run once; if that run also ends `deployment_unattributed`, the
                next waits for a new deploy. A `deployment_unattributed` run right after another one, even one a deploy started,
                gets no such run. New reasons may appear.
            deployment_id (None | UUID): The deployment of the run's `resource` that served the error, for `no_commit`,
                `uncommitted_changes`, `unverified_commit` and `other_repository`. Null for any other reason, including
                `deployment_unattributed`, and when no deployment was serving. Example: 7c2e5a1f-3b8d-4e6a-9f0c-1d2e3f4a5b6c.
     """

    reason: LavaflowSourceUnavailableReason
    deployment_id: None | UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        reason: str = self.reason

        deployment_id: None | str
        if isinstance(self.deployment_id, UUID):
            deployment_id = str(self.deployment_id)
        else:
            deployment_id = self.deployment_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "reason": reason,
            "deployment_id": deployment_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = check_lavaflow_source_unavailable_reason(d.pop("reason"))




        def _parse_deployment_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deployment_id_type_0 = UUID(data)



                return deployment_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        deployment_id = _parse_deployment_id(d.pop("deployment_id"))


        lavaflow_source_unavailable = cls(
            reason=reason,
            deployment_id=deployment_id,
        )


        lavaflow_source_unavailable.additional_properties = d
        return lavaflow_source_unavailable

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
