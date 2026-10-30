from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="GitDeploymentRunError")



@_attrs_define
class GitDeploymentRunError:
    """ Why a run failed or was skipped.

        Attributes:
            code (str): Stable machine-readable reason. For a failed run: `migration_failed`, `migration_invalid_layout`,
                `migration_timeout`, `feature_unavailable`, `owner_not_active`, `source_invalid`, `child_deploy_failed`,
                `child_deploy_not_started`, `deploy_refused`, `typescript_not_compiled`, `deploy_failed`, or
                `max_attempts_exhausted`. `source_invalid`, `deploy_refused`, and `typescript_not_compiled` fail the same way if
                the same commit is pushed again; `child_deploy_not_started`, `deploy_failed`, and `max_attempts_exhausted` may
                succeed on another push, and `owner_not_active` may once the project owner's account is `active`. For a skipped
                run: `auto_deploy_disabled`, `binding_changed`, `disconnected`, `project_missing`, or `nothing_to_deploy`. Treat
                a code you do not know as a failure.
            message (str): What happened. For `migration_failed`, `migration_invalid_layout`, `source_invalid`,
                `deploy_refused`, `child_deploy_not_started`, and `typescript_not_compiled` it names the database, files,
                resource, or setting at fault when Volcano has them.
     """

    code: str
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "code": code,
            "message": message,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        git_deployment_run_error = cls(
            code=code,
            message=message,
        )


        git_deployment_run_error.additional_properties = d
        return git_deployment_run_error

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
