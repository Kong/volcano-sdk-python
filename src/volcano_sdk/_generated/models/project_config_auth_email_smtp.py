from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ProjectConfigAuthEmailSMTP")



@_attrs_define
class ProjectConfigAuthEmailSMTP:
    """ 
        Attributes:
            host (str | Unset):
            port (int | Unset):
            username (str | Unset):
            password (str | Unset): Write-only; omitted from config export.
            use_tls (bool | Unset):
     """

    host: str | Unset = UNSET
    port: int | Unset = UNSET
    username: str | Unset = UNSET
    password: str | Unset = UNSET
    use_tls: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        host = self.host

        port = self.port

        username = self.username

        password = self.password

        use_tls = self.use_tls


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if host is not UNSET:
            field_dict["host"] = host
        if port is not UNSET:
            field_dict["port"] = port
        if username is not UNSET:
            field_dict["username"] = username
        if password is not UNSET:
            field_dict["password"] = password
        if use_tls is not UNSET:
            field_dict["use_tls"] = use_tls

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        host = d.pop("host", UNSET)

        port = d.pop("port", UNSET)

        username = d.pop("username", UNSET)

        password = d.pop("password", UNSET)

        use_tls = d.pop("use_tls", UNSET)

        project_config_auth_email_smtp = cls(
            host=host,
            port=port,
            username=username,
            password=password,
            use_tls=use_tls,
        )

        return project_config_auth_email_smtp

