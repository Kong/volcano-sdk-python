from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_config_hosted_page import ProjectConfigHostedPage





T = TypeVar("T", bound="ProjectConfigHostedPages")



@_attrs_define
class ProjectConfigHostedPages:
    """ Hosted auth pages keyed by page type (PRO plan). Upsert-only: omitted
    pages are left untouched (there is no delete for hosted pages).

        Attributes:
            login (ProjectConfigHostedPage | Unset):
            reset_password (ProjectConfigHostedPage | Unset):
     """

    login: ProjectConfigHostedPage | Unset = UNSET
    reset_password: ProjectConfigHostedPage | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_hosted_page import ProjectConfigHostedPage
        login: dict[str, Any] | Unset = UNSET
        if not isinstance(self.login, Unset):
            login = self.login.to_dict()

        reset_password: dict[str, Any] | Unset = UNSET
        if not isinstance(self.reset_password, Unset):
            reset_password = self.reset_password.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if login is not UNSET:
            field_dict["login"] = login
        if reset_password is not UNSET:
            field_dict["reset_password"] = reset_password

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_hosted_page import ProjectConfigHostedPage
        d = dict(src_dict)
        _login = d.pop("login", UNSET)
        login: ProjectConfigHostedPage | Unset
        if isinstance(_login,  Unset):
            login = UNSET
        else:
            login = ProjectConfigHostedPage.from_dict(_login)




        _reset_password = d.pop("reset_password", UNSET)
        reset_password: ProjectConfigHostedPage | Unset
        if isinstance(_reset_password,  Unset):
            reset_password = UNSET
        else:
            reset_password = ProjectConfigHostedPage.from_dict(_reset_password)




        project_config_hosted_pages = cls(
            login=login,
            reset_password=reset_password,
        )

        return project_config_hosted_pages

