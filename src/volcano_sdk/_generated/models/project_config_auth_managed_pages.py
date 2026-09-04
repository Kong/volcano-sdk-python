from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_config_auth_page_appearance import ProjectConfigAuthPageAppearance
  from ..models.project_config_auth_redirects import ProjectConfigAuthRedirects
  from ..models.project_config_hosted_pages import ProjectConfigHostedPages





T = TypeVar("T", bound="ProjectConfigAuthManagedPages")



@_attrs_define
class ProjectConfigAuthManagedPages:
    """ 
        Attributes:
            enabled (bool | Unset): Enable or disable managed auth hosted pages
            redirects (ProjectConfigAuthRedirects | Unset):
            pages (ProjectConfigHostedPages | Unset): Hosted auth pages keyed by page type (PRO plan). Upsert-only: omitted
                pages are left untouched (there is no delete for hosted pages).
            appearance (ProjectConfigAuthPageAppearance | Unset):
     """

    enabled: bool | Unset = UNSET
    redirects: ProjectConfigAuthRedirects | Unset = UNSET
    pages: ProjectConfigHostedPages | Unset = UNSET
    appearance: ProjectConfigAuthPageAppearance | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_auth_page_appearance import ProjectConfigAuthPageAppearance
        from ..models.project_config_auth_redirects import ProjectConfigAuthRedirects
        from ..models.project_config_hosted_pages import ProjectConfigHostedPages
        enabled = self.enabled

        redirects: dict[str, Any] | Unset = UNSET
        if not isinstance(self.redirects, Unset):
            redirects = self.redirects.to_dict()

        pages: dict[str, Any] | Unset = UNSET
        if not isinstance(self.pages, Unset):
            pages = self.pages.to_dict()

        appearance: dict[str, Any] | Unset = UNSET
        if not isinstance(self.appearance, Unset):
            appearance = self.appearance.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if redirects is not UNSET:
            field_dict["redirects"] = redirects
        if pages is not UNSET:
            field_dict["pages"] = pages
        if appearance is not UNSET:
            field_dict["appearance"] = appearance

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_auth_page_appearance import ProjectConfigAuthPageAppearance
        from ..models.project_config_auth_redirects import ProjectConfigAuthRedirects
        from ..models.project_config_hosted_pages import ProjectConfigHostedPages
        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        _redirects = d.pop("redirects", UNSET)
        redirects: ProjectConfigAuthRedirects | Unset
        if isinstance(_redirects,  Unset):
            redirects = UNSET
        else:
            redirects = ProjectConfigAuthRedirects.from_dict(_redirects)




        _pages = d.pop("pages", UNSET)
        pages: ProjectConfigHostedPages | Unset
        if isinstance(_pages,  Unset):
            pages = UNSET
        else:
            pages = ProjectConfigHostedPages.from_dict(_pages)




        _appearance = d.pop("appearance", UNSET)
        appearance: ProjectConfigAuthPageAppearance | Unset
        if isinstance(_appearance,  Unset):
            appearance = UNSET
        else:
            appearance = ProjectConfigAuthPageAppearance.from_dict(_appearance)




        project_config_auth_managed_pages = cls(
            enabled=enabled,
            redirects=redirects,
            pages=pages,
            appearance=appearance,
        )

        return project_config_auth_managed_pages

