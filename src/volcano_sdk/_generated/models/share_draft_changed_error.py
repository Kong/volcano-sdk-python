from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.share_draft_changed_error_code import check_share_draft_changed_error_code
from ..models.share_draft_changed_error_code import ShareDraftChangedErrorCode
from typing import cast

if TYPE_CHECKING:
  from ..models.share_release_draft import ShareReleaseDraft





T = TypeVar("T", bound="ShareDraftChangedError")



@_attrs_define
class ShareDraftChangedError:
    """ 
        Attributes:
            error (str):
            code (ShareDraftChangedErrorCode):
            draft (ShareReleaseDraft):
     """

    error: str
    code: ShareDraftChangedErrorCode
    draft: ShareReleaseDraft
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.share_release_draft import ShareReleaseDraft # noqa: PLC0415
        error = self.error

        code: str = self.code

        draft = self.draft.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "error": error,
            "code": code,
            "draft": draft,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.share_release_draft import ShareReleaseDraft # noqa: PLC0415
        d = dict(src_dict)
        error = d.pop("error")

        code = check_share_draft_changed_error_code(d.pop("code"))




        draft = ShareReleaseDraft.from_dict(d.pop("draft"))




        share_draft_changed_error = cls(
            error=error,
            code=code,
            draft=draft,
        )


        share_draft_changed_error.additional_properties = d
        return share_draft_changed_error

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
