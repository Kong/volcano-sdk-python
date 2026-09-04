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
            signup (ProjectConfigHostedPage | Unset):
            forgot_password (ProjectConfigHostedPage | Unset):
            device (ProjectConfigHostedPage | Unset):
            verify_email (ProjectConfigHostedPage | Unset):
     """

    login: ProjectConfigHostedPage | Unset = UNSET
    reset_password: ProjectConfigHostedPage | Unset = UNSET
    signup: ProjectConfigHostedPage | Unset = UNSET
    forgot_password: ProjectConfigHostedPage | Unset = UNSET
    device: ProjectConfigHostedPage | Unset = UNSET
    verify_email: ProjectConfigHostedPage | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_hosted_page import ProjectConfigHostedPage
        login: dict[str, Any] | Unset = UNSET
        if not isinstance(self.login, Unset):
            login = self.login.to_dict()

        reset_password: dict[str, Any] | Unset = UNSET
        if not isinstance(self.reset_password, Unset):
            reset_password = self.reset_password.to_dict()

        signup: dict[str, Any] | Unset = UNSET
        if not isinstance(self.signup, Unset):
            signup = self.signup.to_dict()

        forgot_password: dict[str, Any] | Unset = UNSET
        if not isinstance(self.forgot_password, Unset):
            forgot_password = self.forgot_password.to_dict()

        device: dict[str, Any] | Unset = UNSET
        if not isinstance(self.device, Unset):
            device = self.device.to_dict()

        verify_email: dict[str, Any] | Unset = UNSET
        if not isinstance(self.verify_email, Unset):
            verify_email = self.verify_email.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if login is not UNSET:
            field_dict["login"] = login
        if reset_password is not UNSET:
            field_dict["reset_password"] = reset_password
        if signup is not UNSET:
            field_dict["signup"] = signup
        if forgot_password is not UNSET:
            field_dict["forgot_password"] = forgot_password
        if device is not UNSET:
            field_dict["device"] = device
        if verify_email is not UNSET:
            field_dict["verify_email"] = verify_email

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




        _signup = d.pop("signup", UNSET)
        signup: ProjectConfigHostedPage | Unset
        if isinstance(_signup,  Unset):
            signup = UNSET
        else:
            signup = ProjectConfigHostedPage.from_dict(_signup)




        _forgot_password = d.pop("forgot_password", UNSET)
        forgot_password: ProjectConfigHostedPage | Unset
        if isinstance(_forgot_password,  Unset):
            forgot_password = UNSET
        else:
            forgot_password = ProjectConfigHostedPage.from_dict(_forgot_password)




        _device = d.pop("device", UNSET)
        device: ProjectConfigHostedPage | Unset
        if isinstance(_device,  Unset):
            device = UNSET
        else:
            device = ProjectConfigHostedPage.from_dict(_device)




        _verify_email = d.pop("verify_email", UNSET)
        verify_email: ProjectConfigHostedPage | Unset
        if isinstance(_verify_email,  Unset):
            verify_email = UNSET
        else:
            verify_email = ProjectConfigHostedPage.from_dict(_verify_email)




        project_config_hosted_pages = cls(
            login=login,
            reset_password=reset_password,
            signup=signup,
            forgot_password=forgot_password,
            device=device,
            verify_email=verify_email,
        )

        return project_config_hosted_pages

