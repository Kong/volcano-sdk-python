"""Database query facade."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from .models import JSONValue

from ._transport import Transport, invoke, response_payload


class DatabaseContext(Protocol):
    """Client capabilities required by database queries."""

    _transport: Transport

    def _session_token(self) -> str: ...


@dataclass(frozen=True, slots=True)
class QueryBuilder:
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
        """Select the requested columns."""
        return replace(self, _columns=columns)

    def eq(self, column: str, value: object) -> QueryBuilder:
        """Add an equality filter."""
        return self._filter(column, "eq", value)

    def neq(self, column: str, value: object) -> QueryBuilder:
        """Add an inequality filter."""
        return self._filter(column, "neq", value)

    def gt(self, column: str, value: object) -> QueryBuilder:
        """Add a greater-than filter."""
        return self._filter(column, "gt", value)

    def gte(self, column: str, value: object) -> QueryBuilder:
        """Add a greater-than-or-equal filter."""
        return self._filter(column, "gte", value)

    def lt(self, column: str, value: object) -> QueryBuilder:
        """Add a less-than filter."""
        return self._filter(column, "lt", value)

    def lte(self, column: str, value: object) -> QueryBuilder:
        """Add a less-than-or-equal filter."""
        return self._filter(column, "lte", value)

    def like(self, column: str, pattern: str) -> QueryBuilder:
        """Add a case-sensitive pattern filter."""
        return self._filter(column, "like", pattern)

    def ilike(self, column: str, pattern: str) -> QueryBuilder:
        """Add a case-insensitive pattern filter."""
        return self._filter(column, "ilike", pattern)

    def is_(self, column: str, value: object) -> QueryBuilder:
        """Add a null or boolean identity filter."""
        return self._filter(column, "is", value)

    def in_(self, column: str, values: Sequence[object]) -> QueryBuilder:
        """Add a membership filter."""
        return self._filter(column, "in", list(values))

    def insert(self, values: Mapping[str, JSONValue]) -> InsertBuilder:
        """Build an insert for this table."""
        return InsertBuilder(
            self._client,
            self._database_name,
            self._table,
            deepcopy(dict(values)),
        )

    def order(self, column: str, *, ascending: bool = True) -> QueryBuilder:
        """Add an ordering clause."""
        clause = {"column": column, "ascending": ascending}
        return replace(self, _order=(*self._order, clause))

    def limit(self, count: int) -> QueryBuilder:
        """Limit the number of returned rows."""
        return replace(self, _limit=count)

    def offset(self, count: int) -> QueryBuilder:
        """Skip rows before returning results."""
        return replace(self, _offset=count)

    def _filter(self, column: str, operator: str, value: object) -> QueryBuilder:
        condition = {"column": column, "operator": operator, "value": value}
        return replace(self, _filters=(*self._filters, condition))

    def execute(self) -> list[dict[str, Any]]:
        """Execute the query and return its rows."""
        body: dict[str, Any] = {"table": self._table}
        if self._columns and self._columns != ("*",):
            body["select"] = list(self._columns)
        if self._filters:
            body["filters"] = list(self._filters)
        if self._order:
            body["order"] = list(self._order)
        if self._limit is not None:
            body["limit"] = self._limit
        if self._offset is not None:
            body["offset"] = self._offset
        response = invoke(
            self._client._transport.query_database_select,
            authorization=self._client._session_token(),
            database_name=self._database_name,
            body=body,
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
        """Insert one row and return the inserted rows."""
        response = invoke(
            self._client._transport.query_database_insert,
            authorization=self._client._session_token(),
            database_name=self._database_name,
            body={"table": self._table, "values": deepcopy(self._values)},
        )
        payload = response_payload(response, 200)
        return list(payload["data"])


@dataclass(frozen=True, slots=True)
class Database:
    """Entry point for queries against one database."""

    _client: DatabaseContext
    _name: str

    def from_(self, table: str) -> QueryBuilder:
        """Create a query builder for a table."""
        return QueryBuilder(self._client, self._name, table)
