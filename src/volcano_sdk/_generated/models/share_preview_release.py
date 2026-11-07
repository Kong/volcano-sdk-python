from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.share_release_omission import ShareReleaseOmission
  from ..models.share_variable import ShareVariable





T = TypeVar("T", bound="SharePreviewRelease")



@_attrs_define
class SharePreviewRelease:
    """ The release a project created from the link installs.

        Attributes:
            id (UUID): Send it as `release_id` in `POST /forks` to confirm this release.
            published_at (datetime.datetime):
            sha256 (str): The digest of the stored release archive.
            frontends (list[str]): Names of the frontends installing the release creates.
            functions (list[str]): Names of the functions installing the release creates.
            service_key_functions (list[str]): Names of the functions that receive the new project's `VOLCANO_SERVICE_KEY`,
                which bypasses row-level security. Show them to the visitor before they
                confirm. Empty when no function receives it.
            variables (list[ShareVariable]): The project variables the new project gets, sorted by name. A visitor may
                give a value for any of them as `variables` when creating
                the fork with `POST /forks`; each one left out is created empty, for the visitor to set
                later. Volcano's own variables, such as `VOLCANO_API_URL`, are never
                listed: the install sets them.
            omissions (list[ShareReleaseOmission]): What the release does not carry. A `database` entry means the new
                project starts without that database.
     """

    id: UUID
    published_at: datetime.datetime
    sha256: str
    frontends: list[str]
    functions: list[str]
    service_key_functions: list[str]
    variables: list[ShareVariable]
    omissions: list[ShareReleaseOmission]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.share_release_omission import ShareReleaseOmission # noqa: PLC0415
        from ..models.share_variable import ShareVariable # noqa: PLC0415
        id = str(self.id)

        published_at = self.published_at.isoformat()

        sha256 = self.sha256

        frontends = self.frontends



        functions = self.functions



        service_key_functions = self.service_key_functions



        variables = []
        for variables_item_data in self.variables:
            variables_item = variables_item_data.to_dict()
            variables.append(variables_item)



        omissions = []
        for omissions_item_data in self.omissions:
            omissions_item = omissions_item_data.to_dict()
            omissions.append(omissions_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "published_at": published_at,
            "sha256": sha256,
            "frontends": frontends,
            "functions": functions,
            "service_key_functions": service_key_functions,
            "variables": variables,
            "omissions": omissions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.share_release_omission import ShareReleaseOmission # noqa: PLC0415
        from ..models.share_variable import ShareVariable # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        published_at = datetime.datetime.fromisoformat(d.pop("published_at"))




        sha256 = d.pop("sha256")

        frontends = cast(list[str], d.pop("frontends"))


        functions = cast(list[str], d.pop("functions"))


        service_key_functions = cast(list[str], d.pop("service_key_functions"))


        variables = []
        _variables = d.pop("variables")
        for variables_item_data in (_variables):
            variables_item = ShareVariable.from_dict(variables_item_data)



            variables.append(variables_item)


        omissions = []
        _omissions = d.pop("omissions")
        for omissions_item_data in (_omissions):
            omissions_item = ShareReleaseOmission.from_dict(omissions_item_data)



            omissions.append(omissions_item)


        share_preview_release = cls(
            id=id,
            published_at=published_at,
            sha256=sha256,
            frontends=frontends,
            functions=functions,
            service_key_functions=service_key_functions,
            variables=variables,
            omissions=omissions,
        )


        share_preview_release.additional_properties = d
        return share_preview_release

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
