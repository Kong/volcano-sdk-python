from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.import_provider import check_import_provider
from ..models.import_provider import ImportProvider
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="ImportConnection")



@_attrs_define
class ImportConnection:
    """ 
        Attributes:
            id (UUID):
            provider (ImportProvider):
            account_id (str):
            account_name (str):
            configuration_id (str):
            granted_scopes (list[str]):
            status (str):
            last_authenticated_at (datetime.datetime):
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            expires_at (datetime.datetime | None | Unset):
     """

    id: UUID
    provider: ImportProvider
    account_id: str
    account_name: str
    configuration_id: str
    granted_scopes: list[str]
    status: str
    last_authenticated_at: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime
    expires_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        provider: str = self.provider

        account_id = self.account_id

        account_name = self.account_name

        configuration_id = self.configuration_id

        granted_scopes = self.granted_scopes



        status = self.status

        last_authenticated_at = self.last_authenticated_at.isoformat()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "provider": provider,
            "account_id": account_id,
            "account_name": account_name,
            "configuration_id": configuration_id,
            "granted_scopes": granted_scopes,
            "status": status,
            "last_authenticated_at": last_authenticated_at,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        provider = check_import_provider(d.pop("provider"))




        account_id = d.pop("account_id")

        account_name = d.pop("account_name")

        configuration_id = d.pop("configuration_id")

        granted_scopes = cast(list[str], d.pop("granted_scopes"))


        status = d.pop("status")

        last_authenticated_at = datetime.datetime.fromisoformat(d.pop("last_authenticated_at"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        def _parse_expires_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = datetime.datetime.fromisoformat(data)



                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))


        import_connection = cls(
            id=id,
            provider=provider,
            account_id=account_id,
            account_name=account_name,
            configuration_id=configuration_id,
            granted_scopes=granted_scopes,
            status=status,
            last_authenticated_at=last_authenticated_at,
            created_at=created_at,
            updated_at=updated_at,
            expires_at=expires_at,
        )


        import_connection.additional_properties = d
        return import_connection

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
