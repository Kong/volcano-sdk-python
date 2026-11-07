from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowRepositoryChecks")



@_attrs_define
class LavaflowRepositoryChecks:
    """ Whether LavaFlow ran the repository's own checks, such as its tests, on a fix itself, before it opened a pull
    request or held the fix. CI that runs on the pull request afterwards is the repository's own.

        Attributes:
            status (str): `not_run`: LavaFlow did not run the repository's checks on the fix, for the reason `reason` names.
                Treat a status you don't know as `not_run`.
            reason (str): Stable code for why the checks did not run. `sandbox_unavailable`: LavaFlow cannot run a
                repository's checks itself yet.
            message (str): Text to show for the status and reason. It names the pull request when one opened.
     """

    status: str
    reason: str
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        status = self.status

        reason = self.reason

        message = self.message


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "status": status,
            "reason": reason,
            "message": message,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = d.pop("status")

        reason = d.pop("reason")

        message = d.pop("message")

        lavaflow_repository_checks = cls(
            status=status,
            reason=reason,
            message=message,
        )


        lavaflow_repository_checks.additional_properties = d
        return lavaflow_repository_checks

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
