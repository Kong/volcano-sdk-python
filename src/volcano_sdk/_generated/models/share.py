from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.share_status import check_share_status
from ..models.share_status import ShareStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.share_release_ref import ShareReleaseRef





T = TypeVar("T", bound="Share")



@_attrs_define
class Share:
    """ 
        Attributes:
            id (str): The link's public identifier. Its address is `https://volcano.dev/deploy/<id>`.
            project_id (UUID):
            suggested_name (str): A project name for clients to offer a visitor as the default. The create request still
                carries its own `name`; Volcano does not fill one in from the link.
            description (str): What the project does, in the owner's words, shown to visitors before they deploy. One line
                of plain text; empty when the owner wrote none.
            allow_reshare (bool): Whether the projects made from this link, and the projects made from those, may be shared
                again by their owners. False by default, so a copy of this project cannot create, draft, publish or switch on a
                deploy link of its own, and its links serve nothing. Read at each request, so switching it off stops copies'
                links that are already on.
            status (ShareStatus): Whether the owner, or Volcano, has the link on. An `active` link can still not serve; see
                `serving`.
            serving (bool): Whether the link's address serves its current release now: it is
                `active`, published, and nothing stops it, such as deploy links not being
                available in this environment, the project being deleted, the owner's
                account not allowing traffic, or the project being a copy that may no
                longer be shared. An `active` link that is not serving
                answers visitors as one switched off, and switching it on again changes
                nothing until what stops it is resolved.
            current_release (None | ShareReleaseRef): The release visitors are offered. Null until the first publish; until
                then the link's preview answers `404`.
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            disabled_reason (None | str | Unset): Why the link is off. Set only while it is disabled. New reasons can be
                added, so treat an unknown one as disabled. `owner`: its owner switched
                it off. `operator`: Volcano took it down; its owner cannot switch it back
                on or delete it (`PATCH` and `DELETE` answer `403` with code
                `operator_disabled`), but can still edit it. While it is down, its
                project cannot be shared any more (no new link, draft or publish, and no
                link switched on), and no project made from it, or from a copy of it, can
                be shared either.
                 Example: owner.
     """

    id: str
    project_id: UUID
    suggested_name: str
    description: str
    allow_reshare: bool
    status: ShareStatus
    serving: bool
    current_release: None | ShareReleaseRef
    created_at: datetime.datetime
    updated_at: datetime.datetime
    disabled_reason: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.share_release_ref import ShareReleaseRef # noqa: PLC0415
        id = self.id

        project_id = str(self.project_id)

        suggested_name = self.suggested_name

        description = self.description

        allow_reshare = self.allow_reshare

        status: str = self.status

        serving = self.serving

        current_release: dict[str, Any] | None
        if isinstance(self.current_release, ShareReleaseRef):
            current_release = self.current_release.to_dict()
        else:
            current_release = self.current_release

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        disabled_reason: None | str | Unset
        if isinstance(self.disabled_reason, Unset):
            disabled_reason = UNSET
        else:
            disabled_reason = self.disabled_reason


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "project_id": project_id,
            "suggested_name": suggested_name,
            "description": description,
            "allow_reshare": allow_reshare,
            "status": status,
            "serving": serving,
            "current_release": current_release,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if disabled_reason is not UNSET:
            field_dict["disabled_reason"] = disabled_reason

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.share_release_ref import ShareReleaseRef # noqa: PLC0415
        d = dict(src_dict)
        id = d.pop("id")

        project_id = UUID(d.pop("project_id"))




        suggested_name = d.pop("suggested_name")

        description = d.pop("description")

        allow_reshare = d.pop("allow_reshare")

        status = check_share_status(d.pop("status"))




        serving = d.pop("serving")

        def _parse_current_release(data: object) -> None | ShareReleaseRef:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                current_release_type_1 = ShareReleaseRef.from_dict(data)



                return current_release_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ShareReleaseRef, data)

        current_release = _parse_current_release(d.pop("current_release"))


        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        def _parse_disabled_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        disabled_reason = _parse_disabled_reason(d.pop("disabled_reason", UNSET))


        share = cls(
            id=id,
            project_id=project_id,
            suggested_name=suggested_name,
            description=description,
            allow_reshare=allow_reshare,
            status=status,
            serving=serving,
            current_release=current_release,
            created_at=created_at,
            updated_at=updated_at,
            disabled_reason=disabled_reason,
        )


        share.additional_properties = d
        return share

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
