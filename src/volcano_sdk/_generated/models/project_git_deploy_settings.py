from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ProjectGitDeploySettings")



@_attrs_define
class ProjectGitDeploySettings:
    """ A project's GitHub auto-deploy settings: what a push to the connected repo's production branch deploys. All settings
    are default-off.

        Attributes:
            auto_deploy_enabled (bool): Whether a production-branch push triggers a deployment.
            deploy_functions (bool): Whether the repo's functions are deployed on push.
            apply_migrations (bool): Whether a push applies the commit's pending migrations, the SQL files under
                volcano/migrations, before it deploys anything. Each database gets a migration run with source `git_deploy`;
                when one fails, nothing from the push deploys and the live version keeps serving. A push starts a migration run
                only while the project owner's account is `active`; otherwise a push that would start one starts none, deploys
                nothing, and fails with code `owner_not_active`. That check does not stop runs a push started before the account
                changed, but a run that has not started applying then fails with `owner_not_active` and the push ends with
                `migration_failed`; the push deploys after its runs succeed only when it needs no new run. Nothing retries that
                push; push again once the account is `active`. Reads back as saved even where the `databases.migrations`
                capability is unavailable; there, a push whose commit has migrations deploys nothing.
            updated_at (datetime.datetime): When the settings were last saved, or last changed by connecting a repository.
                Other changes to the project leave it alone. Settings a connection turned on before Volcano began tracking this
                report the project's last change before then; settings never saved or changed report when the project was
                created.
            frontend_name (str | Unset): Name of the frontend to build and deploy on push. Omitted when no frontend is
                deployed. Resolved at deploy time; need not exist yet.
            frontend_app_root (str | Unset): App root (subdirectory) the frontend builds from. Omitted for the repo root.
     """

    auto_deploy_enabled: bool
    deploy_functions: bool
    apply_migrations: bool
    updated_at: datetime.datetime
    frontend_name: str | Unset = UNSET
    frontend_app_root: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        auto_deploy_enabled = self.auto_deploy_enabled

        deploy_functions = self.deploy_functions

        apply_migrations = self.apply_migrations

        updated_at = self.updated_at.isoformat()

        frontend_name = self.frontend_name

        frontend_app_root = self.frontend_app_root


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "auto_deploy_enabled": auto_deploy_enabled,
            "deploy_functions": deploy_functions,
            "apply_migrations": apply_migrations,
            "updated_at": updated_at,
        })
        if frontend_name is not UNSET:
            field_dict["frontend_name"] = frontend_name
        if frontend_app_root is not UNSET:
            field_dict["frontend_app_root"] = frontend_app_root

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        auto_deploy_enabled = d.pop("auto_deploy_enabled")

        deploy_functions = d.pop("deploy_functions")

        apply_migrations = d.pop("apply_migrations")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        frontend_name = d.pop("frontend_name", UNSET)

        frontend_app_root = d.pop("frontend_app_root", UNSET)

        project_git_deploy_settings = cls(
            auto_deploy_enabled=auto_deploy_enabled,
            deploy_functions=deploy_functions,
            apply_migrations=apply_migrations,
            updated_at=updated_at,
            frontend_name=frontend_name,
            frontend_app_root=frontend_app_root,
        )


        project_git_deploy_settings.additional_properties = d
        return project_git_deploy_settings

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
