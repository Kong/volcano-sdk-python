from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_config_auth_email_password_provider import ProjectConfigAuthEmailPasswordProvider
  from ..models.project_config_o_auth_provider import ProjectConfigOAuthProvider





T = TypeVar("T", bound="ProjectConfigAuthProviders")



@_attrs_define
class ProjectConfigAuthProviders:
    """ 
        Attributes:
            email_password (ProjectConfigAuthEmailPasswordProvider | Unset):
            oauth (list[ProjectConfigOAuthProvider] | Unset): Fully synced when declared - providers absent from this list
                are deleted.
     """

    email_password: ProjectConfigAuthEmailPasswordProvider | Unset = UNSET
    oauth: list[ProjectConfigOAuthProvider] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_auth_email_password_provider import ProjectConfigAuthEmailPasswordProvider
        from ..models.project_config_o_auth_provider import ProjectConfigOAuthProvider
        email_password: dict[str, Any] | Unset = UNSET
        if not isinstance(self.email_password, Unset):
            email_password = self.email_password.to_dict()

        oauth: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.oauth, Unset):
            oauth = []
            for oauth_item_data in self.oauth:
                oauth_item = oauth_item_data.to_dict()
                oauth.append(oauth_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if email_password is not UNSET:
            field_dict["email_password"] = email_password
        if oauth is not UNSET:
            field_dict["oauth"] = oauth

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_auth_email_password_provider import ProjectConfigAuthEmailPasswordProvider
        from ..models.project_config_o_auth_provider import ProjectConfigOAuthProvider
        d = dict(src_dict)
        _email_password = d.pop("email_password", UNSET)
        email_password: ProjectConfigAuthEmailPasswordProvider | Unset
        if isinstance(_email_password,  Unset):
            email_password = UNSET
        else:
            email_password = ProjectConfigAuthEmailPasswordProvider.from_dict(_email_password)




        _oauth = d.pop("oauth", UNSET)
        oauth: list[ProjectConfigOAuthProvider] | Unset = UNSET
        if _oauth is not UNSET:
            oauth = []
            for oauth_item_data in _oauth:
                oauth_item = ProjectConfigOAuthProvider.from_dict(oauth_item_data)



                oauth.append(oauth_item)


        project_config_auth_providers = cls(
            email_password=email_password,
            oauth=oauth,
        )

        return project_config_auth_providers

