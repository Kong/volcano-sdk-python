from typing import Literal

ProjectConfigDatabasePgVersion = Literal['15', '16']

PROJECT_CONFIG_DATABASE_PG_VERSION_VALUES: set[ProjectConfigDatabasePgVersion] = { '15', '16',  }

def check_project_config_database_pg_version(value: str) -> ProjectConfigDatabasePgVersion:
    if value in PROJECT_CONFIG_DATABASE_PG_VERSION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_CONFIG_DATABASE_PG_VERSION_VALUES!r}")
