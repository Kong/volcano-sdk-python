"""Database query facade."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Protocol

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
        response = invoke(
            self._client._transport.query_database_select,
            authorization=self._client._session_token(),
            database_name=self._database_name,
            body=body,
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
