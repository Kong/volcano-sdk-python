from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.share_release_omission_kind import check_share_release_omission_kind
from ..models.share_release_omission_kind import ShareReleaseOmissionKind
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ShareReleaseOmission")



@_attrs_define
class ShareReleaseOmission:
    """ Something a release does not carry.

        Attributes:
            kind (ShareReleaseOmissionKind): `no_source`: a function or frontend whose current deployment has no stored
                source to carry. `database`: a database; a visitor's project starts without
                one. `sandbox`: a sandbox, which releases do not deploy. `secret_file`: a
                file that may hold credentials, such as a dotenv or `.envrc` file, a tool's
                token file like `.netrc` or an `.npmrc` holding a registry credential, a
                private key, a credential JSON or a Terraform variables file. `unsupported_entry`: a file that is not a regular
                file,
                such as a symbolic link.
            resource (str | Unset): The function, frontend, database or sandbox, when there is one.
            path (str | Unset): The file left out, for a file.
     """

    kind: ShareReleaseOmissionKind
    resource: str | Unset = UNSET
    path: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        resource = self.resource

        path = self.path


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "kind": kind,
        })
        if resource is not UNSET:
            field_dict["resource"] = resource
        if path is not UNSET:
            field_dict["path"] = path

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_share_release_omission_kind(d.pop("kind"))




        resource = d.pop("resource", UNSET)

        path = d.pop("path", UNSET)

        share_release_omission = cls(
            kind=kind,
            resource=resource,
            path=path,
        )


        share_release_omission.additional_properties = d
        return share_release_omission

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
