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
  from ..models.share_release_function import ShareReleaseFunction
  from ..models.share_release_omission import ShareReleaseOmission
  from ..models.share_variable import ShareVariable





T = TypeVar("T", bound="ShareRelease")



@_attrs_define
class ShareRelease:
    """ 
        Attributes:
            id (UUID):
            share_id (str):
            project_id (UUID):
            published_at (datetime.datetime):
            published_by (str): The id of the user who published the release.
            sha256 (str): The digest of the stored release archive. An install refuses an archive that does not match it.
            size_bytes (int):
            functions (list[ShareReleaseFunction]):
            frontends (list[str]):
            variables (list[ShareVariable]):
            service_key_functions (list[str]):
            omissions (list[ShareReleaseOmission]):
     """

    id: UUID
    share_id: str
    project_id: UUID
    published_at: datetime.datetime
    published_by: str
    sha256: str
    size_bytes: int
    functions: list[ShareReleaseFunction]
    frontends: list[str]
    variables: list[ShareVariable]
    service_key_functions: list[str]
    omissions: list[ShareReleaseOmission]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.share_release_function import ShareReleaseFunction # noqa: PLC0415
        from ..models.share_release_omission import ShareReleaseOmission # noqa: PLC0415
        from ..models.share_variable import ShareVariable # noqa: PLC0415
        id = str(self.id)

        share_id = self.share_id

        project_id = str(self.project_id)

        published_at = self.published_at.isoformat()

        published_by = self.published_by

        sha256 = self.sha256

        size_bytes = self.size_bytes

        functions = []
        for functions_item_data in self.functions:
            functions_item = functions_item_data.to_dict()
            functions.append(functions_item)



        frontends = self.frontends



        variables = []
        for variables_item_data in self.variables:
            variables_item = variables_item_data.to_dict()
            variables.append(variables_item)



        service_key_functions = self.service_key_functions



        omissions = []
        for omissions_item_data in self.omissions:
            omissions_item = omissions_item_data.to_dict()
            omissions.append(omissions_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "share_id": share_id,
            "project_id": project_id,
            "published_at": published_at,
            "published_by": published_by,
            "sha256": sha256,
            "size_bytes": size_bytes,
            "functions": functions,
            "frontends": frontends,
            "variables": variables,
            "service_key_functions": service_key_functions,
            "omissions": omissions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.share_release_function import ShareReleaseFunction # noqa: PLC0415
        from ..models.share_release_omission import ShareReleaseOmission # noqa: PLC0415
        from ..models.share_variable import ShareVariable # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        share_id = d.pop("share_id")

        project_id = UUID(d.pop("project_id"))




        published_at = datetime.datetime.fromisoformat(d.pop("published_at"))




        published_by = d.pop("published_by")

        sha256 = d.pop("sha256")

        size_bytes = d.pop("size_bytes")

        functions = []
        _functions = d.pop("functions")
        for functions_item_data in (_functions):
            functions_item = ShareReleaseFunction.from_dict(functions_item_data)



            functions.append(functions_item)


        frontends = cast(list[str], d.pop("frontends"))


        variables = []
        _variables = d.pop("variables")
        for variables_item_data in (_variables):
            variables_item = ShareVariable.from_dict(variables_item_data)



            variables.append(variables_item)


        service_key_functions = cast(list[str], d.pop("service_key_functions"))


        omissions = []
        _omissions = d.pop("omissions")
        for omissions_item_data in (_omissions):
            omissions_item = ShareReleaseOmission.from_dict(omissions_item_data)



            omissions.append(omissions_item)


        share_release = cls(
            id=id,
            share_id=share_id,
            project_id=project_id,
            published_at=published_at,
            published_by=published_by,
            sha256=sha256,
            size_bytes=size_bytes,
            functions=functions,
            frontends=frontends,
            variables=variables,
            service_key_functions=service_key_functions,
            omissions=omissions,
        )


        share_release.additional_properties = d
        return share_release

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
