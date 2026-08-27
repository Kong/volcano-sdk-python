from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_config_o_auth_provider_provider import check_project_config_o_auth_provider_provider
from ..models.project_config_o_auth_provider_provider import ProjectConfigOAuthProviderProvider
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProjectConfigOAuthProvider")



@_attrs_define
class ProjectConfigOAuthProvider:
    """ 
        Attributes:
            provider (ProjectConfigOAuthProviderProvider):
            enabled (bool | Unset):
            client_id (str | Unset): Required for non-device providers. Server-generated for
                `provider=device` (exported read-only, ignored on apply).
            client_secret (str | Unset): Write-only; omitted from config export. Not used for `provider=device`.
            redirect_url (str | Unset): Not used for `provider=device`.
            scopes (list[str] | Unset):
     """

    provider: ProjectConfigOAuthProviderProvider
    enabled: bool | Unset = UNSET
    client_id: str | Unset = UNSET
    client_secret: str | Unset = UNSET
    redirect_url: str | Unset = UNSET
    scopes: list[str] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        provider: str = self.provider

        enabled = self.enabled

        client_id = self.client_id

        client_secret = self.client_secret

        redirect_url = self.redirect_url

        scopes: list[str] | Unset = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "provider": provider,
        })
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_secret is not UNSET:
            field_dict["client_secret"] = client_secret
        if redirect_url is not UNSET:
            field_dict["redirect_url"] = redirect_url
        if scopes is not UNSET:
            field_dict["scopes"] = scopes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider = check_project_config_o_auth_provider_provider(d.pop("provider"))




        enabled = d.pop("enabled", UNSET)

        client_id = d.pop("client_id", UNSET)

        client_secret = d.pop("client_secret", UNSET)

        redirect_url = d.pop("redirect_url", UNSET)

        scopes = cast(list[str], d.pop("scopes", UNSET))


        project_config_o_auth_provider = cls(
            provider=provider,
            enabled=enabled,
            client_id=client_id,
            client_secret=client_secret,
            redirect_url=redirect_url,
            scopes=scopes,
        )

        return project_config_o_auth_provider

