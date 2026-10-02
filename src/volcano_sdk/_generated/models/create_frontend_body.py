from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field
import json
from .. import types

from ..types import UNSET, Unset

from ..models.create_frontend_body_framework import check_create_frontend_body_framework
from ..models.create_frontend_body_framework import CreateFrontendBodyFramework
from ..types import File, FileTypes
from ..types import UNSET, Unset
from io import BytesIO
from typing import cast






T = TypeVar("T", bound="CreateFrontendBody")



@_attrs_define
class CreateFrontendBody:
    """ 
        Attributes:
            name (str): DNS-safe frontend name
            archive (File): ZIP or tar.gz archive of the frontend project directory or monorepo workspace root. The API
                enforces SOURCE_ARCHIVE_SIZE_LIMIT_MB and stores a normalized tar.gz archive.
            framework (CreateFrontendBodyFramework | Unset): Next.js frontend. Supported Next.js majors are 15.x and 16.x.
                Default: 'nextjs'.
            app_root (str | Unset): Optional relative POSIX path from the uploaded archive root to the Next.js app to build,
                for example `apps/web`. Example: apps/web.
     """

    name: str
    archive: File
    framework: CreateFrontendBodyFramework | Unset = 'nextjs'
    app_root: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        archive = self.archive.to_tuple()


        framework: str | Unset = UNSET
        if not isinstance(self.framework, Unset):
            framework = self.framework


        app_root = self.app_root


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "archive": archive,
        })
        if framework is not UNSET:
            field_dict["framework"] = framework
        if app_root is not UNSET:
            field_dict["app_root"] = app_root

        return field_dict


    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("name", (None, str(self.name).encode(), "text/plain")))



        files.append(("archive", self.archive.to_tuple()))



        if not isinstance(self.framework, Unset):
            files.append(("framework", (None, str(self.framework).encode(), "text/plain")))



        if not isinstance(self.app_root, Unset):
            files.append(("app_root", (None, str(self.app_root).encode(), "text/plain")))




        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))



        return files


    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        archive = File(
             payload = BytesIO(d.pop("archive"))
        )




        _framework = d.pop("framework", UNSET)
        framework: CreateFrontendBodyFramework | Unset
        if isinstance(_framework,  Unset):
            framework = UNSET
        else:
            framework = check_create_frontend_body_framework(_framework)




        app_root = d.pop("app_root", UNSET)

        create_frontend_body = cls(
            name=name,
            archive=archive,
            framework=framework,
            app_root=app_root,
        )


        create_frontend_body.additional_properties = d
        return create_frontend_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
