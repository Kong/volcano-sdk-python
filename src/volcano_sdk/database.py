from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Protocol

from ._transport import Transport, invoke, response_payload


class DatabaseContext(Protocol):
    _transport: Transport

    def _session_token(self) -> str: ...


@dataclass(frozen=True, slots=True)
class QueryBuilder:
    _client: DatabaseContext
    _database_name: str
    _table: str
    _columns: tuple[str, ...] = ()
    _filters: tuple[dict[str, Any], ...] = ()

    def select(self, *columns: str) -> QueryBuilder:
        return replace(self, _columns=columns)

    def eq(self, column: str, value: Any) -> QueryBuilder:
        condition = {"column": column, "operator": "eq", "value": value}
        return replace(self, _filters=(*self._filters, condition))

    def execute(self) -> list[dict[str, Any]]:
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
    _client: DatabaseContext
    _name: str

    def from_(self, table: str) -> QueryBuilder:
        return QueryBuilder(self._client, self._name, table)
