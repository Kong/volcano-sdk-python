from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.autofix_edit import AutofixEdit





T = TypeVar("T", bound="AutofixPatch")



@_attrs_define
class AutofixPatch:
    """ The fix the model proposed, applied to the deployed commit. Present whenever the run opened a pull request, and when
    a valid fix could not be published.

        Attributes:
            title (str):
            edits (list[AutofixEdit]):
     """

    title: str
    edits: list[AutofixEdit]





    def to_dict(self) -> dict[str, Any]:
        from ..models.autofix_edit import AutofixEdit # noqa: PLC0415
        title = self.title

        edits = []
        for edits_item_data in self.edits:
            edits_item = edits_item_data.to_dict()
            edits.append(edits_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "title": title,
            "edits": edits,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.autofix_edit import AutofixEdit # noqa: PLC0415
        d = dict(src_dict)
        title = d.pop("title")

        edits = []
        _edits = d.pop("edits")
        for edits_item_data in (_edits):
            edits_item = AutofixEdit.from_dict(edits_item_data)



            edits.append(edits_item)


        autofix_patch = cls(
            title=title,
            edits=edits,
        )

        return autofix_patch

