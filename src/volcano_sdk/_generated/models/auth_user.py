from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auth_user_status import AuthUserStatus
from ..models.auth_user_status import check_auth_user_status
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.auth_user_app_metadata import AuthUserAppMetadata
  from ..models.auth_user_user_metadata import AuthUserUserMetadata





T = TypeVar("T", bound="AuthUser")



@_attrs_define
class AuthUser:
    """ 
        Attributes:
            id (UUID):
            email (str):
            status (AuthUserStatus):
            project_id (UUID | Unset):
            email_confirmed (bool | Unset):
            user_metadata (AuthUserUserMetadata | Unset): User-editable metadata
            app_metadata (AuthUserAppMetadata | Unset): Application-controlled metadata (read-only for users)
            avatar_url (str | Unset): User avatar URL (from OAuth provider or manually set)
            banned_until (datetime.datetime | None | Unset): When temporary ban expires (null if not banned or permanent)
            last_sign_in_at (datetime.datetime | Unset):
            created_at (datetime.datetime | Unset):
            updated_at (datetime.datetime | Unset):
     """

    id: UUID
    email: str
    status: AuthUserStatus
    project_id: UUID | Unset = UNSET
    email_confirmed: bool | Unset = UNSET
    user_metadata: AuthUserUserMetadata | Unset = UNSET
    app_metadata: AuthUserAppMetadata | Unset = UNSET
    avatar_url: str | Unset = UNSET
    banned_until: datetime.datetime | None | Unset = UNSET
    last_sign_in_at: datetime.datetime | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_user_app_metadata import AuthUserAppMetadata
        from ..models.auth_user_user_metadata import AuthUserUserMetadata
        id = str(self.id)

        email = self.email

        status: str = self.status

        project_id: str | Unset = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        email_confirmed = self.email_confirmed

        user_metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()

        app_metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.app_metadata, Unset):
            app_metadata = self.app_metadata.to_dict()

        avatar_url = self.avatar_url

        banned_until: None | str | Unset
        if isinstance(self.banned_until, Unset):
            banned_until = UNSET
        elif isinstance(self.banned_until, datetime.datetime):
            banned_until = self.banned_until.isoformat()
        else:
            banned_until = self.banned_until

        last_sign_in_at: str | Unset = UNSET
        if not isinstance(self.last_sign_in_at, Unset):
            last_sign_in_at = self.last_sign_in_at.isoformat()

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "email": email,
            "status": status,
        })
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if email_confirmed is not UNSET:
            field_dict["email_confirmed"] = email_confirmed
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata
        if app_metadata is not UNSET:
            field_dict["app_metadata"] = app_metadata
        if avatar_url is not UNSET:
            field_dict["avatar_url"] = avatar_url
        if banned_until is not UNSET:
            field_dict["banned_until"] = banned_until
        if last_sign_in_at is not UNSET:
            field_dict["last_sign_in_at"] = last_sign_in_at
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_user_app_metadata import AuthUserAppMetadata
        from ..models.auth_user_user_metadata import AuthUserUserMetadata
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        email = d.pop("email")

        status = check_auth_user_status(d.pop("status"))




        _project_id = d.pop("project_id", UNSET)
        project_id: UUID | Unset
        if isinstance(_project_id,  Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)




        email_confirmed = d.pop("email_confirmed", UNSET)

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: AuthUserUserMetadata | Unset
        if isinstance(_user_metadata,  Unset):
            user_metadata = UNSET
        else:
            user_metadata = AuthUserUserMetadata.from_dict(_user_metadata)




        _app_metadata = d.pop("app_metadata", UNSET)
        app_metadata: AuthUserAppMetadata | Unset
        if isinstance(_app_metadata,  Unset):
            app_metadata = UNSET
        else:
            app_metadata = AuthUserAppMetadata.from_dict(_app_metadata)




        avatar_url = d.pop("avatar_url", UNSET)

        def _parse_banned_until(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                banned_until_type_0 = datetime.datetime.fromisoformat(data)



                return banned_until_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        banned_until = _parse_banned_until(d.pop("banned_until", UNSET))


        _last_sign_in_at = d.pop("last_sign_in_at", UNSET)
        last_sign_in_at: datetime.datetime | Unset
        if isinstance(_last_sign_in_at,  Unset):
            last_sign_in_at = UNSET
        else:
            last_sign_in_at = datetime.datetime.fromisoformat(_last_sign_in_at)




        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)




        _updated_at = d.pop("updated_at", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at,  Unset):
            updated_at = UNSET
        else:
            updated_at = datetime.datetime.fromisoformat(_updated_at)




        auth_user = cls(
            id=id,
            email=email,
            status=status,
            project_id=project_id,
            email_confirmed=email_confirmed,
            user_metadata=user_metadata,
            app_metadata=app_metadata,
            avatar_url=avatar_url,
            banned_until=banned_until,
            last_sign_in_at=last_sign_in_at,
            created_at=created_at,
            updated_at=updated_at,
        )


        auth_user.additional_properties = d
        return auth_user

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
