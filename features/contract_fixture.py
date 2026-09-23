"""Typed boundary for the shared SDK contract fixture."""

from __future__ import annotations

from typing import TypeAlias, TypedDict, TypeGuard

ContractRow: TypeAlias = dict[str, str]


class UpdateRows(TypedDict):
    """Expected before and after values for an update scenario."""

    before: ContractRow
    after: ContractRow


class MutationRows(TypedDict):
    """Rows used by the shared mutation scenarios."""

    insert: ContractRow
    update: UpdateRows
    delete: ContractRow


class ContractFixture(TypedDict):
    """Fields provisioned by Hosting for the Python contract runner."""

    api_url: str
    project_id: str
    anon_key: str
    service_key: str
    platform_token: str
    user_id: str
    user_email: str
    user_password: str
    database_name: str
    table_name: str
    query_table_name: str
    fixture_row: ContractRow
    mutation_rows: MutationRows
    bucket_name: str
    storage_path: str
    realtime_channel: str
    realtime_table_name: str
    lock_key: str
    function_name: str
    function_id: str
    durable_function_name: str
    logs_access_token: str


STRING_FIELDS = (
    "api_url",
    "project_id",
    "anon_key",
    "service_key",
    "platform_token",
    "user_id",
    "user_email",
    "user_password",
    "database_name",
    "table_name",
    "query_table_name",
    "bucket_name",
    "storage_path",
    "realtime_channel",
    "realtime_table_name",
    "lock_key",
    "function_name",
    "function_id",
    "durable_function_name",
    "logs_access_token",
)


def is_object_dict(value: object) -> TypeGuard[dict[object, object]]:
    """Narrow a decoded dictionary without trusting its keys or values."""
    return isinstance(value, dict)


def is_contract_row(value: object) -> TypeGuard[ContractRow]:
    """Check the fields read by the database scenarios."""
    if not is_object_dict(value):
        return False
    return (
        all(
            isinstance(key, str) and isinstance(item, str)
            for key, item in value.items()
        )
        and "slug" in value
        and "value" in value
    )


def is_update_rows(value: object) -> TypeGuard[UpdateRows]:
    """Check both states of the update scenario."""
    if not is_object_dict(value):
        return False
    return is_contract_row(value.get("before")) and is_contract_row(value.get("after"))


def is_mutation_rows(value: object) -> TypeGuard[MutationRows]:
    """Check the three mutation fixtures."""
    if not is_object_dict(value):
        return False
    return (
        is_contract_row(value.get("insert"))
        and is_update_rows(value.get("update"))
        and is_contract_row(value.get("delete"))
    )


def is_contract_fixture(value: object) -> TypeGuard[ContractFixture]:
    """Validate every field consumed by the shared scenarios."""
    if not is_object_dict(value):
        return False
    if any(not isinstance(value.get(key), str) for key in STRING_FIELDS):
        return False
    return is_contract_row(value.get("fixture_row")) and is_mutation_rows(
        value.get("mutation_rows")
    )
