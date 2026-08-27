from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_config_auth_signup_allowed_email_domains_mode import check_project_config_auth_signup_allowed_email_domains_mode
from ..models.project_config_auth_signup_allowed_email_domains_mode import ProjectConfigAuthSignupAllowedEmailDomainsMode
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProjectConfigAuthSignup")



@_attrs_define
class ProjectConfigAuthSignup:
    """ 
        Attributes:
            enable_signup (bool | Unset): Master switch for signups across ALL providers
            enable_anonymous_signins (bool | Unset):
            allowed_email_domains (list[str] | Unset): Email domains allowed to create users. Empty allows every domain.
                Replaces the stored list; entries are normalized (lowercase, no `@`
                prefix) and must be bare domains such as `domain1.com`. Matching is
                exact, so subdomains need their own entry. At most 100 entries.

                Restricting signups is a PRO feature to configure and to enforce: a
                FREE project can only declare the list it already has or remove the
                restriction, and the list it keeps is parked until it upgrades.
                 Example: ['domain1.com', 'domain2.com'].
            allowed_email_domains_mode (ProjectConfigAuthSignupAllowedEmailDomainsMode | Unset): How far
                `allowed_email_domains` reaches. `signup` gates account
                creation only. `signup_and_signin` also blocks sign-in for accounts
                outside the list and signs out the ones it locks out. `disabled`
                keeps the list without enforcing it.
     """

    enable_signup: bool | Unset = UNSET
    enable_anonymous_signins: bool | Unset = UNSET
    allowed_email_domains: list[str] | Unset = UNSET
    allowed_email_domains_mode: ProjectConfigAuthSignupAllowedEmailDomainsMode | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        enable_signup = self.enable_signup

        enable_anonymous_signins = self.enable_anonymous_signins

        allowed_email_domains: list[str] | Unset = UNSET
        if not isinstance(self.allowed_email_domains, Unset):
            allowed_email_domains = self.allowed_email_domains



        allowed_email_domains_mode: str | Unset = UNSET
        if not isinstance(self.allowed_email_domains_mode, Unset):
            allowed_email_domains_mode = self.allowed_email_domains_mode



        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if enable_signup is not UNSET:
            field_dict["enable_signup"] = enable_signup
        if enable_anonymous_signins is not UNSET:
            field_dict["enable_anonymous_signins"] = enable_anonymous_signins
        if allowed_email_domains is not UNSET:
            field_dict["allowed_email_domains"] = allowed_email_domains
        if allowed_email_domains_mode is not UNSET:
            field_dict["allowed_email_domains_mode"] = allowed_email_domains_mode

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enable_signup = d.pop("enable_signup", UNSET)

        enable_anonymous_signins = d.pop("enable_anonymous_signins", UNSET)

        allowed_email_domains = cast(list[str], d.pop("allowed_email_domains", UNSET))


        _allowed_email_domains_mode = d.pop("allowed_email_domains_mode", UNSET)
        allowed_email_domains_mode: ProjectConfigAuthSignupAllowedEmailDomainsMode | Unset
        if isinstance(_allowed_email_domains_mode,  Unset):
            allowed_email_domains_mode = UNSET
        else:
            allowed_email_domains_mode = check_project_config_auth_signup_allowed_email_domains_mode(_allowed_email_domains_mode)




        project_config_auth_signup = cls(
            enable_signup=enable_signup,
            enable_anonymous_signins=enable_anonymous_signins,
            allowed_email_domains=allowed_email_domains,
            allowed_email_domains_mode=allowed_email_domains_mode,
        )

        return project_config_auth_signup

