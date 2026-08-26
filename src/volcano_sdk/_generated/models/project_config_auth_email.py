from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_config_auth_email_from import ProjectConfigAuthEmailFrom
  from ..models.project_config_auth_email_smtp import ProjectConfigAuthEmailSMTP
  from ..models.project_config_email_templates import ProjectConfigEmailTemplates





T = TypeVar("T", bound="ProjectConfigAuthEmail")



@_attrs_define
class ProjectConfigAuthEmail:
    """ 
        Attributes:
            enabled (bool | Unset): Enable transactional email sending
            from_ (ProjectConfigAuthEmailFrom | Unset):
            smtp (ProjectConfigAuthEmailSMTP | Unset):
            templates (ProjectConfigEmailTemplates | Unset): Email templates keyed by type. Fully synced when declared -
                template
                types absent from a declared map revert to server defaults (custom
                bodies deleted, subject overrides cleared). Custom template bodies
                require the PRO plan; subject-only changes are available on FREE.
     """

    enabled: bool | Unset = UNSET
    from_: ProjectConfigAuthEmailFrom | Unset = UNSET
    smtp: ProjectConfigAuthEmailSMTP | Unset = UNSET
    templates: ProjectConfigEmailTemplates | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_auth_email_from import ProjectConfigAuthEmailFrom
        from ..models.project_config_auth_email_smtp import ProjectConfigAuthEmailSMTP
        from ..models.project_config_email_templates import ProjectConfigEmailTemplates
        enabled = self.enabled

        from_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.from_, Unset):
            from_ = self.from_.to_dict()

        smtp: dict[str, Any] | Unset = UNSET
        if not isinstance(self.smtp, Unset):
            smtp = self.smtp.to_dict()

        templates: dict[str, Any] | Unset = UNSET
        if not isinstance(self.templates, Unset):
            templates = self.templates.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if from_ is not UNSET:
            field_dict["from"] = from_
        if smtp is not UNSET:
            field_dict["smtp"] = smtp
        if templates is not UNSET:
            field_dict["templates"] = templates

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_auth_email_from import ProjectConfigAuthEmailFrom
        from ..models.project_config_auth_email_smtp import ProjectConfigAuthEmailSMTP
        from ..models.project_config_email_templates import ProjectConfigEmailTemplates
        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        _from_ = d.pop("from", UNSET)
        from_: ProjectConfigAuthEmailFrom | Unset
        if isinstance(_from_,  Unset):
            from_ = UNSET
        else:
            from_ = ProjectConfigAuthEmailFrom.from_dict(_from_)




        _smtp = d.pop("smtp", UNSET)
        smtp: ProjectConfigAuthEmailSMTP | Unset
        if isinstance(_smtp,  Unset):
            smtp = UNSET
        else:
            smtp = ProjectConfigAuthEmailSMTP.from_dict(_smtp)




        _templates = d.pop("templates", UNSET)
        templates: ProjectConfigEmailTemplates | Unset
        if isinstance(_templates,  Unset):
            templates = UNSET
        else:
            templates = ProjectConfigEmailTemplates.from_dict(_templates)




        project_config_auth_email = cls(
            enabled=enabled,
            from_=from_,
            smtp=smtp,
            templates=templates,
        )

        return project_config_auth_email

