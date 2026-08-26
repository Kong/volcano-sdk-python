from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_config_database_database_type import check_project_config_database_database_type
from ..models.project_config_database_database_type import ProjectConfigDatabaseDatabaseType
from ..models.project_config_database_pg_version import check_project_config_database_pg_version
from ..models.project_config_database_pg_version import ProjectConfigDatabasePgVersion
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProjectConfigDatabase")



@_attrs_define
class ProjectConfigDatabase:
    """ Assertion-only entry for an existing database. No database property is
    mutable through the manifest; declared values are compared against the
    deployed database and any mismatch fails validation. Databases are
    never created or deleted here.

        Attributes:
            name (str):
            region (str): Deployed region ID (e.g. aws-us-east-1). Asserted, never written.
            pg_version (ProjectConfigDatabasePgVersion): PostgreSQL major version. Asserted, never written.
            database_type (ProjectConfigDatabaseDatabaseType | Unset): Compute tier. Asserted, never written - tier changes
                are not
                supported via the manifest; use the databases API/CLI/GUI instead.
     """

    name: str
    region: str
    pg_version: ProjectConfigDatabasePgVersion
    database_type: ProjectConfigDatabaseDatabaseType | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        region = self.region

        pg_version: str = self.pg_version

        database_type: str | Unset = UNSET
        if not isinstance(self.database_type, Unset):
            database_type = self.database_type



        field_dict: dict[str, Any] = {}

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

        pg_version = check_project_config_database_pg_version(d.pop("pg_version"))




        _database_type = d.pop("database_type", UNSET)
        database_type: ProjectConfigDatabaseDatabaseType | Unset
        if isinstance(_database_type,  Unset):
            database_type = UNSET
        else:
            database_type = check_project_config_database_database_type(_database_type)




        project_config_database = cls(
            name=name,
            region=region,
            pg_version=pg_version,
            database_type=database_type,
        )

        return project_config_database

