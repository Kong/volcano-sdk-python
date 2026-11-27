from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field
import json
from .. import types

from ..types import UNSET, Unset

from ..types import File, FileTypes
from ..types import UNSET, Unset
from io import BytesIO






T = TypeVar("T", bound="CreateFrontendCandidateBody")



@_attrs_define
class CreateFrontendCandidateBody:
    """ 
        Attributes:
            name (str): Names the Candidate within the frontend. Cannot be `production`.
            archive (File): ZIP or tar.gz archive of the frontend project, as for creating a frontend. The API enforces
                SOURCE_ARCHIVE_SIZE_LIMIT_MB.
            ttl_seconds (int | Unset): Deletes the Candidate this many seconds after it is created, at most 30 days. Omit to
                keep it until deleted.
     """

    name: str
    archive: File
    ttl_seconds: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        archive = self.archive.to_tuple()


        ttl_seconds = self.ttl_seconds


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "archive": archive,
        })
        if ttl_seconds is not UNSET:
            field_dict["ttl_seconds"] = ttl_seconds

        return field_dict


    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("name", (None, str(self.name).encode(), "text/plain")))



        files.append(("archive", self.archive.to_tuple()))



        if not isinstance(self.ttl_seconds, Unset):
            files.append(("ttl_seconds", (None, str(self.ttl_seconds).encode(), "text/plain")))




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




        ttl_seconds = d.pop("ttl_seconds", UNSET)

        create_frontend_candidate_body = cls(
            name=name,
            archive=archive,
            ttl_seconds=ttl_seconds,
        )


        create_frontend_candidate_body.additional_properties = d
        return create_frontend_candidate_body

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
