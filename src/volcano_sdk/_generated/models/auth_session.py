from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auth_session_provider import AuthSessionProvider
from ..models.auth_session_provider import check_auth_session_provider
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="AuthSession")



@_attrs_define
class AuthSession:
    """ An authentication session for a user

        Attributes:
            id (UUID): Unique session identifier
            user_id (UUID): The user this session belongs to
            provider (AuthSessionProvider): Authentication provider used to create this session Example: email.
            expires_at (datetime.datetime): When this session expires
            is_active (bool): Whether the session is currently active (not expired)
            is_current (bool): Whether this is the session making the current request
            user_agent (str | Unset): Browser/device user agent string Example: Mozilla/5.0 (Macintosh; Intel Mac OS X
                10_15_7).
            ip_address (str | Unset): IP address of the client when the session was created Example: 192.168.1.1.
            last_ip_address (str | Unset): IP address of the most recent activity (token refresh) Example: 192.168.1.100.
            last_activity_at (datetime.datetime | Unset): Last activity timestamp
            session_started_at (datetime.datetime | Unset): When the session was created
            created_at (datetime.datetime | Unset):
            updated_at (datetime.datetime | Unset):
     """

    id: UUID
    user_id: UUID
    provider: AuthSessionProvider
    expires_at: datetime.datetime
    is_active: bool
    is_current: bool
    user_agent: str | Unset = UNSET
    ip_address: str | Unset = UNSET
    last_ip_address: str | Unset = UNSET
    last_activity_at: datetime.datetime | Unset = UNSET
    session_started_at: datetime.datetime | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        user_id = str(self.user_id)

        provider: str = self.provider

        expires_at = self.expires_at.isoformat()

        is_active = self.is_active

        is_current = self.is_current

        user_agent = self.user_agent

        ip_address = self.ip_address

        last_ip_address = self.last_ip_address

        last_activity_at: str | Unset = UNSET
        if not isinstance(self.last_activity_at, Unset):
            last_activity_at = self.last_activity_at.isoformat()

        session_started_at: str | Unset = UNSET
        if not isinstance(self.session_started_at, Unset):
            session_started_at = self.session_started_at.isoformat()

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
            "user_id": user_id,
            "provider": provider,
            "expires_at": expires_at,
            "is_active": is_active,
            "is_current": is_current,
        })
        if user_agent is not UNSET:
            field_dict["user_agent"] = user_agent
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address
        if last_ip_address is not UNSET:
            field_dict["last_ip_address"] = last_ip_address
        if last_activity_at is not UNSET:
            field_dict["last_activity_at"] = last_activity_at
        if session_started_at is not UNSET:
            field_dict["session_started_at"] = session_started_at
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        user_id = UUID(d.pop("user_id"))




        provider = check_auth_session_provider(d.pop("provider"))




        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))




        is_active = d.pop("is_active")

        is_current = d.pop("is_current")

        user_agent = d.pop("user_agent", UNSET)

        ip_address = d.pop("ip_address", UNSET)

        last_ip_address = d.pop("last_ip_address", UNSET)

        _last_activity_at = d.pop("last_activity_at", UNSET)
        last_activity_at: datetime.datetime | Unset
        if isinstance(_last_activity_at,  Unset):
            last_activity_at = UNSET
        else:
            last_activity_at = datetime.datetime.fromisoformat(_last_activity_at)




        _session_started_at = d.pop("session_started_at", UNSET)
        session_started_at: datetime.datetime | Unset
        if isinstance(_session_started_at,  Unset):
            session_started_at = UNSET
        else:
            session_started_at = datetime.datetime.fromisoformat(_session_started_at)




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




        auth_session = cls(
            id=id,
            user_id=user_id,
            provider=provider,
            expires_at=expires_at,
            is_active=is_active,
            is_current=is_current,
            user_agent=user_agent,
            ip_address=ip_address,
            last_ip_address=last_ip_address,
            last_activity_at=last_activity_at,
            session_started_at=session_started_at,
            created_at=created_at,
            updated_at=updated_at,
        )


        auth_session.additional_properties = d
        return auth_session

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
