from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auth_page_layout import AuthPageLayout
from ..models.auth_page_layout import check_auth_page_layout
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProjectConfigAuthPageLayouts")



@_attrs_define
class ProjectConfigAuthPageLayouts:
    """ 
        Attributes:
            login (AuthPageLayout | Unset):
            signup (AuthPageLayout | Unset):
            forgot_password (AuthPageLayout | Unset):
            device (AuthPageLayout | Unset):
            verify_email (AuthPageLayout | Unset):
            reset_password (AuthPageLayout | Unset):
     """

    login: AuthPageLayout | Unset = UNSET
    signup: AuthPageLayout | Unset = UNSET
    forgot_password: AuthPageLayout | Unset = UNSET
    device: AuthPageLayout | Unset = UNSET
    verify_email: AuthPageLayout | Unset = UNSET
    reset_password: AuthPageLayout | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        login: str | Unset = UNSET
        if not isinstance(self.login, Unset):
            login = self.login


        signup: str | Unset = UNSET
        if not isinstance(self.signup, Unset):
            signup = self.signup


        forgot_password: str | Unset = UNSET
        if not isinstance(self.forgot_password, Unset):
            forgot_password = self.forgot_password


        device: str | Unset = UNSET
        if not isinstance(self.device, Unset):
            device = self.device


        verify_email: str | Unset = UNSET
        if not isinstance(self.verify_email, Unset):
            verify_email = self.verify_email


        reset_password: str | Unset = UNSET
        if not isinstance(self.reset_password, Unset):
            reset_password = self.reset_password



        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if login is not UNSET:
            field_dict["login"] = login
        if signup is not UNSET:
            field_dict["signup"] = signup
        if forgot_password is not UNSET:
            field_dict["forgot_password"] = forgot_password
        if device is not UNSET:
            field_dict["device"] = device
        if verify_email is not UNSET:
            field_dict["verify_email"] = verify_email
        if reset_password is not UNSET:
            field_dict["reset_password"] = reset_password

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _login = d.pop("login", UNSET)
        login: AuthPageLayout | Unset
        if isinstance(_login,  Unset):
            login = UNSET
        else:
            login = check_auth_page_layout(_login)




        _signup = d.pop("signup", UNSET)
        signup: AuthPageLayout | Unset
        if isinstance(_signup,  Unset):
            signup = UNSET
        else:
            signup = check_auth_page_layout(_signup)




        _forgot_password = d.pop("forgot_password", UNSET)
        forgot_password: AuthPageLayout | Unset
        if isinstance(_forgot_password,  Unset):
            forgot_password = UNSET
        else:
            forgot_password = check_auth_page_layout(_forgot_password)




        _device = d.pop("device", UNSET)
        device: AuthPageLayout | Unset
        if isinstance(_device,  Unset):
            device = UNSET
        else:
            device = check_auth_page_layout(_device)




        _verify_email = d.pop("verify_email", UNSET)
        verify_email: AuthPageLayout | Unset
        if isinstance(_verify_email,  Unset):
            verify_email = UNSET
        else:
            verify_email = check_auth_page_layout(_verify_email)




        _reset_password = d.pop("reset_password", UNSET)
        reset_password: AuthPageLayout | Unset
        if isinstance(_reset_password,  Unset):
            reset_password = UNSET
        else:
            reset_password = check_auth_page_layout(_reset_password)




        project_config_auth_page_layouts = cls(
            login=login,
            signup=signup,
            forgot_password=forgot_password,
            device=device,
            verify_email=verify_email,
            reset_password=reset_password,
        )

        return project_config_auth_page_layouts

