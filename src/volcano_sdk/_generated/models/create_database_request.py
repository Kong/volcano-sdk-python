from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_database_request_database_type import check_create_database_request_database_type
from ..models.create_database_request_database_type import CreateDatabaseRequestDatabaseType
from ..models.create_database_request_pg_version import check_create_database_request_pg_version
from ..models.create_database_request_pg_version import CreateDatabaseRequestPgVersion
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="CreateDatabaseRequest")



@_attrs_define
class CreateDatabaseRequest:
    """ Create a new PostgreSQL database. Volcano automatically sets up:
    - Auth helpers (auth.uid(), auth.email(), auth.role())
    - Database roles (anon for unauthenticated, authenticated for signed-in users)
    - Secure multi-tenant isolation
    - Ready for Row-Level Security

        Attributes:
            name (str): Database name (must be unique within project) Example: my_database.
            region (str): Region for database hosting. The accepted values are the regions this
                environment runs in, so read them from `GET /databases/regions` rather
                than hardcoding a list. A region the environment does not offer is
                rejected with 400.
                 Example: aws-us-east-1.
            pg_version (CreateDatabaseRequestPgVersion): PostgreSQL major version Example: 16.
            database_type (CreateDatabaseRequestDatabaseType | Unset): Compute size tier (optional, defaults to volcano-db-
                xs).
                Determines autoscaling limits for the database.
                 Default: 'volcano-db-xs'. Example: volcano-db-xs.
     """

    name: str
    region: str
    pg_version: CreateDatabaseRequestPgVersion
    database_type: CreateDatabaseRequestDatabaseType | Unset = 'volcano-db-xs'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        region = self.region

        pg_version: str = self.pg_version

        database_type: str | Unset = UNSET
        if not isinstance(self.database_type, Unset):
            database_type = self.database_type



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "region": region,
            "pg_version": pg_version,
        })
        if database_type is not UNSET:
            field_dict["database_type"] = database_type

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        region = d.pop("region")

        pg_version = check_create_database_request_pg_version(d.pop("pg_version"))




        _database_type = d.pop("database_type", UNSET)
        database_type: CreateDatabaseRequestDatabaseType | Unset
        if isinstance(_database_type,  Unset):
            database_type = UNSET
        else:
            database_type = check_create_database_request_database_type(_database_type)




        create_database_request = cls(
            name=name,
            region=region,
            pg_version=pg_version,
            database_type=database_type,
        )


        create_database_request.additional_properties = d
        return create_database_request

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
