"""Database query facade."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any, Protocol, Self, cast

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .auth import Auth
    from .models import JSONValue

from ._transport import Transport, invoke, response_payload


def _snapshot_json(value: JSONValue) -> JSONValue:
    if isinstance(value, Mapping):
        return {key: _snapshot_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_snapshot_json(item) for item in value]
    return value


def _snapshot_row(values: Mapping[str, JSONValue]) -> dict[str, JSONValue]:
    return {key: _snapshot_json(value) for key, value in values.items()}


def _snapshot_filter_value(value: object) -> object:
    if isinstance(value, Mapping):
        mapping = cast("Mapping[object, object]", value)
        return {key: _snapshot_filter_value(item) for key, item in mapping.items()}
    if isinstance(value, (list, tuple)):
        sequence = cast("list[object] | tuple[object, ...]", value)
        return [_snapshot_filter_value(item) for item in sequence]
    return value


class DatabaseContext(Protocol):
    """Client capabilities required by database queries."""

    _transport: Transport
    auth: Auth

    def _session_token(self) -> str: ...


class FilterBuilder:
    """Shared immutable filters for database operations."""

    _filters: tuple[dict[str, Any], ...]

    def _with_filters(self, filters: tuple[dict[str, Any], ...]) -> Self:
        raise NotImplementedError

    def eq(self, column: str, value: object) -> Self:
        """Add an equality filter.

        Returns
        -------
        Self
            A new builder with this filter appended; the original is unchanged.

        """
        return self._filter(column, "eq", value)

    def neq(self, column: str, value: object) -> Self:
        """Add an inequality filter.

        Returns
        -------
        Self
            A new builder with this filter appended; the original is unchanged.

        """
        return self._filter(column, "neq", value)

    def gt(self, column: str, value: object) -> Self:
        """Add a greater-than filter.

        Returns
        -------
        Self
            A new builder with this filter appended; the original is unchanged.

        """
        return self._filter(column, "gt", value)

    def gte(self, column: str, value: object) -> Self:
        """Add a greater-than-or-equal filter.

        Returns
        -------
        Self
            A new builder with this filter appended; the original is unchanged.

        """
        return self._filter(column, "gte", value)

    def lt(self, column: str, value: object) -> Self:
        """Add a less-than filter.

        Returns
        -------
        Self
            A new builder with this filter appended; the original is unchanged.

        """
        return self._filter(column, "lt", value)

    def lte(self, column: str, value: object) -> Self:
        """Add a less-than-or-equal filter.

        Returns
        -------
        Self
            A new builder with this filter appended; the original is unchanged.

        """
        return self._filter(column, "lte", value)

    def like(self, column: str, pattern: str) -> Self:
        """Add a case-sensitive pattern filter.

        Returns
        -------
        Self
            A new builder with this filter appended; the original is unchanged.

        """
        return self._filter(column, "like", pattern)

    def ilike(self, column: str, pattern: str) -> Self:
        """Add a case-insensitive pattern filter.

        Returns
        -------
        Self
            A new builder with this filter appended; the original is unchanged.

        """
        return self._filter(column, "ilike", pattern)

    def is_(self, column: str, value: object) -> Self:
        """Add a null or boolean identity filter.

        Returns
        -------
        Self
            A new builder with this filter appended; the original is unchanged.

        """
        return self._filter(column, "is", value)

    def in_(self, column: str, values: Sequence[object]) -> Self:
        """Add a membership filter.

        Returns
        -------
        Self
            A new builder with this filter appended; the original is unchanged.

        """
        return self._filter(column, "in", list(values))

    def _filter(self, column: str, operator: str, value: object) -> Self:
        condition = {
            "column": column,
            "operator": operator,
            "value": _snapshot_filter_value(value),
        }
        return self._with_filters((*self._filters, condition))


@dataclass(frozen=True, slots=True)
class QueryBuilder(FilterBuilder):
    """Build and execute an immutable database select query."""

    _client: DatabaseContext
    _database_name: str
    _table: str
    _columns: tuple[str, ...] = ()
    _filters: tuple[dict[str, Any], ...] = ()
    _order: tuple[dict[str, Any], ...] = ()
    _limit: int | None = None
    _offset: int | None = None

    def select(self, *columns: str) -> QueryBuilder:
        """Select the requested columns.

        Returns
        -------
        QueryBuilder
            A new query with the requested columns and existing filters.

        """
        return replace(self, _columns=columns)

    def insert(self, values: Mapping[str, JSONValue]) -> InsertBuilder:
        """Build an insert for this table.

        Returns
        -------
        InsertBuilder
            An insert builder with a snapshot of the supplied row values.

        """
        return InsertBuilder(
            self._client,
            self._database_name,
            self._table,
            _snapshot_row(values),
        )

    def update(self, values: Mapping[str, JSONValue]) -> UpdateBuilder:
        """Build a filtered update for this table.

        Returns
        -------
        UpdateBuilder
            An update builder with the existing filters and a snapshot of the values.

        """
        return UpdateBuilder(
            self._client,
            self._database_name,
            self._table,
            _snapshot_row(values),
            self._filters,
        )

    def delete(self) -> DeleteBuilder:
        """Build a filtered delete for this table.

        Returns
        -------
        DeleteBuilder
            A delete builder carrying the existing filters.

        """
        return DeleteBuilder(
            self._client,
            self._database_name,
            self._table,
            self._filters,
        )

    def order(self, column: str, *, ascending: bool = True) -> QueryBuilder:
        """Add an ordering clause.

        Returns
        -------
        QueryBuilder
            A new query with this ordering clause appended.

        """
        clause = {"column": column, "ascending": ascending}
        return replace(self, _order=(*self._order, clause))

    def limit(self, count: int) -> QueryBuilder:
        """Limit the number of returned rows.

        Returns
        -------
        QueryBuilder
            A new query with the row limit replaced.

        """
        return replace(self, _limit=count)

    def offset(self, count: int) -> QueryBuilder:
        """Skip rows before returning results.

        Returns
        -------
        QueryBuilder
            A new query with the row offset replaced.

        """
        return replace(self, _offset=count)

    def _with_filters(self, filters: tuple[dict[str, Any], ...]) -> QueryBuilder:
        return replace(self, _filters=filters)

    def _request_body(self) -> dict[str, object]:
        body: dict[str, object] = {"table": self._table}
        if self._columns and self._columns != ("*",):
            body["select"] = list(self._columns)
        if self._filters:
            body["filters"] = list(self._filters)
        if self._order:
            body["order"] = list(self._order)
        return body | self._pagination()

    def _pagination(self) -> dict[str, int]:
        return {
            name: value
            for name, value in (("limit", self._limit), ("offset", self._offset))
            if value is not None
        }

    def execute(self) -> list[dict[str, Any]]:
        """Execute the query and return its rows.

        Returns
        -------
        list[dict[str, Any]]
            Rows returned by the select request.

        """
        body = self._request_body()
        response = self._client.auth._session_request(
            lambda token: invoke(
                self._client._transport.query_database_select,
                authorization=token,
                database_name=self._database_name,
                body=body,
            )
        )
        payload = response_payload(response, 200)
        return list(payload["data"])


@dataclass(frozen=True, slots=True)
class InsertBuilder:
    """Build and execute an immutable database insert."""

    _client: DatabaseContext
    _database_name: str
    _table: str
    _values: dict[str, JSONValue]

    def execute(self) -> list[dict[str, Any]]:
        """Insert one row and return the inserted rows.

        Returns
        -------
        list[dict[str, Any]]
            Inserted rows returned by the server.

        """
        response = self._client.auth._session_request(
            lambda token: invoke(
                self._client._transport.query_database_insert,
                authorization=token,
                database_name=self._database_name,
                body={"table": self._table, "values": _snapshot_row(self._values)},
            )
        )
        payload = response_payload(response, 200)
        return list(payload["data"])


@dataclass(frozen=True, slots=True)
class UpdateBuilder(FilterBuilder):
    """Build and execute an immutable filtered database update."""

    _client: DatabaseContext
    _database_name: str
    _table: str
    _values: dict[str, JSONValue]
    _filters: tuple[dict[str, Any], ...] = ()

    def _with_filters(self, filters: tuple[dict[str, Any], ...]) -> UpdateBuilder:
        return replace(self, _filters=filters)

    def execute(self) -> list[dict[str, Any]]:
        """Update matching rows and return them.

        Returns
        -------
        list[dict[str, Any]]
            Updated rows returned by the server.

        """
        response = self._client.auth._session_request(
            lambda token: invoke(
                self._client._transport.query_database_update,
                authorization=token,
                database_name=self._database_name,
                body={
                    "table": self._table,
                    "values": _snapshot_row(self._values),
                    "filters": list(self._filters),
                },
            )
        )
        payload = response_payload(response, 200)
        return list(payload["data"])


@dataclass(frozen=True, slots=True)
class DeleteBuilder(FilterBuilder):
    """Build and execute an immutable filtered database delete."""

    _client: DatabaseContext
    _database_name: str
    _table: str
    _filters: tuple[dict[str, Any], ...] = ()

    def _with_filters(self, filters: tuple[dict[str, Any], ...]) -> DeleteBuilder:
        return replace(self, _filters=filters)

    def execute(self) -> list[dict[str, Any]]:
        """Delete matching rows and return them.

        Returns
        -------
        list[dict[str, Any]]
            Deleted rows returned by the server.

        """
        response = self._client.auth._session_request(
            lambda token: invoke(
                self._client._transport.query_database_delete,
                authorization=token,
                database_name=self._database_name,
                body={"table": self._table, "filters": list(self._filters)},
            )
        )
        payload = response_payload(response, 200)
        return list(payload["data"])


@dataclass(frozen=True, slots=True)
class Database:
    """Entry point for queries against one database."""

    _client: DatabaseContext
    _name: str

    def from_(self, table: str) -> QueryBuilder:
        """Create a query builder for a table.

        Returns
        -------
        QueryBuilder
            An unfiltered select builder for the named table.

        """
        return QueryBuilder(self._client, self._name, table)
