from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.share_update_request_status import check_share_update_request_status
from ..models.share_update_request_status import ShareUpdateRequestStatus
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ShareUpdateRequest")



@_attrs_define
class ShareUpdateRequest:
    """ 
        Attributes:
            suggested_name (str | Unset):
            description (str | Unset): What the project does, shown to visitors before they deploy. One line of plain text
                with no control characters; surrounding spaces are trimmed. Send an empty string to remove it.
            allow_reshare (bool | Unset): Lets the projects made from this link be shared again by their owners. Switching
                it off stops their copies, and copies of those, from sharing again, read at each request, including links of
                theirs that are already on.
            status (ShareUpdateRequestStatus | Unset):
     """

    suggested_name: str | Unset = UNSET
    description: str | Unset = UNSET
    allow_reshare: bool | Unset = UNSET
    status: ShareUpdateRequestStatus | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        suggested_name = self.suggested_name

        description = self.description

        allow_reshare = self.allow_reshare

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status



        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if suggested_name is not UNSET:
            field_dict["suggested_name"] = suggested_name
        if description is not UNSET:
            field_dict["description"] = description
        if allow_reshare is not UNSET:
            field_dict["allow_reshare"] = allow_reshare
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        suggested_name = d.pop("suggested_name", UNSET)

        description = d.pop("description", UNSET)

        allow_reshare = d.pop("allow_reshare", UNSET)

        _status = d.pop("status", UNSET)
        status: ShareUpdateRequestStatus | Unset
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = check_share_update_request_status(_status)




        share_update_request = cls(
            suggested_name=suggested_name,
            description=description,
            allow_reshare=allow_reshare,
            status=status,
        )

        return share_update_request

