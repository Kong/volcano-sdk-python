from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.share_preview_release import SharePreviewRelease





T = TypeVar("T", bound="SharePreview")



@_attrs_define
class SharePreview:
    """ 
        Attributes:
            id (str):
            suggested_name (str): A project name the link's owner suggests, for clients to offer as the default. The create
                request still carries its own `name`; Volcano does not fill one in from the link.
            description (str): What the project does, in the owner's words. Plain text; empty when the owner wrote none.
            release (SharePreviewRelease): The release a project created from the link installs.
     """

    id: str
    suggested_name: str
    description: str
    release: SharePreviewRelease
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.share_preview_release import SharePreviewRelease # noqa: PLC0415
        id = self.id

        suggested_name = self.suggested_name

        description = self.description

        release = self.release.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "suggested_name": suggested_name,
            "description": description,
            "release": release,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.share_preview_release import SharePreviewRelease # noqa: PLC0415
        d = dict(src_dict)
        id = d.pop("id")

        suggested_name = d.pop("suggested_name")

        description = d.pop("description")

        release = SharePreviewRelease.from_dict(d.pop("release"))




        share_preview = cls(
            id=id,
            suggested_name=suggested_name,
            description=description,
            release=release,
        )


        share_preview.additional_properties = d
        return share_preview

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
