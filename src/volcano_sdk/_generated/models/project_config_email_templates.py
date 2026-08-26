from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_config_email_template import ProjectConfigEmailTemplate





T = TypeVar("T", bound="ProjectConfigEmailTemplates")



@_attrs_define
class ProjectConfigEmailTemplates:
    """ Email templates keyed by type. Fully synced when declared - template
    types absent from a declared map revert to server defaults (custom
    bodies deleted, subject overrides cleared). Custom template bodies
    require the PRO plan; subject-only changes are available on FREE.

        Attributes:
            confirmation (ProjectConfigEmailTemplate | Unset):
            password_reset (ProjectConfigEmailTemplate | Unset):
            password_changed (ProjectConfigEmailTemplate | Unset):
            welcome (ProjectConfigEmailTemplate | Unset):
     """

    confirmation: ProjectConfigEmailTemplate | Unset = UNSET
    password_reset: ProjectConfigEmailTemplate | Unset = UNSET
    password_changed: ProjectConfigEmailTemplate | Unset = UNSET
    welcome: ProjectConfigEmailTemplate | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_email_template import ProjectConfigEmailTemplate
        confirmation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.confirmation, Unset):
            confirmation = self.confirmation.to_dict()

        password_reset: dict[str, Any] | Unset = UNSET
        if not isinstance(self.password_reset, Unset):
            password_reset = self.password_reset.to_dict()

        password_changed: dict[str, Any] | Unset = UNSET
        if not isinstance(self.password_changed, Unset):
            password_changed = self.password_changed.to_dict()

        welcome: dict[str, Any] | Unset = UNSET
        if not isinstance(self.welcome, Unset):
            welcome = self.welcome.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if confirmation is not UNSET:
            field_dict["confirmation"] = confirmation
        if password_reset is not UNSET:
            field_dict["password_reset"] = password_reset
        if password_changed is not UNSET:
            field_dict["password_changed"] = password_changed
        if welcome is not UNSET:
            field_dict["welcome"] = welcome

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_email_template import ProjectConfigEmailTemplate
        d = dict(src_dict)
        _confirmation = d.pop("confirmation", UNSET)
        confirmation: ProjectConfigEmailTemplate | Unset
        if isinstance(_confirmation,  Unset):
            confirmation = UNSET
        else:
            confirmation = ProjectConfigEmailTemplate.from_dict(_confirmation)




        _password_reset = d.pop("password_reset", UNSET)
        password_reset: ProjectConfigEmailTemplate | Unset
        if isinstance(_password_reset,  Unset):
            password_reset = UNSET
        else:
            password_reset = ProjectConfigEmailTemplate.from_dict(_password_reset)




        _password_changed = d.pop("password_changed", UNSET)
        password_changed: ProjectConfigEmailTemplate | Unset
        if isinstance(_password_changed,  Unset):
            password_changed = UNSET
        else:
            password_changed = ProjectConfigEmailTemplate.from_dict(_password_changed)




        _welcome = d.pop("welcome", UNSET)
        welcome: ProjectConfigEmailTemplate | Unset
        if isinstance(_welcome,  Unset):
            welcome = UNSET
        else:
            welcome = ProjectConfigEmailTemplate.from_dict(_welcome)




        project_config_email_templates = cls(
            confirmation=confirmation,
            password_reset=password_reset,
            password_changed=password_changed,
            welcome=welcome,
        )

        return project_config_email_templates

