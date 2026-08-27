from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.database_database_type import check_database_database_type
from ..models.database_database_type import DatabaseDatabaseType
from ..models.database_status import check_database_status
from ..models.database_status import DatabaseStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="Database")



@_attrs_define
class Database:
    """ PostgreSQL database with automatic scalability and security features.

        Attributes:
            id (UUID):
            project_id (UUID):
            name (str): Database name
            status (DatabaseStatus): Database provisioning status
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            provisioning_started_at (datetime.datetime | Unset): Timestamp when the current provisioning phase started
            connection_string (str | Unset): Secure PostgreSQL connection URI for your database.

                The database is identified by the globally-unique username
                (`volcano_client_{database_id}`) already in this URI; the
                `application_name` parameter only selects the access mode:
                - `volcano_full_access` — Full admin access (DDL, migrations)
                - `volcano_user_access:{user_id}` — User impersonation (RLS enforced)
                - `volcano_user_access` — Anonymous access (anon role, RLS enforced)
            region (str | Unset): Region where the database is hosted Example: aws-us-east-1.
            pg_version (str | Unset): PostgreSQL major version Example: 16.
            database_type (DatabaseDatabaseType | Unset): Database size tier that determines available RAM and scaling
                limits.
                 Example: volcano-db-xs.
            storage_bytes (int | Unset): Latest observed on-disk size from `pg_database_size`, in bytes. This
                point-in-time gauge may be absent until the database has been sampled.
                Summing the latest samples for every database in a project produces
                the project's "Database Storage (Bytes)" usage gauge. Populated on
                database list responses; single-database responses omit it.
            last_invoked_at (datetime.datetime | Unset): Most recent request timestamp for this database
     """

    id: UUID
    project_id: UUID
    name: str
    status: DatabaseStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    provisioning_started_at: datetime.datetime | Unset = UNSET
    connection_string: str | Unset = UNSET
    region: str | Unset = UNSET
    pg_version: str | Unset = UNSET
    database_type: DatabaseDatabaseType | Unset = UNSET
    storage_bytes: int | Unset = UNSET
    last_invoked_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id = str(self.project_id)

        name = self.name

        status: str = self.status

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        provisioning_started_at: str | Unset = UNSET
        if not isinstance(self.provisioning_started_at, Unset):
            provisioning_started_at = self.provisioning_started_at.isoformat()

        connection_string = self.connection_string

        region = self.region

        pg_version = self.pg_version

        database_type: str | Unset = UNSET
        if not isinstance(self.database_type, Unset):
            database_type = self.database_type


        storage_bytes = self.storage_bytes

        last_invoked_at: str | Unset = UNSET
        if not isinstance(self.last_invoked_at, Unset):
            last_invoked_at = self.last_invoked_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "project_id": project_id,
            "name": name,
            "status": status,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if provisioning_started_at is not UNSET:
            field_dict["provisioning_started_at"] = provisioning_started_at
        if connection_string is not UNSET:
            field_dict["connection_string"] = connection_string
        if region is not UNSET:
            field_dict["region"] = region
        if pg_version is not UNSET:
            field_dict["pg_version"] = pg_version
        if database_type is not UNSET:
            field_dict["database_type"] = database_type
        if storage_bytes is not UNSET:
            field_dict["storage_bytes"] = storage_bytes
        if last_invoked_at is not UNSET:
            field_dict["last_invoked_at"] = last_invoked_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        name = d.pop("name")

        status = check_database_status(d.pop("status"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        _provisioning_started_at = d.pop("provisioning_started_at", UNSET)
        provisioning_started_at: datetime.datetime | Unset
        if isinstance(_provisioning_started_at,  Unset):
            provisioning_started_at = UNSET
        else:
            provisioning_started_at = datetime.datetime.fromisoformat(_provisioning_started_at)




        connection_string = d.pop("connection_string", UNSET)

        region = d.pop("region", UNSET)

        pg_version = d.pop("pg_version", UNSET)

        _database_type = d.pop("database_type", UNSET)
        database_type: DatabaseDatabaseType | Unset
        if isinstance(_database_type,  Unset):
            database_type = UNSET
        else:
            database_type = check_database_database_type(_database_type)




        storage_bytes = d.pop("storage_bytes", UNSET)

        _last_invoked_at = d.pop("last_invoked_at", UNSET)
        last_invoked_at: datetime.datetime | Unset
        if isinstance(_last_invoked_at,  Unset):
            last_invoked_at = UNSET
        else:
            last_invoked_at = datetime.datetime.fromisoformat(_last_invoked_at)




        database = cls(
            id=id,
            project_id=project_id,
            name=name,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            provisioning_started_at=provisioning_started_at,
            connection_string=connection_string,
            region=region,
            pg_version=pg_version,
            database_type=database_type,
            storage_bytes=storage_bytes,
            last_invoked_at=last_invoked_at,
        )


        database.additional_properties = d
        return database

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
